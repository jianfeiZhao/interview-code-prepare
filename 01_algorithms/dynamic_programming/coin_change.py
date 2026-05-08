"""
零钱兑换（完全背包）
LeetCode #322 (Medium)
高频考点: 字节跳动 / 阿里巴巴 / 腾讯 (必考)

============================================================

题目描述
---------
给你一个整数数组 coins，代表不同面额的硬币；以及一个整数 amount，代表总金额。
计算凑成总金额所需的最少的硬币个数，如果无法凑成，返回 -1。
每种硬币的数量是无限的（完全背包）。

示例
------
输入: coins = [1, 2, 5], amount = 11
输出: 3  （11 = 5 + 5 + 1）

输入: coins = [2], amount = 3
输出: -1

约束
------
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4

TL;DR
============================================================
完全背包变形（每种硬币可无限用）

状态: dp[i] = 凑成金额 i 所需的最少硬币数
初始: dp[0]=0, dp[1..amount]=inf
转移: dp[i] = min(dp[i], dp[i - coin] + 1)  for coin in coins if i >= coin
答案: dp[amount]，若仍为 inf 返回 -1

关键：外层枚举金额（0→amount），内层枚举硬币
      完全背包：内层正向遍历（允许重复使用同一硬币）
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：标准完全背包 DP（一维滚动数组）
# ─────────────────────────────────────────────
def coin_change(coins: List[int], amount: int) -> int:
    """
    解题思路:
      完全背包：每枚硬币可以使用无限次。
      dp[i] 代表凑出金额 i 的最少硬币数量。
      对每个金额 i，枚举所有面值 coin：
        若 i >= coin，则 dp[i] = min(dp[i], dp[i-coin] + 1)

      正向遍历金额保证"无限次使用"的语义（与0-1背包逆向遍历相反）。

    时间: O(amount * len(coins))
    空间: O(amount)
    """
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] != INF:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != INF else -1


# ─────────────────────────────────────────────
# 方法2：BFS（层序遍历，等价于找最短路径）
# ─────────────────────────────────────────────
from collections import deque

def coin_change_bfs(coins: List[int], amount: int) -> int:
    """
    解题思路（BFS视角）:
      将问题看作图的最短路径：节点=当前余额，边=使用一枚硬币。
      BFS 从 amount 出发，每次减去一枚硬币面值，到达 0 时返回层数（步数）。
      优先适合"最少步数"此类问题的直觉理解。

    时间: O(amount * len(coins))
    空间: O(amount)
    """
    if amount == 0:
        return 0
    visited = {amount}
    queue = deque([amount])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for coin in coins:
                nxt = curr - coin
                if nxt == 0:
                    return steps
                if nxt > 0 and nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
    return -1


# ─────────────────────────────────────────────
# 扩展: 零钱兑换 II (#518) — 求组合数
# ─────────────────────────────────────────────
def coin_change_ii(amount: int, coins: List[int]) -> int:
    """
    求恰好凑成 amount 的硬币组合数（顺序无关，每种可无限用）。

    状态: dp[i] = 凑成金额 i 的组合方案数
    转移: dp[i] += dp[i - coin]  for coin in coins

    注意：外层枚举硬币、内层枚举金额
          这样可以保证每种硬币"先被完整考虑"，避免重复计数排列。
    时间: O(amount * len(coins))，空间: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_coin_change():
    # 基本用例
    assert coin_change([1, 2, 5], 11) == 3        # 5+5+1
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([1], 1) == 1
    assert coin_change([1, 5, 10, 25], 30) == 2   # 25+5
    assert coin_change([186, 419, 83, 408], 6249) == 20
    print("coin_change (DP): all passed")

    # BFS 结果一致
    assert coin_change_bfs([1, 2, 5], 11) == 3
    assert coin_change_bfs([2], 3) == -1
    assert coin_change_bfs([1], 0) == 0
    print("coin_change (BFS): all passed")

    # 组合数 II
    assert coin_change_ii(5, [1, 2, 5]) == 4      # [1,1,1,1,1],[1,1,1,2],[1,2,2],[5]
    assert coin_change_ii(3, [2]) == 0
    assert coin_change_ii(10, [10]) == 1
    print("coin_change_ii: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_coin_change()
