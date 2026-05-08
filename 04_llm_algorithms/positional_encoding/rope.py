"""
题目：RoPE（旋转位置编码）
难度：Hard | 高频出现：字节/阿里/百度（LLM岗）
标签：RoPE、位置编码、LLaMA、Transformer


题目描述
---------
手写实现旋转位置编码（Rotary Position Embedding, RoPE），这是 LLaMA 等现代 LLM 采用的位置编码方案。
RoPE 通过对 Q、K 向量施加基于位置的旋转变换，使注意力分数天然编码相对位置信息，
相比绝对位置编码具有更好的外推性（推理时处理比训练时更长的序列）。

关键公式：
  对于位置 m 的向量 x，RoPE 变换为：RoPE(x, m) = x ⊗ e^(imθ)
  其中 θ_j = 1/10000^(2j/d)（与 Transformer 原始位置编码相同的频率基）

输入/输出
----------
输入: x（B, L, H, d），positions（L）
输出: rotated_x（B, L, H, d）

约束
------
- 旋转仅应用于 Q、K，不应用于 V
- 支持向量化实现（complex multiplication trick）

TL;DR（30秒速览）
- 将绝对位置信息以旋转矩阵形式编码到 Q/K，相对位置自然出现在 QKᵀ 中
- 核心操作：把向量每两个维度视为复数，乘以旋转因子 e^{imθ}
- 优势：外推性好，支持比训练长度更长的序列（配合 YaRN/LongRoPE）

详细解析
---------
RoPE 核心：
  position m 的旋转角度：θ_i = m / 10000^{2i/d}（与 Sinusoidal 相同基础）
  对 q 的第 2i, 2i+1 维度：
    q'_{2i}   = q_{2i} * cos(mθ_i) - q_{2i+1} * sin(mθ_i)
    q'_{2i+1} = q_{2i} * sin(mθ_i) + q_{2i+1} * cos(mθ_i)

  q'ᵀk' 只依赖位置差 (m - n)，即编码了相对位置

复数形式（更优雅）：
  将 (q_{2i}, q_{2i+1}) 看作复数 q_{2i} + iq_{2i+1}
  乘以 e^{imθ} 即为旋转
"""

import numpy as np


def precompute_freqs(d: int, max_seq_len: int, base: float = 10000.0):
    """
    预计算旋转频率
    d: head dimension (必须为偶数)
    返回: freqs_cos, freqs_sin，shape 均为 (max_seq_len, d//2)
    """
    theta = 1.0 / (base ** (np.arange(0, d, 2) / d))  # (d//2,)
    positions = np.arange(max_seq_len)                  # (seq_len,)
    freqs = np.outer(positions, theta)                   # (seq_len, d//2)
    return np.cos(freqs), np.sin(freqs)


def apply_rope(x: np.ndarray, cos: np.ndarray, sin: np.ndarray) -> np.ndarray:
    """
    x: (batch, seq_len, num_heads, d_head)
    cos, sin: (seq_len, d_head//2)
    """
    seq_len, d_half = cos.shape
    # 拆分奇偶维度
    x1 = x[..., :d_half]   # 偶数维
    x2 = x[..., d_half:]   # 奇数维
    # 旋转：实部/虚部分别计算
    cos = cos[np.newaxis, :seq_len, np.newaxis, :]  # (1, S, 1, d/2) broadcast
    sin = sin[np.newaxis, :seq_len, np.newaxis, :]
    x_rotated = np.concatenate([
        x1 * cos - x2 * sin,
        x1 * sin + x2 * cos,
    ], axis=-1)
    return x_rotated


def apply_rope_interleaved(x: np.ndarray, cos: np.ndarray, sin: np.ndarray) -> np.ndarray:
    """
    交错版 RoPE（GPT-NeoX 风格）：(x0, x1, x2, x3) → 对 (x0,x1), (x2,x3) 分别旋转
    """
    def rotate_half(x):
        x1, x2 = x[..., ::2], x[..., 1::2]
        return np.stack([-x2, x1], axis=-1).reshape(x.shape)

    cos = cos[np.newaxis, :, np.newaxis, :]
    sin = sin[np.newaxis, :, np.newaxis, :]
    cos_full = np.repeat(cos, 2, axis=-1)
    sin_full = np.repeat(sin, 2, axis=-1)
    return x * cos_full + rotate_half(x) * sin_full


if __name__ == "__main__":
    np.random.seed(42)
    batch, seq_len, num_heads, d_head = 2, 8, 4, 16

    cos, sin = precompute_freqs(d_head, max_seq_len=128)
    Q = np.random.randn(batch, seq_len, num_heads, d_head)
    K = np.random.randn(batch, seq_len, num_heads, d_head)

    Q_rope = apply_rope(Q, cos, sin)
    K_rope = apply_rope(K, cos, sin)

    assert Q_rope.shape == Q.shape

    # 验证 RoPE 不改变向量模长（旋转保范性）
    q_norm = np.linalg.norm(Q, axis=-1)
    q_rope_norm = np.linalg.norm(Q_rope, axis=-1)
    assert np.allclose(q_norm, q_rope_norm, atol=1e-5), "RoPE should preserve norm"

    print("All tests passed.")
