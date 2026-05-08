"""
题目：Grouped Query Attention（GQA）
难度：Hard | 高频出现：字节/阿里（LLM 高级岗）
标签：GQA、MQA、KV Cache、推理优化


题目描述
---------
手写实现分组查询注意力（Grouped Query Attention, GQA），这是 LLaMA 2/3 等模型采用的优化方案。
GQA 是 MHA（多头注意力）和 MQA（多查询注意力）之间的折中：
  - MHA：每个头有独立的 Q、K、V（参数量大，但表达能力强）
  - MQA：所有头共享同一组 K、V（推理快，但质量略降）
  - GQA：将 h 个 Q 头分为 g 组，每组共享一对 K、V（平衡质量与速度）

输入/输出
----------
输入: Q（B, L, h×d_k），K（B, L, g×d_k），V（B, L, g×d_v）
输出: output（B, L, h×d_v）

约束
------
- h 必须被 g 整除（h/g 为每组中 Q 头的数量）
- 推理时 KV Cache 大小降为 MHA 的 g/h

TL;DR（30秒速览）
- GQA：多个 Query 头共享同一组 K/V 头，减少 KV Cache 显存
- MQA = GQA(num_kv_heads=1)，GQA 是 MQA 和 MHA 的折中
- 核心操作：repeat_kv，将 K/V 从 num_kv_heads 复制到 num_heads

详细解析
---------
三者对比：
  MHA: num_q_heads = num_kv_heads = H
  MQA: num_q_heads = H, num_kv_heads = 1
  GQA: num_q_heads = H, num_kv_heads = G，H % G == 0

每组 Query 头数：groups_per_kv = num_q_heads // num_kv_heads

KV Cache 显存对比（以 LLaMA2-70B 为例）：
  MHA: 2 × 80 layers × 4096 × seq_len × dtype
  GQA(G=8): 减少到 1/10，大幅节省显存

实现关键：repeat_kv
  K: (B, kv_heads, S, d_head) → (B, q_heads, S, d_head) 通过重复扩展
"""

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)


def repeat_kv(x: np.ndarray, n_rep: int) -> np.ndarray:
    """
    x: (batch, num_kv_heads, seq, d_head)
    return: (batch, num_kv_heads * n_rep, seq, d_head)
    """
    if n_rep == 1:
        return x
    batch, kv_heads, seq, d_head = x.shape
    x = x[:, :, np.newaxis, :, :]          # (B, kv, 1, S, d)
    x = np.broadcast_to(x, (batch, kv_heads, n_rep, seq, d_head))
    return x.reshape(batch, kv_heads * n_rep, seq, d_head)


class GroupedQueryAttention:
    def __init__(self, d_model: int, num_q_heads: int, num_kv_heads: int):
        assert num_q_heads % num_kv_heads == 0
        self.d_model = d_model
        self.num_q_heads = num_q_heads
        self.num_kv_heads = num_kv_heads
        self.n_rep = num_q_heads // num_kv_heads
        self.d_head = d_model // num_q_heads

        scale = np.sqrt(2.0 / d_model)
        self.Wq = np.random.randn(d_model, d_model) * scale
        self.Wk = np.random.randn(d_model, num_kv_heads * self.d_head) * scale
        self.Wv = np.random.randn(d_model, num_kv_heads * self.d_head) * scale
        self.Wo = np.random.randn(d_model, d_model) * scale

    def forward(self, X: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        batch, seq, _ = X.shape

        Q = (X @ self.Wq).reshape(batch, seq, self.num_q_heads, self.d_head).transpose(0,2,1,3)
        K = (X @ self.Wk).reshape(batch, seq, self.num_kv_heads, self.d_head).transpose(0,2,1,3)
        V = (X @ self.Wv).reshape(batch, seq, self.num_kv_heads, self.d_head).transpose(0,2,1,3)

        # 复制 K/V 到与 Q 相同的头数
        K = repeat_kv(K, self.n_rep)  # (B, num_q_heads, S, d_head)
        V = repeat_kv(V, self.n_rep)

        scores = Q @ K.swapaxes(-2, -1) / np.sqrt(self.d_head)
        if mask is not None:
            scores = scores + mask * -1e9
        attn = softmax(scores, axis=-1)
        out = (attn @ V).transpose(0, 2, 1, 3).reshape(batch, seq, self.d_model)
        return out @ self.Wo


if __name__ == "__main__":
    np.random.seed(42)
    batch, seq, d_model = 2, 8, 64
    X = np.random.randn(batch, seq, d_model)

    # MHA: num_kv_heads = num_q_heads
    mha = GroupedQueryAttention(d_model, num_q_heads=8, num_kv_heads=8)
    out_mha = mha.forward(X)
    assert out_mha.shape == (batch, seq, d_model)

    # MQA: num_kv_heads = 1
    mqa = GroupedQueryAttention(d_model, num_q_heads=8, num_kv_heads=1)
    out_mqa = mqa.forward(X)
    assert out_mqa.shape == (batch, seq, d_model)

    # GQA: num_kv_heads = 2（中间方案）
    gqa = GroupedQueryAttention(d_model, num_q_heads=8, num_kv_heads=2)
    out_gqa = gqa.forward(X)
    assert out_gqa.shape == (batch, seq, d_model)

    print(f"MHA params(K): {d_model*64//8*8}, MQA params(K): {d_model*64//8*1}")
    print("All tests passed.")
