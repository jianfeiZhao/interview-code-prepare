"""
题目：Top-k / Top-p（Nucleus）采样
难度：Medium | 高频出现：字节/阿里（LLM推理岗）
标签：解码策略、采样、温度


题目描述
---------
手写实现 LLM 解码时的采样策略：Temperature 缩放、Top-k 采样、Top-p（Nucleus）采样。
这些采样方法控制生成文本的多样性和质量，是 LLM 推理的重要组成部分。

  - Temperature：softmax(logits/T)，T→0 趋向贪心，T→∞ 趋向均匀
  - Top-k：只从概率最高的 k 个 token 中采样，截断长尾
  - Top-p（Nucleus）：从累积概率 ≥ p 的最小 token 集合采样，自适应候选数量

输入/输出
----------
输入: logits（词表大小 V），temperature（float），k（int），p（float）
输出: sampled_token_id（int）

约束
------
- 推荐组合：先 Top-k，再 Top-p，再 Temperature，综合过滤效果更好
- Greedy = Temperature(0) 或 Top-k(1)

TL;DR（30秒速览）
- Top-k：只从概率最高的 k 个 token 中采样
- Top-p（nucleus）：从累积概率 >= p 的最小 token 集合采样
- Temperature：控制分布尖锐程度，T→0 贪心搜索，T→∞ 均匀分布

详细解析
---------
贪心解码：每步取 argmax，确定性但质量一般
束搜索（Beam Search）：维护 k 条路径，质量高但多样性差
采样方法：有随机性，生成更自然

Top-k vs Top-p：
  Top-k 固定候选数，分布扁平时候选少（保守），尖锐时候选多（宽松）
  Top-p 自适应候选数，更合理

组合使用：先 Top-k 截断，再 Top-p 过滤，再 Temperature 缩放
"""

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max()
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()


def temperature_scaling(logits: np.ndarray, temperature: float) -> np.ndarray:
    """温度缩放：T < 1 更确定，T > 1 更随机"""
    if temperature == 0:
        one_hot = np.zeros_like(logits)
        one_hot[np.argmax(logits)] = 1.0
        return one_hot
    return softmax(logits / temperature)


def top_k_sampling(logits: np.ndarray, k: int, temperature: float = 1.0) -> int:
    """Top-k 采样"""
    probs = temperature_scaling(logits, temperature)
    top_k_indices = np.argsort(probs)[-k:]
    top_k_probs = probs[top_k_indices]
    top_k_probs /= top_k_probs.sum()  # 重归一化
    return int(np.random.choice(top_k_indices, p=top_k_probs))


def top_p_sampling(logits: np.ndarray, p: float, temperature: float = 1.0) -> int:
    """Top-p（Nucleus）采样"""
    probs = temperature_scaling(logits, temperature)
    sorted_indices = np.argsort(probs)[::-1]  # 从大到小
    sorted_probs = probs[sorted_indices]
    cumulative_probs = np.cumsum(sorted_probs)

    # 找到累积概率超过 p 的最小集合
    # 保留第一个使累积概率 >= p 的 token（inclusive）
    cutoff_idx = np.searchsorted(cumulative_probs, p) + 1
    nucleus_indices = sorted_indices[:cutoff_idx]
    nucleus_probs = probs[nucleus_indices]
    nucleus_probs /= nucleus_probs.sum()
    return int(np.random.choice(nucleus_indices, p=nucleus_probs))


def greedy_decode(logits: np.ndarray) -> int:
    return int(np.argmax(logits))


def beam_search_step(logits: np.ndarray, beams: list, beam_width: int) -> list:
    """
    beams: [(score, token_sequence), ...]
    单步 beam search（简化版）
    """
    log_probs = np.log(softmax(logits) + 1e-12)
    new_beams = []
    for score, seq in beams:
        for token_id in range(len(logits)):
            new_beams.append((score + log_probs[token_id], seq + [token_id]))
    new_beams.sort(key=lambda x: x[0], reverse=True)
    return new_beams[:beam_width]


if __name__ == "__main__":
    np.random.seed(42)
    vocab_size = 100
    logits = np.random.randn(vocab_size)

    # Top-k 测试：返回值在有效范围
    for _ in range(10):
        idx = top_k_sampling(logits, k=10)
        assert 0 <= idx < vocab_size

    # Top-p 测试
    for _ in range(10):
        idx = top_p_sampling(logits, p=0.9)
        assert 0 <= idx < vocab_size

    # Temperature → 0 时等价于贪心
    greedy_idx = greedy_decode(logits)
    topk_greedy = top_k_sampling(logits, k=1, temperature=1.0)
    # k=1 时等价于贪心
    assert topk_greedy == greedy_idx

    # 分布测试：高温度时分布更均匀
    n_samples = 10000
    samples_low_t = [top_k_sampling(logits, k=50, temperature=0.1) for _ in range(n_samples)]
    samples_high_t = [top_k_sampling(logits, k=50, temperature=2.0) for _ in range(n_samples)]
    unique_low = len(set(samples_low_t))
    unique_high = len(set(samples_high_t))
    assert unique_high > unique_low, "Higher temperature should give more diverse samples"
    print(f"Unique tokens (T=0.1): {unique_low}, (T=2.0): {unique_high}")
    print("All tests passed.")
