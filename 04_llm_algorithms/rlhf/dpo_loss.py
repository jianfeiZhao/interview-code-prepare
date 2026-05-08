"""
题目：DPO Loss（直接偏好优化）
难度：Hard | 高频出现：字节/阿里（RLHF岗）
标签：DPO、RLHF、偏好学习

题目描述
---------
DPO（Direct Preference Optimization）是 RLHF 的简化替代方案。
传统 RLHF 需要先训练奖励模型（RM），再用 PPO 优化策略，流程复杂（4 个模型并行）。
DPO 通过数学推导，将奖励模型隐式嵌入策略目标，直接用人类偏好数据
(prompt x, chosen y_w, rejected y_l) 优化语言模型，无需显式 RM。

损失函数形式：
  L_DPO = -E[ log σ( β × (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)) ) ]

其中 β 为 KL 惩罚系数，隐式奖励 = β × log(π(y)/π_ref(y))。

示例/场景
---------
输入：batch 条偏好对，每条包含策略模型和参考模型对 chosen/rejected 的 log 概率（各 shape (batch,)）
输出：DPO loss（标量）、每条样本的隐式奖励、chosen 的胜率（accuracy）
附加：IPO（Identity Preference Optimization）作为 DPO 的数值稳定改进变体

关键概念
---------
- Bradley-Terry 模型：对比偏好的概率建模基础，P(y_w > y_l) = σ(r_w - r_l)
- 隐式奖励：β × log(π(y|x) / π_ref(y|x))，无需独立 RM 网络
- β（KL 系数）：控制策略偏离参考模型的强度；β 越大，越保守（靠近 π_ref）
- DPO vs PPO：DPO 只需策略网络 + 参考策略（frozen），PPO 额外需要 RM + 价值网络
- 数值稳定性：log σ(x) 需分正负区间分别计算，避免 exp 溢出

TL;DR（30秒速览）
- DPO：无需奖励模型，直接从人类偏好数据 (x, y_w, y_l) 训练
- L_DPO = -E[log σ(β × (log π(y_w)/π_ref(y_w) - log π(y_l)/π_ref(y_l)))]
- β 控制偏离参考策略的强度，β 越大越保守

详细解析
---------
DPO 推导：
  PPO 的奖励 = RM(y) - β × log(π(y)/π_ref(y))
  在最优策略下，RM(y) = β × log(π*(y)/π_ref(y)) + Z(x)
  代入 BT 模型（Bradley-Terry 偏好模型）得到 DPO Loss

DPO vs PPO：
  PPO：需要奖励模型 + 价值网络 + PPO 训练，4个模型，复杂
  DPO：只需一个策略网络，无需 RM，简单稳定
  DPO 代价：需要完整的参考策略 π_ref 存在内存中（或近似）

数据格式：(prompt, chosen_response, rejected_response)
"""

import numpy as np


def dpo_loss(
    log_probs_chosen_policy: np.ndarray,
    log_probs_rejected_policy: np.ndarray,
    log_probs_chosen_ref: np.ndarray,
    log_probs_rejected_ref: np.ndarray,
    beta: float = 0.1,
) -> tuple:
    """
    DPO Loss

    Args:
        log_probs_chosen_policy:    策略模型对 chosen 的 log 概率，shape (batch,)
        log_probs_rejected_policy:  策略模型对 rejected 的 log 概率，shape (batch,)
        log_probs_chosen_ref:       参考模型对 chosen 的 log 概率，shape (batch,)
        log_probs_rejected_ref:     参考模型对 rejected 的 log 概率，shape (batch,)
        beta:                       KL 惩罚系数

    Returns:
        (loss, reward_chosen, reward_rejected, accuracy)
    """
    # 隐式奖励 = β × log(π(y)/π_ref(y))
    reward_chosen = beta * (log_probs_chosen_policy - log_probs_chosen_ref)
    reward_rejected = beta * (log_probs_rejected_policy - log_probs_rejected_ref)

    # DPO Loss = -log σ(reward_chosen - reward_rejected)
    logits = reward_chosen - reward_rejected  # (batch,)
    loss = -log_sigmoid(logits).mean()

    # 胜率（chosen reward > rejected reward 的比例）
    accuracy = (reward_chosen > reward_rejected).mean()

    return loss, reward_chosen, reward_rejected, accuracy


def log_sigmoid(x: np.ndarray) -> np.ndarray:
    """数值稳定的 log(sigmoid(x))"""
    return np.where(
        x >= 0,
        -np.log1p(np.exp(-x)),
        x - np.log1p(np.exp(x))
    )


def ipo_loss(
    log_probs_chosen_policy: np.ndarray,
    log_probs_rejected_policy: np.ndarray,
    log_probs_chosen_ref: np.ndarray,
    log_probs_rejected_ref: np.ndarray,
    tau: float = 0.1,
) -> np.ndarray:
    """
    IPO（Identity Preference Optimization）Loss，DPO 的改进
    L_IPO = (log(π(y_w)/π_ref(y_w)) - log(π(y_l)/π_ref(y_l)) - 1/(2τ))²
    """
    h_w = log_probs_chosen_policy - log_probs_chosen_ref
    h_l = log_probs_rejected_policy - log_probs_rejected_ref
    return ((h_w - h_l - 1 / (2 * tau)) ** 2).mean()


if __name__ == "__main__":
    np.random.seed(42)
    batch = 8

    # 模拟：策略模型对 chosen 比 rejected 概率更高
    log_probs_chosen_policy   = np.random.randn(batch) * 0.5 - 1.0
    log_probs_rejected_policy = np.random.randn(batch) * 0.5 - 2.0  # 更低
    log_probs_chosen_ref      = np.random.randn(batch) * 0.5 - 1.5
    log_probs_rejected_ref    = np.random.randn(batch) * 0.5 - 1.5

    loss, r_w, r_l, acc = dpo_loss(
        log_probs_chosen_policy,
        log_probs_rejected_policy,
        log_probs_chosen_ref,
        log_probs_rejected_ref,
    )
    print(f"DPO Loss: {loss:.4f}")
    print(f"Reward chosen: {r_w.mean():.4f}, rejected: {r_l.mean():.4f}")
    print(f"Accuracy: {acc:.2%}")

    assert loss > 0, "DPO loss should be positive"
    assert r_w.shape == (batch,)

    # IPO
    ipo = ipo_loss(log_probs_chosen_policy, log_probs_rejected_policy,
                   log_probs_chosen_ref, log_probs_rejected_ref)
    assert ipo >= 0

    print("All tests passed.")
