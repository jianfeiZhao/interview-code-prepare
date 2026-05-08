"""
题目：手写标量反向传播（自动微分 minigrad）
难度：Hard | 高频出现：字节/阿里
标签：自动微分、反向传播、计算图


题目描述
---------
手写实现标量版本的自动微分（反向传播），理解计算图和链式法则。
通过构建简单的计算图节点（Value 类），实现对任意标量表达式的自动梯度计算。
这是理解深度学习框架（PyTorch autograd）底层原理的关键。

关键概念：
  - 前向传播：按顺序计算每个节点的值
  - 反向传播：通过链式法则从 loss 反向计算每个参数的梯度
  - 拓扑排序：确保反向传播顺序正确

示例
------
x = Value(2.0); y = Value(3.0)
z = x * y + x  # 前向计算 z = 8.0
z.backward()
print(x.grad)  # dz/dx = y + 1 = 4.0
print(y.grad)  # dz/dy = x = 2.0

约束
------
- 掌握加法、乘法、幂次、ReLU、tanh 等操作的梯度推导

TL;DR（30秒速览）
- 每个 Value 存储值、梯度、以及如何对其前驱节点反向传播
- backward() 按拓扑序从 loss 反向传播梯度
- 面试重点：理解链式法则 + 局部梯度相乘

详细解析
---------
计算图节点（Value）：
  - data: 前向值
  - grad: 该节点的梯度（dLoss/d_self）
  - _backward: 局部梯度传播函数（闭包）
  - _prev: 子节点（输入）

拓扑排序后从后往前执行 _backward()
这是 PyTorch autograd 的简化版本（参考 Karpathy 的 micrograd）
"""

import math


class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, power):
        out = Value(self.data ** power, (self,), f'**{power}')
        def _backward():
            self.grad += power * (self.data ** (power - 1)) * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Value(max(0, self.data), (self,), 'ReLU')
        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')
        def _backward():
            self.grad += (1 - t ** 2) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        # 拓扑排序
        topo, visited = [], set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)
    def __truediv__(self, other): return self * other ** -1
    def __radd__(self, other): return self + other
    def __rmul__(self, other): return self * other
    def __repr__(self): return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"


if __name__ == "__main__":
    # 验证：f(x) = (x+2)^2 → f'(x) = 2*(x+2)
    x = Value(3.0)
    f = (x + 2) ** 2
    f.backward()
    assert abs(x.grad - 10.0) < 1e-6, f"Expected 10, got {x.grad}"

    # 简单神经元：z = relu(w1*x1 + w2*x2 + b)
    w1, w2, b = Value(0.5), Value(-0.3), Value(0.1)
    x1, x2 = Value(2.0), Value(1.0)
    z = (w1 * x1 + w2 * x2 + b).relu()
    z.backward()
    print(f"w1.grad={w1.grad:.4f}, w2.grad={w2.grad:.4f}")

    # 验证与数值梯度一致
    eps = 1e-4
    w1_plus = Value(0.5 + eps)
    z_plus = (w1_plus * Value(2.0) + Value(-0.3) * Value(1.0) + Value(0.1)).relu()
    numerical_grad = (z_plus.data - z.data) / eps
    assert abs(w1.grad - numerical_grad) < 1e-3

    print("All tests passed.")
