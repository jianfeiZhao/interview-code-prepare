"""
题目：手写 Dropout
难度：Easy | 高频出现：字节/阿里
标签：正则化、Dropout、深度学习


题目描述
---------
手写实现 Dropout 正则化层的前向传播和反向传播。
训练时随机将部分神经元输出置零（以概率 p），并对剩余输出缩放（inverted dropout）。
推理时关闭 Dropout（所有神经元正常工作）。

前向（训练）：
  mask = (random > p)，out = x * mask / (1-p)  # inverted dropout

前向（推理）：
  out = x  # 不做任何变换

反向：
  dx = dout * mask / (1-p)

输入/输出
----------
输入: x（任意形状），p（dropout 概率，0~1），training（是否训练模式）
输出: out（同 x 形状），cache（mask，用于反向）

约束
------
- inverted dropout 使推理时无需额外缩放
- 掌握 Dropout 的正则化原理：减少神经元间的共适应

TL;DR（30秒速览）
- 训练：随机置零 p 比例的神经元，剩余神经元除以 (1-p) 保持期望不变（Inverted Dropout）
- 推理：直接通过，不做任何处理
- 梯度：与前向 mask 相同位置置零，其余除以 (1-p)

详细解析
---------
Inverted Dropout（现代标准做法）：
  训练：mask = (rand > p); x_out = x * mask / (1-p)
  推理：直接返回 x（因为训练时已缩放，推理无需调整）

Non-inverted（旧版）：
  训练：x_out = x * mask
  推理：x_out = x * (1-p)  ← 需要在推理时缩放

dropout_rate 含义：
  p = 0.5 意味着 50% 神经元被置零（dropout rate）
  keep_prob = 1 - p = 0.5
"""

import numpy as np


class Dropout:
    def __init__(self, p: float = 0.5):
        """p: dropout rate（被置零的概率）"""
        assert 0 <= p < 1
        self.p = p
        self.mask = None
        self.training = True

    def forward(self, x: np.ndarray) -> np.ndarray:
        if not self.training or self.p == 0:
            return x
        keep_prob = 1 - self.p
        self.mask = (np.random.rand(*x.shape) > self.p).astype(float)
        return x * self.mask / keep_prob  # Inverted Dropout

    def backward(self, dout: np.ndarray) -> np.ndarray:
        if not self.training or self.p == 0:
            return dout
        keep_prob = 1 - self.p
        return dout * self.mask / keep_prob

    def train(self): self.training = True
    def eval(self): self.training = False


if __name__ == "__main__":
    np.random.seed(42)
    x = np.ones((1000, 100))

    dropout = Dropout(p=0.5)

    # 训练模式：约50%被置零，但期望值保持不变
    out = dropout.forward(x)
    zero_ratio = (out == 0).mean()
    assert abs(zero_ratio - 0.5) < 0.05, f"Drop rate off: {zero_ratio}"
    assert abs(out.mean() - 1.0) < 0.05, f"Mean changed: {out.mean()}"

    # 推理模式：直接通过
    dropout.eval()
    out_eval = dropout.forward(x)
    assert np.allclose(out_eval, x)

    # 梯度测试
    dropout.train()
    out = dropout.forward(x)
    dout = np.ones_like(out)
    dx = dropout.backward(dout)
    assert dx.shape == x.shape

    print("All tests passed.")
