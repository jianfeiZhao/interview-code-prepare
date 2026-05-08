"""
题目：Scaled Dot-Product Attention
难度：Medium | 高频出现：字节/阿里/百度（LLM岗）
标签：Attention、Transformer、自注意力


题目描述
---------
手写实现缩放点积注意力机制（Scaled Dot-Product Attention），这是 Transformer 的核心模块。
给定查询（Q）、键（K）、值（V）矩阵，计算注意力输出：
  Attention(Q, K, V) = softmax(QKᵀ / √d_k) × V

需要支持：
  - 可选的 Mask（因果掩码 causal mask 或 Padding mask）
  - 可选的 Dropout（应用于注意力权重）
  - 批处理（支持 batch 维度）

输入/输出
----------
输入: Q（...×L_q×d_k），K（...×L_k×d_k），V（...×L_k×d_v），mask（可选）
输出: output（...×L_q×d_v），attn_weights（...×L_q×L_k）

约束
------
- 为何除以 √d_k：防止点积过大，使 softmax 梯度稳定
- 因果掩码：上三角填 -inf，实现自回归生成

TL;DR（30秒速览）
- 公式：Attention(Q,K,V) = softmax(QKᵀ / √d_k) × V
- 除以 √d_k：防止点积过大导致 softmax 进入梯度消失区域
- Mask：因果掩码（上三角=−∞）用于自回归解码

详细解析
---------
为什么除以 √d_k？
  Q,K 每个元素均值0，方差1，点积 QKᵀ 方差为 d_k
  除以 √d_k → 方差归一，softmax 梯度稳定

两种 Mask：
  1. Padding Mask：对 <PAD> 位置置 -inf（防止注意力到填充位置）
  2. Causal Mask（因果掩码）：下三角矩阵，只允许看到当前及之前的位置

KV Cache 原理：
  推理时，新 token 只需计算新的 Q，K/V 可以复用缓存
"""

import numpy as np


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
    mask: np.ndarray = None,
) -> tuple:
    """
    Q: (..., seq_len_q, d_k)
    K: (..., seq_len_k, d_k)
    V: (..., seq_len_k, d_v)
    mask: (..., seq_len_q, seq_len_k) bool, True 表示掩盖
    返回: (output, attention_weights)
    """
    d_k = Q.shape[-1]
    scores = Q @ K.swapaxes(-2, -1) / np.sqrt(d_k)  # (..., q, k)

    if mask is not None:
        scores = scores + mask * -1e9  # 掩盖位置填 -inf

    attn_weights = softmax(scores, axis=-1)
    output = attn_weights @ V
    return output, attn_weights


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)


def make_causal_mask(seq_len: int) -> np.ndarray:
    """因果掩码：上三角为 True（不可见）"""
    return np.triu(np.ones((seq_len, seq_len), dtype=bool), k=1)


if __name__ == "__main__":
    np.random.seed(42)
    batch, seq_len, d_k, d_v = 2, 4, 8, 8

    Q = np.random.randn(batch, seq_len, d_k)
    K = np.random.randn(batch, seq_len, d_k)
    V = np.random.randn(batch, seq_len, d_v)

    # 无掩码
    out, attn = scaled_dot_product_attention(Q, K, V)
    assert out.shape == (batch, seq_len, d_v)
    assert np.allclose(attn.sum(axis=-1), 1.0)

    # 因果掩码
    mask = make_causal_mask(seq_len)
    out_causal, attn_causal = scaled_dot_product_attention(Q, K, V, mask)
    # 因果掩码下，上三角注意力权重应为0
    assert np.allclose(attn_causal[0, 0, 1:], 0, atol=1e-6)  # 第1个query只看第0个key
    assert np.allclose(attn_causal[0, 1, 2:], 0, atol=1e-6)  # 第2个query只看前2个

    # 对比 PyTorch
    try:
        import torch
        import torch.nn.functional as F
        Q_t = torch.tensor(Q, dtype=torch.float32)
        K_t = torch.tensor(K, dtype=torch.float32)
        V_t = torch.tensor(V, dtype=torch.float32)
        out_t = F.scaled_dot_product_attention(Q_t, K_t, V_t).numpy()
        assert np.allclose(out, out_t, atol=1e-5)
        print("Matches PyTorch!")
    except ImportError:
        pass

    print("All tests passed.")
