"""
题目：手写 LayerNorm（层归一化）
难度：Medium | 高频出现：字节/阿里/百度（LLM相关岗）
标签：归一化、Transformer、深度学习


题目描述
---------
手写实现 Layer Normalization（层归一化）的前向传播和反向传播。
与 BatchNorm 不同，LayerNorm 在特征维度（而非 batch 维度）进行归一化，
不依赖 batch size，适用于 NLP 和 Transformer。

前向公式：
  μ = mean(x, axis=-1)，σ² = var(x, axis=-1)
  x̂ = (x - μ) / sqrt(σ² + ε)，y = γ * x̂ + β

输入/输出
----------
输入: x（形状 [N, D]），gamma（形状 [D]），beta（形状 [D]）
输出: out（形状 [N, D]），cache（用于反向传播）

约束
------
- 掌握 LayerNorm vs BatchNorm 在维度和使用场景上的核心区别

TL;DR（30秒速览）
- 对每个样本的特征维度归一化（BN 对每个特征的 batch 维度归一化）
- LLM 中几乎全用 LayerNorm（不依赖 batch size，适合自回归推理）
- 公式：y = γ × (x - μ) / √(σ² + ε) + β

详细解析
---------
BatchNorm vs LayerNorm：
  - BN：对 batch 维度统计，batch_size=1 时退化（推理时用移动均值）
  - LN：对单个样本的特征维度统计，不受 batch_size 影响
  - Transformer/LLM 全用 LN；CV 模型多用 BN

RMSNorm（LLaMA 使用）：
  省去减均值步骤，只做 RMS 缩放，计算更快
  y = x / RMS(x) × γ，其中 RMS(x) = sqrt(mean(x²) + ε)
"""

import numpy as np


class LayerNorm:
    def __init__(self, normalized_shape: int, eps: float = 1e-5):
        self.eps = eps
        self.gamma = np.ones(normalized_shape)   # 可学习缩放
        self.beta = np.zeros(normalized_shape)   # 可学习偏移
        self.cache = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        """x: (batch, seq_len, hidden) 或 (batch, hidden)"""
        mu = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        x_norm = (x - mu) / np.sqrt(var + self.eps)
        out = self.gamma * x_norm + self.beta
        self.cache = (x, x_norm, mu, var)
        return out

    def backward(self, dout: np.ndarray):
        x, x_norm, mu, var = self.cache
        N = x.shape[-1]

        dgamma = (dout * x_norm).sum(axis=tuple(range(dout.ndim - 1)))
        dbeta = dout.sum(axis=tuple(range(dout.ndim - 1)))

        dx_norm = dout * self.gamma
        dvar = (dx_norm * (x - mu) * -0.5 * (var + self.eps) ** (-1.5)).sum(axis=-1, keepdims=True)
        dmu = (dx_norm * -1 / np.sqrt(var + self.eps)).sum(axis=-1, keepdims=True)

        dx = dx_norm / np.sqrt(var + self.eps) + dvar * 2 * (x - mu) / N + dmu / N
        return dx, dgamma, dbeta


class RMSNorm:
    """LLaMA 使用的 RMSNorm，无偏置，无减均值"""
    def __init__(self, d: int, eps: float = 1e-6):
        self.eps = eps
        self.weight = np.ones(d)

    def forward(self, x: np.ndarray) -> np.ndarray:
        rms = np.sqrt((x ** 2).mean(axis=-1, keepdims=True) + self.eps)
        return self.weight * x / rms


if __name__ == "__main__":
    np.random.seed(42)
    batch, seq_len, hidden = 2, 4, 8

    ln = LayerNorm(hidden)
    x = np.random.randn(batch, seq_len, hidden)
    out = ln.forward(x)

    # 归一化后每个位置均值接近0，方差接近1
    mean_out = out.mean(axis=-1)
    assert np.allclose(mean_out, 0, atol=1e-5), f"Mean not zero: {mean_out}"

    # RMSNorm 测试
    rms_norm = RMSNorm(hidden)
    out_rms = rms_norm.forward(x)
    assert out_rms.shape == x.shape

    # 验证与 PyTorch 结果一致（如有torch）
    try:
        import torch
        import torch.nn as nn
        x_torch = torch.tensor(x, dtype=torch.float32)
        ln_torch = nn.LayerNorm(hidden)
        out_torch = ln_torch(x_torch).detach().numpy()
        assert np.allclose(out, out_torch, atol=1e-5)
        print("Matches PyTorch LayerNorm!")
    except ImportError:
        print("PyTorch not available, skipping comparison")

    print("All tests passed.")
