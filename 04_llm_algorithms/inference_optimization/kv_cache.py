"""
题目：KV Cache 原理与实现
难度：Medium | 高频出现：字节/阿里/百度（LLM推理岗）
标签：KV Cache、自回归生成、推理优化


题目描述
---------
手写实现 KV Cache（键值缓存），这是 LLM 自回归推理的核心优化技术。
自回归生成时，每步生成新 token 都需要与所有之前的 token 做注意力计算。
KV Cache 将已计算的 K、V 缓存起来，避免重复计算，将推理复杂度从 O(n²) 降至 O(n)。

实现要点：
  - Prefill 阶段：一次性处理所有 prompt token，填充 KV Cache
  - Decode 阶段：每次只计算新 token 的 K、V，并追加到 Cache
  - 内存管理：Cache 大小 = batch_size × num_layers × 2 × max_len × num_heads × head_dim

输入/输出
----------
输入: new_Q（B,1,d），cached_K（B,L,d），cached_V（B,L,d）
输出: 注意力输出（B,1,d），更新后的 KV Cache

约束
------
- 内存限制是 KV Cache 在长序列推理时的主要瓶颈

TL;DR（30秒速览）
- 推理时每步只计算新 token 的 Q，K/V 追加到缓存后复用
- 无 KV Cache：每步 O(t²) 计算；有 KV Cache：每步 O(t)
- 显存占用：2 × n_layers × n_kv_heads × max_seq × d_head × dtype

详细解析
---------
自回归生成流程：
  Prefill 阶段（处理 prompt）：
    完整输入，并行计算所有 token 的 K/V，存入 cache
  Decode 阶段（生成每个新 token）：
    输入只有 1 个新 token（或当前 token）
    计算新 Q, 新 K_new, 新 V_new
    K_cache = cat(K_cache_prev, K_new)
    V_cache = cat(V_cache_prev, V_new)
    Attention 用新 Q 和完整 K_cache / V_cache

KV Cache 的代价：
  显存是主要瓶颈，这也是 MQA/GQA 存在的动机（减少 kv_heads）
"""

import numpy as np
from collections import defaultdict


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)


class KVCache:
    """简单 KV 缓存实现（单层）"""
    def __init__(self):
        self.k_cache = None  # (batch, num_heads, seq, d_head)
        self.v_cache = None

    def update(self, new_k: np.ndarray, new_v: np.ndarray):
        """追加新 token 的 K/V"""
        if self.k_cache is None:
            self.k_cache = new_k
            self.v_cache = new_v
        else:
            self.k_cache = np.concatenate([self.k_cache, new_k], axis=2)  # 沿 seq 维度拼接
            self.v_cache = np.concatenate([self.v_cache, new_v], axis=2)
        return self.k_cache, self.v_cache

    def reset(self):
        self.k_cache = None
        self.v_cache = None

    @property
    def seq_len(self):
        return 0 if self.k_cache is None else self.k_cache.shape[2]


class SimpleAttentionWithKVCache:
    def __init__(self, d_model: int, num_heads: int):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads
        scale = 0.01
        self.Wq = np.random.randn(d_model, d_model) * scale
        self.Wk = np.random.randn(d_model, d_model) * scale
        self.Wv = np.random.randn(d_model, d_model) * scale
        self.Wo = np.random.randn(d_model, d_model) * scale
        self.kv_cache = KVCache()

    def forward(self, x: np.ndarray, use_cache: bool = True) -> np.ndarray:
        """
        x: (batch, seq_len, d_model)
        use_cache: 是否使用 KV Cache（decode 阶段为 True）
        """
        batch, seq, _ = x.shape

        def split_heads(t):
            return t.reshape(batch, seq, self.num_heads, self.d_head).transpose(0, 2, 1, 3)

        Q = split_heads(x @ self.Wq)
        K_new = split_heads(x @ self.Wk)
        V_new = split_heads(x @ self.Wv)

        if use_cache:
            K, V = self.kv_cache.update(K_new, V_new)
        else:
            K, V = K_new, V_new

        scores = Q @ K.swapaxes(-2, -1) / np.sqrt(self.d_head)
        attn = softmax(scores, axis=-1)
        context = (attn @ V).transpose(0, 2, 1, 3).reshape(batch, seq, self.d_model)
        return context @ self.Wo

    def reset_cache(self):
        self.kv_cache.reset()


def kv_cache_memory_bytes(n_layers, n_kv_heads, max_seq_len, d_head, dtype_bytes=2):
    """计算 KV Cache 显存占用（字节）"""
    return 2 * n_layers * n_kv_heads * max_seq_len * d_head * dtype_bytes


if __name__ == "__main__":
    np.random.seed(42)
    batch, d_model, num_heads = 1, 32, 4

    attn = SimpleAttentionWithKVCache(d_model, num_heads)

    # Prefill：输入 4 个 token
    prompt = np.random.randn(batch, 4, d_model)
    out_prefill = attn.forward(prompt, use_cache=True)
    assert attn.kv_cache.seq_len == 4
    assert out_prefill.shape == (batch, 4, d_model)

    # Decode：逐 token 生成
    for step in range(3):
        new_token = np.random.randn(batch, 1, d_model)
        out = attn.forward(new_token, use_cache=True)
        expected_cache_len = 4 + step + 1
        assert attn.kv_cache.seq_len == expected_cache_len, \
            f"Cache len: {attn.kv_cache.seq_len} != {expected_cache_len}"
        assert out.shape == (batch, 1, d_model)

    # 显存计算示例（LLaMA2-7B）
    mem = kv_cache_memory_bytes(n_layers=32, n_kv_heads=32, max_seq_len=4096, d_head=128)
    print(f"LLaMA2-7B KV Cache (4096 seq): {mem/1e9:.2f} GB (fp16)")

    print("All tests passed.")
