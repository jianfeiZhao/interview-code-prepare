"""
题目：PPO Clip Loss（近端策略优化裁剪目标）
难度：Hard | 高频出现：字节/阿里（RLHF岗）
标签：PPO、RLHF、强化学习、策略梯度


题目描述
---------
手写实现 PPO（Proximal Policy Optimization）的 Clip 损失函数，
这是 RLHF（人类反馈强化学习）中训练语言模型的核心算法（InstructGPT/ChatGPT 使用）。

PPO-Clip 目标函数：
  L_CLIP = E[min(r_t * A_t, clip(r_t, 1-ε, 1+ε) * A_t)]
  其中 r_t = π_θ(a|s) / π_θ_old(a|s) 为概率比，A_t 为优势函数，ε 为裁剪范围

关键设计：
  - clip 操作限制策略更新幅度，避免训练不稳定
  - 优势正时不允许概率比 > 1+ε；优势负时不允许概率比 < 1-ε

输入/输出
----------
输入: log_probs_new, log_probs_old（形状 [B, T]），advantages（[B, T]），ε
输出: ppo_loss（标量），clip_fraction（被裁剪的比例，用于监控训练）

约束
------
- 结合 Value Loss 和 Entropy Bonus 形成完整 PPO 目标

TL;DR（30秒速览）
- PPO = 策略梯度 + 重要性采样比率 + Clip 约束（防止更新过大）
- ratio = π_new(a|s) / π_old(a|s)（新旧策略的概率比）
- L_CLIP = E[min(ratio × A, clip(ratio, 1-ε, 1+ε) × A)]
- ε 通常取 0.1~0.2，限制单次更新幅度

详细解析
---------
为什么需要 PPO？
  普通策略梯度（REINFORCE）步长难以控制，更新过大会破坏策略
  TRPO 通过 KL 散度约束，但二阶优化复杂
  PPO 通过 Clip 近似 TRPO 的约束，实现简单、效果好

PPO 在 RLHF 中的应用：
  1. 训练奖励模型（RM）
  2. 用 PPO 优化 LM：奖励 = RM 打分 - β × KL(π_new || π_ref)
  3. KL 惩罚防止 LM 偏离预训练分布太远

值函数损失：MSE(V(s), returns)
总损失：L = -L_CLIP + c1 * L_VF - c2 * entropy_bonus
"""

import numpy as np


def ppo_clip_loss(
    log_probs_new: np.ndarray,
    log_probs_old: np.ndarray,
    advantages: np.ndarray,
    clip_eps: float = 0.2,
) -> tuple:
    """
    PPO Clip 目标函数

    Args:
        log_probs_new: 新策略的 log 概率，shape (batch,)
        log_probs_old: 旧策略的 log 概率（detach），shape (batch,)
        advantages: 优势函数估计，shape (batch,)
        clip_eps: 裁剪范围 ε

    Returns:
        (loss, ratio, clipped_ratio) — loss 取负号（最大化目标 → 最小化负目标）
    """
    # 重要性采样比率：exp(log π_new - log π_old)
    ratio = np.exp(log_probs_new - log_probs_old)

    # 裁剪比率
    clipped_ratio = np.clip(ratio, 1 - clip_eps, 1 + clip_eps)

    # PPO Clip 目标：取未裁剪和裁剪中较小的（保守更新）
    surrogate1 = ratio * advantages
    surrogate2 = clipped_ratio * advantages
    policy_loss = -np.minimum(surrogate1, surrogate2).mean()

    return policy_loss, ratio, clipped_ratio


def compute_advantages_gae(
    rewards: np.ndarray,
    values: np.ndarray,
    dones: np.ndarray,
    gamma: float = 0.99,
    lam: float = 0.95,
) -> np.ndarray:
    """
    GAE（广义优势估计）
    A_t = Σ (γλ)^l × δ_{t+l}，其中 δ_t = r_t + γV_{t+1} - V_t
    """
    T = len(rewards)
    advantages = np.zeros(T)
    last_gae = 0
    for t in reversed(range(T)):
        next_value = values[t + 1] if t + 1 < T else 0
        delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
        last_gae = delta + gamma * lam * (1 - dones[t]) * last_gae
        advantages[t] = last_gae
    return advantages


def kl_divergence_penalty(
    log_probs_new: np.ndarray,
    log_probs_ref: np.ndarray,
    beta: float = 0.1,
) -> float:
    """
    KL 散度惩罚（RLHF 中防止 LM 偏离参考策略）
    KL(π_new || π_ref) = E[log π_new - log π_ref]
    """
    kl = (log_probs_new - log_probs_ref).mean()
    return beta * kl


if __name__ == "__main__":
    np.random.seed(42)
    batch = 16

    log_probs_new = np.random.randn(batch) * 0.1
    log_probs_old = log_probs_new + np.random.randn(batch) * 0.05  # 小变化
    advantages = np.random.randn(batch)
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)  # 归一化

    loss, ratio, clipped = ppo_clip_loss(log_probs_new, log_probs_old, advantages)
    print(f"PPO Loss: {loss:.4f}")
    print(f"Ratio range: [{ratio.min():.4f}, {ratio.max():.4f}]")

    # 验证裁剪生效
    assert clipped.min() >= 1 - 0.2 - 1e-6
    assert clipped.max() <= 1 + 0.2 + 1e-6

    # GAE 测试
    rewards = np.array([1.0, 0.0, 0.0, 1.0, 0.0])
    values = np.array([0.5, 0.3, 0.2, 0.6, 0.1])
    dones = np.zeros(5)
    adv = compute_advantages_gae(rewards, values, dones)
    assert adv.shape == (5,)

    print("All tests passed.")
