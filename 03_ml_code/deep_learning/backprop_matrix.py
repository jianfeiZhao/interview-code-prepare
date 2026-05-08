"""
题目：手写矩阵版反向传播（两层神经网络）
难度：Hard | 高频出现：字节/阿里/百度
标签：反向传播、梯度下降、神经网络


题目描述
---------
手写实现矩阵版本的两层神经网络反向传播（前向+反向+参数更新）。
包含完整的训练循环：前向传播计算 loss，反向传播计算梯度，梯度下降更新参数。

网络结构：X(N,D) → FC1(D,H) → ReLU → FC2(H,C) → Softmax → CrossEntropy Loss

关键梯度公式：
  dW = Xᵀ @ dout，dx = dout @ Wᵀ（矩阵乘法的梯度）
  ReLU 反向：dout * (pre_activation > 0)

输入/输出
----------
输入: X（N,D），y（N，类别索引），隐藏层维度 H，类别数 C
输出: 训练后的参数 W1, b1, W2, b2；预测函数 predict(X)

约束
------
- 矩阵维度检查是反向传播调试的关键

TL;DR（30秒速览）
- 前向：X → FC1 → ReLU → FC2 → Softmax+CE Loss
- 反向：链式法则，从 loss 逐层求梯度
- 核心梯度：dW = Xᵀ @ dout，dX = dout @ Wᵀ

详细解析
---------
链式法则流程（从后往前）：
  dLoss/dlogits = probs - y_onehot（/N）
  dW2 = h1ᵀ @ dlogits
  dh1 = dlogits @ W2ᵀ
  dh1_relu = dh1 * (h1_pre > 0)（ReLU 反向）
  dW1 = Xᵀ @ dh1_relu
  db1 = dh1_relu.sum(axis=0)

矩阵维度检查（非常重要）：
  X: (N, D)   W1: (D, H)   W2: (H, C)
  dW1: (D, H) = Xᵀ(D,N) @ dh1_relu(N,H)
"""

import numpy as np


class TwoLayerNet:
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, lr: float = 0.01):
        self.lr = lr
        self.params = {
            'W1': np.random.randn(input_dim, hidden_dim) * 0.01,
            'b1': np.zeros(hidden_dim),
            'W2': np.random.randn(hidden_dim, output_dim) * 0.01,
            'b2': np.zeros(output_dim),
        }
        self.cache = {}

    def forward(self, X: np.ndarray) -> np.ndarray:
        W1, b1, W2, b2 = self.params['W1'], self.params['b1'], self.params['W2'], self.params['b2']
        h1_pre = X @ W1 + b1
        h1 = np.maximum(0, h1_pre)           # ReLU
        logits = h1 @ W2 + b2
        # Softmax（数值稳定）
        logits -= logits.max(axis=1, keepdims=True)
        exp_logits = np.exp(logits)
        probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)

        self.cache = {'X': X, 'h1_pre': h1_pre, 'h1': h1, 'probs': probs}
        return probs

    def loss(self, probs: np.ndarray, labels: np.ndarray) -> float:
        N = probs.shape[0]
        log_probs = -np.log(probs[np.arange(N), labels] + 1e-12)
        return log_probs.mean()

    def backward(self, labels: np.ndarray):
        X, h1_pre, h1, probs = self.cache['X'], self.cache['h1_pre'], self.cache['h1'], self.cache['probs']
        N = X.shape[0]
        W2 = self.params['W2']

        # Softmax+CE 合并梯度
        dlogits = probs.copy()
        dlogits[np.arange(N), labels] -= 1
        dlogits /= N

        # W2, b2 梯度
        dW2 = h1.T @ dlogits              # (H, C)
        db2 = dlogits.sum(axis=0)          # (C,)

        # 传回 h1
        dh1 = dlogits @ W2.T              # (N, H)
        # ReLU 反向
        dh1[h1_pre <= 0] = 0

        # W1, b1 梯度
        dW1 = X.T @ dh1                   # (D, H)
        db1 = dh1.sum(axis=0)             # (H,)

        grads = {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2}
        return grads

    def step(self, grads: dict):
        for key in self.params:
            self.params[key] -= self.lr * grads[key]

    def train_step(self, X: np.ndarray, labels: np.ndarray):
        probs = self.forward(X)
        loss = self.loss(probs, labels)
        grads = self.backward(labels)
        self.step(grads)
        return loss


if __name__ == "__main__":
    np.random.seed(42)
    N, D, H, C = 100, 4, 16, 3
    X = np.random.randn(N, D)
    y = np.random.randint(0, C, N)

    net = TwoLayerNet(D, H, C, lr=0.1)
    losses = []
    for _ in range(200):
        loss = net.train_step(X, y)
        losses.append(loss)

    # 训练后 loss 应该下降
    assert losses[-1] < losses[0], f"Loss did not decrease: {losses[0]:.4f} -> {losses[-1]:.4f}"
    print(f"Loss: {losses[0]:.4f} -> {losses[-1]:.4f}")
    print("All tests passed.")
