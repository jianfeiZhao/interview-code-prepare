"""
题目：推测解码（Speculative Decoding）原理与简化实现
难度：Hard | 高频出现：字节/阿里（LLM推理岗）
标签：推测解码、推理加速、拒绝采样


题目描述
---------
手写实现推测解码（Speculative Decoding），这是 LLM 推理加速的重要技术。
使用小型草稿模型（draft model）一次生成多个 token，再由大型目标模型（target model）
并行验证，通过接受/拒绝机制保证输出分布与目标模型一致。

算法流程：
  1. 草稿模型自回归生成 K 个候选 token（γ 步）
  2. 目标模型并行计算这 K 个位置的概率
  3. 逐位比较：若 p_target / p_draft >= uniform(0,1)，则接受；否则拒绝并重采样
  4. 期望加速比 ≈ K * 接受率（接受率越高，加速越明显）

输入/输出
----------
输入: 草稿模型、目标模型、输入 token 序列
输出: 生成的 token 序列（分布等同于目标模型，但速度接近草稿模型）

约束
------
- 接受率越高（草稿模型越好），加速效果越明显
- 保证输出分布严格等同于目标模型（无近似误差）

TL;DR（30秒速览）
- 用小（快）模型生成 K 个 draft token，用大（慢）模型并行验证
- 若 draft token 被大模型接受（概率比），保留；否则拒绝并采样修正 token
- 加速比：无损加速，输出分布与纯大模型相同（理论证明）

详细解析
---------
算法流程：
  1. Draft（小模型）：自回归生成 K 个候选 token：t_1, ..., t_K
  2. Verify（大模型）：并行（一次前向）计算 p_big(·|context, t_1..t_{i-1})
  3. 接受/拒绝：
     对每个位置 i：
       r = p_big(t_i) / p_draft(t_i)
       以 min(1, r) 的概率接受 t_i
       一旦拒绝，从修正分布 max(0, p_big - p_draft) 中采样
  4. 若全部接受，额外采样一个 token

加速来源：
  大模型并行验证 K 个 token（一次前向 ≈ 生成1个token的代价）
  若 draft quality 好，平均接受 α*K 个 token（α 是接受率）
  加速比 ≈ α*K（理论上限为 K）
"""

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max()
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()


def speculative_decode_step(
    draft_probs: np.ndarray,   # (K, vocab)  小模型对每步的概率
    target_probs: np.ndarray,  # (K+1, vocab) 大模型并行计算的概率
    draft_tokens: np.ndarray,  # (K,) 小模型生成的 token id
) -> list:
    """
    推测解码单步

    返回接受的 token 列表（可能包含最终修正 token）
    """
    K = len(draft_tokens)
    accepted_tokens = []

    for i in range(K):
        t = draft_tokens[i]
        p_draft = draft_probs[i, t]
        p_target = target_probs[i, t]

        acceptance_prob = min(1.0, p_target / (p_draft + 1e-10))
        if np.random.random() < acceptance_prob:
            accepted_tokens.append(t)
        else:
            # 拒绝：从修正分布采样
            residual = np.maximum(0, target_probs[i] - draft_probs[i])
            if residual.sum() < 1e-10:
                # 分布完全相同，从 target 直接采样
                corrected = np.random.choice(len(target_probs[i]), p=target_probs[i])
            else:
                residual /= residual.sum()
                corrected = np.random.choice(len(residual), p=residual)
            accepted_tokens.append(corrected)
            return accepted_tokens  # 停止

    # 全部接受，额外从大模型最后一步采样一个 token
    last_token = np.random.choice(len(target_probs[K]), p=target_probs[K])
    accepted_tokens.append(last_token)
    return accepted_tokens


def estimate_acceptance_rate(draft_probs, target_probs, n_trials=1000):
    """估计接受率（越高越好，说明小模型越接近大模型）"""
    total_tokens = 0
    accepted_tokens = 0
    K = draft_probs.shape[0]
    for _ in range(n_trials):
        # 模拟采样
        draft_tokens = np.array([np.random.choice(draft_probs.shape[1], p=draft_probs[i])
                                  for i in range(K)])
        for i, t in enumerate(draft_tokens):
            ratio = target_probs[i, t] / (draft_probs[i, t] + 1e-10)
            accepted = min(1.0, ratio) > np.random.random()
            total_tokens += 1
            if accepted:
                accepted_tokens += 1
            else:
                break
    return accepted_tokens / total_tokens


if __name__ == "__main__":
    np.random.seed(42)
    K, vocab_size = 4, 50

    # 模拟：小模型和大模型概率相近时，接受率高
    target_logits = np.random.randn(K + 1, vocab_size)
    target_probs = np.array([softmax(target_logits[i]) for i in range(K + 1)])

    # Draft 接近 target（高接受率场景）
    draft_probs_good = np.array([softmax(target_logits[i] + np.random.randn(vocab_size) * 0.1)
                                  for i in range(K)])
    # Draft 偏离 target（低接受率场景）
    draft_probs_bad = np.array([softmax(np.random.randn(vocab_size)) for _ in range(K)])

    acc_good = estimate_acceptance_rate(draft_probs_good, target_probs[:K])
    acc_bad = estimate_acceptance_rate(draft_probs_bad, target_probs[:K])
    print(f"Acceptance rate (good draft): {acc_good:.2%}")
    print(f"Acceptance rate (bad draft):  {acc_bad:.2%}")
    assert acc_good > acc_bad, "Good draft should have higher acceptance rate"

    # 单步解码测试
    draft_tokens = np.array([np.random.choice(vocab_size, p=draft_probs_good[i]) for i in range(K)])
    result = speculative_decode_step(draft_probs_good, target_probs, draft_tokens)
    assert len(result) >= 1 and len(result) <= K + 1

    print("All tests passed.")
