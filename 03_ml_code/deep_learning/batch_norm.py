"""
题目：手写 BatchNorm（批归一化）前向 + 反向
难度：Hard | 高频出现：字节/阿里/百度
标签：BatchNorm、归一化、反向传播


题目描述
---------
手写实现 Batch Normalization（批归一化）的前向传播（训练/推理模式）和反向传播。
BatchNorm 通过对每个 batch 内的特征进行归一化，加速训练、允许更大学习率、
有一定正则化效果，是深度网络的标配组件。

前向（训练）：
  对每个特征维度，计算 batch 均值/方差，归一化后缩放：y = γ*x̂ + β

前向（推理）：
  使用训练时的指数移动平均（running_mean/var），不依赖当前 batch

输入/输出
----------
输入: x（[N, D]），gamma/beta（[D]）
输出: out（[N, D]）；训练时返回 cache 供反向传播使用

约束
------
- 推理时必须使用 running_mean/var，而不是当前 batch 统计

TL;DR（30秒速览）
- 训练：对每个特征在 batch 维度求均值/方差，归一化后缩放
- 推理：用训练时的移动均值/方差（不再依赖当前batch）
- 梯度公式复杂，记住核心：dγ=Σdout*x̂, dβ=Σdout，dx 涉及三项

详细解析
---------
BN 前向（训练模式）：
  μ = mean(x, axis=0)
  σ² = var(x, axis=0)
  x̂ = (x - μ) / sqrt(σ² + ε)
  y = γ * x̂ + β

移动统计（推理时使用）：
  running_mean = momentum * running_mean + (1-momentum) * batch_mean
  running_var  = momentum * running_var  + (1-momentum) * batch_var
"""

import numpy as np


class BatchNorm1d:
    def __init__(self, num_features: int, eps: float = 1e-5, momentum: float = 0.1):
        self.eps = eps
        self.momentum = momentum
        self.gamma = np.ones(num_features)
        self.beta = np.zeros(num_features)
        self.running_mean = np.zeros(num_features)
        self.running_var = np.ones(num_features)
        self.training = True
        self.cache = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        if self.training:
            mu = x.mean(axis=0)
            var = x.var(axis=0)
            x_norm = (x - mu) / np.sqrt(var + self.eps)
            out = self.gamma * x_norm + self.beta
            # 更新移动统计
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mu
            self.running_var  = (1 - self.momentum) * self.running_var  + self.momentum * var
            self.cache = (x, x_norm, mu, var)
        else:
            x_norm = (x - self.running_mean) / np.sqrt(self.running_var + self.eps)
            out = self.gamma * x_norm + self.beta
        return out

    def backward(self, dout: np.ndarray):
        x, x_norm, mu, var = self.cache
        N = x.shape[0]

        dgamma = (dout * x_norm).sum(axis=0)
        dbeta = dout.sum(axis=0)

        dx_norm = dout * self.gamma
        dvar = (dx_norm * (x - mu) * -0.5 * (var + self.eps) ** (-1.5)).sum(axis=0)
        dmu = (dx_norm / (-np.sqrt(var + self.eps))).sum(axis=0) + dvar * (-2 * (x - mu)).mean(axis=0)
        dx = dx_norm / np.sqrt(var + self.eps) + dvar * 2 * (x - mu) / N + dmu / N

        return dx, dgamma, dbeta

    def train(self): self.training = True
    def eval(self): self.training = False


if __name__ == "__main__":
    np.random.seed(42)
    bn = BatchNorm1d(4)
    x = np.random.randn(8, 4)

    out = bn.forward(x)
    # 训练时输出近似标准化
    assert np.allclose(out.mean(axis=0), np.zeros(4), atol=1e-5)
    assert np.allclose(out.var(axis=0), np.ones(4), atol=1e-5)

    # 梯度计算
    dout = np.random.randn(*out.shape)
    dx, dgamma, dbeta = bn.backward(dout)
    assert dx.shape == x.shape
    assert dgamma.shape == (4,)

    # 推理模式
    bn.eval()
    out_eval = bn.forward(x)
    assert out_eval.shape == x.shape

    # 对比 PyTorch
    try:
        import torch
        import torch.nn as nn
        bn_torch = nn.BatchNorm1d(4)
        bn_torch.weight.data = torch.ones(4)
        bn_torch.bias.data = torch.zeros(4)
        out_torch = bn_torch(torch.tensor(x, dtype=torch.float32)).detach().numpy()
        assert np.allclose(out, out_torch, atol=1e-5)
        print("Matches PyTorch BatchNorm1d!")
    except ImportError:
        pass

    print("All tests passed.")
