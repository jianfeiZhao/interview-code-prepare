"""
题目：手写 Adam 优化器
难度：Medium | 高频出现：字节/阿里/百度
标签：优化器、Adam、梯度下降


题目描述
---------
手写实现 Adam 优化器（Adaptive Moment Estimation），并与 AdamW 对比。
Adam 结合了 Momentum（一阶矩）和 RMSProp（二阶矩），并通过偏差修正消除初始化偏差。

更新规则：
  m = β₁*m + (1-β₁)*g       # 一阶矩（动量）
  v = β₂*v + (1-β₂)*g²      # 二阶矩（梯度平方的期望）
  m̂ = m/(1-β₁ᵗ)，v̂ = v/(1-β₂ᵗ)  # 偏差修正
  θ = θ - lr * m̂ / (√v̂ + ε)

输入/输出
----------
输入: params（参数列表），grads（梯度列表），lr，β₁，β₂，ε
输出: 更新后的参数

约束
------
- AdamW 将 L2 正则作用于参数而非梯度，避免自适应学习率抵消正则化效果

TL;DR（30秒速览）
- Adam = Momentum（一阶矩）+ RMSProp（二阶矩）+ 偏差修正
- 更新：θ = θ - lr × m̂ / (√v̂ + ε)
- 偏差修正：m̂ = m/(1-β₁ᵗ), v̂ = v/(1-β₂ᵗ)，消除初始零偏置

详细解析
---------
Adam 算法：
  t += 1
  g = gradient
  m = β₁ * m + (1-β₁) * g            # 一阶矩（动量）
  v = β₂ * v + (1-β₂) * g²           # 二阶矩（梯度平方期望）
  m̂ = m / (1 - β₁^t)                 # 偏差修正
  v̂ = v / (1 - β₂^t)                 # 偏差修正
  θ = θ - lr * m̂ / (√v̂ + ε)

典型超参：lr=1e-3, β₁=0.9, β₂=0.999, ε=1e-8

AdamW = Adam + 权重衰减（L2正则直接作用于参数，不通过梯度）
  θ = θ - lr * (m̂ / (√v̂ + ε) + λθ)
"""

import numpy as np


class Adam:
    def __init__(self, lr: float = 1e-3, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = {}  # 一阶矩
        self.v = {}  # 二阶矩

    def step(self, params: dict, grads: dict):
        self.t += 1
        for key in params:
            if key not in self.m:
                self.m[key] = np.zeros_like(params[key])
                self.v[key] = np.zeros_like(params[key])

            g = grads[key]
            self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * g
            self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * g ** 2

            m_hat = self.m[key] / (1 - self.beta1 ** self.t)
            v_hat = self.v[key] / (1 - self.beta2 ** self.t)

            params[key] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


class AdamW(Adam):
    """Adam with Weight Decay"""
    def __init__(self, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=1e-2):
        super().__init__(lr, beta1, beta2, eps)
        self.weight_decay = weight_decay

    def step(self, params: dict, grads: dict):
        # 先做 Adam 更新
        super().step(params, grads)
        # 再做权重衰减（独立于梯度）
        for key in params:
            params[key] -= self.lr * self.weight_decay * params[key]


if __name__ == "__main__":
    np.random.seed(42)
    # 最小化 f(x) = x^2，最优解 x=0
    params = {'x': np.array([5.0])}
    optimizer = Adam(lr=0.1)

    for _ in range(200):
        grads = {'x': 2 * params['x']}  # df/dx = 2x
        optimizer.step(params, grads)

    assert abs(params['x'][0]) < 0.01, f"x should converge to 0, got {params['x'][0]}"
    print(f"Converged to x = {params['x'][0]:.6f}")
    print("All tests passed.")
