"""
题目：ALiBi（Attention with Linear Biases）位置编码
难度：Medium | 高频出现：字节/阿里
标签：ALiBi、位置编码、长度外推


题目描述
---------
手写实现 ALiBi（Attention with Linear Biases）位置编码，这是另一种适合长序列外推的方案。
ALiBi 不给词向量添加位置编码，而是直接在注意力 logits 上加线性偏置：
  Attention_score(i, j) = QK^T/√d_k - m * (i - j)
其中 m 是每个头固定的斜率（slope），距离越远偏置越大，注意力自然衰减。

关键设计：
  - m 值：2^(-8/H) 的等比数列（H 为头数）
  - 不需要训练，完全确定性的位置编码
  - 对比 RoPE：ALiBi 更简单，但表达能力略弱

输入/输出
----------
输入: attn_logits（B, H, L_q, L_k），形状
输出: biased_logits（B, H, L_q, L_k）

约束
------
- bias 矩阵只与序列长度和头数有关，可预先计算

TL;DR（30秒速览）
- ALiBi：不在 embedding 添加位置信息，而是直接在 attention score 上加线性惩罚
- 惩罚 = -m × |i - j|，m 是每个头的斜率（几何级数）
- 外推性强：无需微调即可处理比训练更长的序列

详细解析
---------
ALiBi 公式：
  score_{ij} = Q_i · K_j / √d - m_h × |i - j|
  m_h = 2^{-8/H × h}，h 从 1 到 H

与 RoPE 对比：
  ALiBi：加法偏置，更简单，适合 inference 外推
  RoPE：旋转变换，相对位置更自然，LLaMA/Mistral 使用
  Sinusoidal：绝对位置，外推性差

使用 ALiBi 的模型：MPT、BLOOM
"""

import numpy as np


def get_alibi_slopes(num_heads: int) -> np.ndarray:
    """
    计算 ALiBi 每个头的斜率 m_h
    对于 num_heads 为 2 的幂，斜率为 2^{-8/H}, 2^{-16/H}, ...
    对于非 2 的幂，使用插值
    """
    def _get_slopes_power_of_2(n):
        start = 2 ** (-(2 ** -(np.log2(n) - 3)))
        ratio = start
        return [start * ratio ** i for i in range(n)]

    if np.log2(num_heads).is_integer():
        return np.array(_get_slopes_power_of_2(num_heads))
    else:
        # 找最近的 2 的幂，插值
        closest_pow2 = int(2 ** np.floor(np.log2(num_heads)))
        slopes = _get_slopes_power_of_2(closest_pow2)
        extra = _get_slopes_power_of_2(2 * closest_pow2)[0::2][:num_heads - closest_pow2]
        return np.array(slopes + extra)


def compute_alibi_bias(num_heads: int, seq_len: int) -> np.ndarray:
    """
    计算 ALiBi 偏置矩阵
    返回: (num_heads, seq_len, seq_len)
    """
    slopes = get_alibi_slopes(num_heads)  # (H,)
    # 位置差矩阵 |i - j|（因果：只看左侧，j <= i）
    positions = np.arange(seq_len)
    distance = positions[np.newaxis, :] - positions[:, np.newaxis]  # (S, S)
    # 取绝对值，因果掩码（j > i 的位置不计）
    alibi = -np.abs(distance)[np.newaxis, :, :] * slopes[:, np.newaxis, np.newaxis]
    return alibi  # (H, S, S)


def softmax(x: np.ndarray, axis=-1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)


def attention_with_alibi(Q, K, V, alibi_bias):
    """
    Q, K, V: (batch, heads, seq, d_head)
    alibi_bias: (heads, seq, seq)
    """
    d_k = Q.shape[-1]
    scores = Q @ K.swapaxes(-2, -1) / np.sqrt(d_k)
    scores = scores + alibi_bias[np.newaxis, :, :, :]  # broadcast batch
    attn = softmax(scores, axis=-1)
    return attn @ V


if __name__ == "__main__":
    np.random.seed(42)
    num_heads, seq_len, d_head = 8, 16, 32
    batch = 2

    slopes = get_alibi_slopes(num_heads)
    assert len(slopes) == num_heads
    # 斜率应该递增（惩罚从小到大）
    assert all(slopes[i] < slopes[i+1] for i in range(len(slopes)-1))

    alibi_bias = compute_alibi_bias(num_heads, seq_len)
    assert alibi_bias.shape == (num_heads, seq_len, seq_len)
    # 对角线（距离为0）偏置为 0
    assert np.all(alibi_bias[:, range(seq_len), range(seq_len)] == 0)

    Q = np.random.randn(batch, num_heads, seq_len, d_head)
    K = np.random.randn(batch, num_heads, seq_len, d_head)
    V = np.random.randn(batch, num_heads, seq_len, d_head)
    out = attention_with_alibi(Q, K, V, alibi_bias)
    assert out.shape == (batch, num_heads, seq_len, d_head)

    print("All tests passed.")
