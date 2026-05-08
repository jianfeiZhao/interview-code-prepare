"""
题目：Multi-Head Attention（多头注意力）
难度：Hard | 高频出现：字节/阿里/百度（LLM岗）
标签：MHA、Transformer、注意力机制


题目描述
---------
手写实现多头注意力机制（Multi-Head Attention），这是 Transformer 的标志性设计。
将 Q、K、V 分别投影到 h 个子空间，并行执行注意力，最后拼接后再投影。
多头允许模型同时关注不同位置的不同表示子空间中的信息。

公式：
  head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
  MultiHead(Q,K,V) = Concat(head_1,...,head_h) W^O

输入/输出
----------
输入: Q,K,V（形状 [B, L, d_model]），mask（可选）
输出: output（[B, L, d_model]），attn_weights（[B, h, L_q, L_k]）

约束
------
- d_k = d_v = d_model / h（头维度）
- 实际实现通常将 batch 和 head 维度合并以提高效率

TL;DR（30秒速览）
- H个头并行计算 Attention，拼接后投影，捕获不同子空间信息
- 每头维度：d_head = d_model / num_heads
- 实现技巧：reshape + transpose 合并 batch 和 head 维度，一次矩阵乘法

详细解析
---------
Multi-Head Attention：
  1. 线性投影：Q = X @ Wq, K = X @ Wk, V = X @ Wv（每头有独立 W）
  2. 分头：reshape 到 (batch, heads, seq, d_head)
  3. 各头独立计算 Attention
  4. 拼接：concat → (batch, seq, d_model)
  5. 输出投影：output = concat @ Wo

为什么多头？
  不同头可以关注不同类型的关系（语法、语义、位置等）
  类似 CNN 的多通道
"""

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)


class MultiHeadAttention:
    def __init__(self, d_model: int, num_heads: int):
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads

        # 初始化权重（Xavier）
        scale = np.sqrt(2.0 / d_model)
        self.Wq = np.random.randn(d_model, d_model) * scale
        self.Wk = np.random.randn(d_model, d_model) * scale
        self.Wv = np.random.randn(d_model, d_model) * scale
        self.Wo = np.random.randn(d_model, d_model) * scale

    def forward(self, Q: np.ndarray, K: np.ndarray, V: np.ndarray,
                mask: np.ndarray = None) -> np.ndarray:
        """
        Q, K, V: (batch, seq_len, d_model)
        返回: (batch, seq_len, d_model)
        """
        batch, seq_q = Q.shape[:2]
        seq_k = K.shape[1]

        # 线性投影
        Q_proj = Q @ self.Wq  # (B, seq, d_model)
        K_proj = K @ self.Wk
        V_proj = V @ self.Wv

        # 分头：(B, seq, d_model) → (B, heads, seq, d_head)
        def split_heads(x, seq_len):
            x = x.reshape(batch, seq_len, self.num_heads, self.d_head)
            return x.transpose(0, 2, 1, 3)  # (B, H, S, d_head)

        Q_heads = split_heads(Q_proj, seq_q)
        K_heads = split_heads(K_proj, seq_k)
        V_heads = split_heads(V_proj, seq_k)

        # Scaled Dot-Product Attention（所有头并行）
        scores = Q_heads @ K_heads.swapaxes(-2, -1) / np.sqrt(self.d_head)
        if mask is not None:
            scores = scores + mask * -1e9
        attn_weights = softmax(scores, axis=-1)
        context = attn_weights @ V_heads  # (B, H, seq_q, d_head)

        # 合并头：(B, H, seq, d_head) → (B, seq, d_model)
        context = context.transpose(0, 2, 1, 3).reshape(batch, seq_q, self.d_model)

        # 输出投影
        return context @ self.Wo


if __name__ == "__main__":
    np.random.seed(42)
    batch, seq_len, d_model, num_heads = 2, 6, 64, 8

    mha = MultiHeadAttention(d_model, num_heads)
    X = np.random.randn(batch, seq_len, d_model)
    out = mha.forward(X, X, X)

    assert out.shape == (batch, seq_len, d_model), f"Shape mismatch: {out.shape}"

    # 因果掩码测试
    from scaled_dot_product_attention import make_causal_mask
    mask = make_causal_mask(seq_len)[np.newaxis, np.newaxis, :, :]  # (1,1,S,S) broadcast
    out_causal = mha.forward(X, X, X, mask=mask)
    assert out_causal.shape == (batch, seq_len, d_model)

    print("All tests passed.")
