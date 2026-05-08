"""
题目：手写 Softmax + 交叉熵损失（含反向传播）
难度：Medium | 高频出现：字节/阿里/百度
标签：Softmax、交叉熵、反向传播


题目描述
---------
手写实现 Softmax 函数和交叉熵损失（Cross-Entropy Loss），并推导其梯度。
Softmax 将 logits 转换为概率分布；交叉熵衡量预测分布与真实分布的差距。

关键点：
  - 数值稳定性：减去最大值防止指数溢出，即 softmax(x) = softmax(x - max(x))
  - 梯度：Softmax + CrossEntropy 合并后梯度简化为 (probs - y_onehot) / N

输入/输出
----------
输入: logits（形状 [N, C]），labels（形状 [N]，整数类别索引）
输出: loss（标量），dlogits（梯度，形状 [N, C]）

约束
------
- N：batch size，C：类别数
- 掌握为什么 Softmax+CE 梯度比单独推导更简洁

TL;DR（30秒速览）
- Softmax: p_i = exp(x_i) / Σexp(x_j)，需减去最大值防数值溢出
- 交叉熵: L = -Σ y_i * log(p_i)
- 合并梯度: dL/dx_i = p_i - y_i（极其简洁，面试高频考点）

详细解析
---------
数值稳定 Softmax：
  softmax(x) = softmax(x - max(x))，不改变结果，避免 exp 溢出

Softmax + 交叉熵合并的反向传播推导：
  L = -log(p_y)  (y 是真实类别)
  dL/dx_i = p_i - y_i  (y_i=1 if i==y else 0)
  这个结论非常优雅，面试必须能推导
"""

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    """数值稳定的 Softmax（支持 batch）"""
    x = x - x.max(axis=-1, keepdims=True)  # 防止 exp 溢出
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=-1, keepdims=True)


def cross_entropy_loss(probs: np.ndarray, labels: np.ndarray) -> float:
    """
    probs: (batch, num_classes) softmax 输出
    labels: (batch,) 整数类别标签
    """
    batch_size = probs.shape[0]
    log_probs = -np.log(probs[np.arange(batch_size), labels] + 1e-12)
    return log_probs.mean()


def softmax_cross_entropy_backward(probs: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Softmax + CrossEntropy 合并反向传播
    返回对 logits 的梯度：dL/dx = (p - y) / batch_size
    """
    batch_size = probs.shape[0]
    grad = probs.copy()
    grad[np.arange(batch_size), labels] -= 1
    return grad / batch_size


class SoftmaxCrossEntropyLayer:
    """完整的前向+反向"""
    def forward(self, logits: np.ndarray, labels: np.ndarray) -> float:
        self.probs = softmax(logits)
        self.labels = labels
        return cross_entropy_loss(self.probs, labels)

    def backward(self) -> np.ndarray:
        return softmax_cross_entropy_backward(self.probs, self.labels)


if __name__ == "__main__":
    np.random.seed(42)

    # Softmax 测试
    x = np.array([[2.0, 1.0, 0.1]])
    p = softmax(x)
    assert abs(p.sum() - 1.0) < 1e-6
    assert p[0, 0] > p[0, 1] > p[0, 2]  # 单调性

    # 数值溢出测试
    x_large = np.array([[1000.0, 1001.0, 1002.0]])
    p_large = softmax(x_large)
    assert not np.any(np.isnan(p_large))

    # 交叉熵测试：完美预测时损失接近0
    probs_perfect = np.array([[0.001, 0.001, 0.998]])
    loss = cross_entropy_loss(probs_perfect, np.array([2]))
    assert loss < 0.01, f"Expected near 0, got {loss}"

    # 反向传播梯度测试
    logits = np.random.randn(4, 3)
    labels = np.array([0, 1, 2, 1])
    layer = SoftmaxCrossEntropyLayer()
    loss = layer.forward(logits, labels)
    grad = layer.backward()
    assert grad.shape == logits.shape
    print(f"Loss: {loss:.4f}")
    print("All tests passed.")
