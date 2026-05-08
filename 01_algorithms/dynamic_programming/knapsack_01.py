"""
0-1 背包问题（经典模板）
非 LeetCode 题，但面试必考
高频考点: 字节跳动 / 阿里巴巴

============================================================

题目描述
---------
给定 n 件物品，第 i 件物品重量为 w[i]，价值为 v[i]，背包容量为 W。
每件物品只能选 0 或 1 次（0-1 背包），求在不超过背包容量的情况下能装入物品的最大总价值。
这是动态规划最基础的经典题型，也是完全背包、分组背包的前置知识。

示例
------
输入: W=5, weights=[2,3,4], values=[3,4,5]
输出: 7  （选重量2和3的物品）

约束
------
- 1 <= n <= 1000，1 <= w[i] <= W <= 10^5
- 1 <= v[i] <= 10^4

TL;DR
============================================================
n 件物品，每件有重量 w[i] 和价值 v[i]，背包容量 W，每件只能用一次。

状态: dp[i][j] = 前 i 件物品、容量 j 时的最大价值
转移:
  不放第 i 件: dp[i][j] = dp[i-1][j]
  放第 i 件:   dp[i][j] = dp[i-1][j-w[i]] + v[i]  (j >= w[i])
  dp[i][j] = max(两者)

空间优化（一维滚动数组）:
  dp[j] = max(dp[j], dp[j - w[i]] + v[i])
  内层必须逆向遍历（j: W → w[i]），防止同一件物品被选多次。

完全背包对比:
  内层正向遍历 → 允许重复使用同一物品。
============================================================
"""

from typing import List, Tuple


# ─────────────────────────────────────────────
# 方法1：二维 DP（直观，便于理解）
# ─────────────────────────────────────────────
def knapsack_2d(W: int, weights: List[int], values: List[int]) -> int:
    """
    时间: O(n * W)，空间: O(n * W)

    参数:
      W:       背包最大承重
      weights: 各物品重量列表
      values:  各物品价值列表
    返回最大总价值。
    """
    n = len(weights)
    # dp[i][j]: 考虑前 i 件物品，容量 j 时的最大价值
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for j in range(W + 1):
            dp[i][j] = dp[i - 1][j]        # 不放第 i 件
            if j >= w_i:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w_i] + v_i)  # 放第 i 件

    return dp[n][W]


# ─────────────────────────────────────────────
# 方法2：一维滚动数组（空间优化，O(W)）
# ─────────────────────────────────────────────
def knapsack_1d(W: int, weights: List[int], values: List[int]) -> int:
    """
    空间优化到 O(W)。
    关键：内层逆向遍历，保证每件物品最多被选一次。

    原理：逆向遍历时，dp[j-w[i]] 引用的是"上一行"的值（还未被本轮更新），
          等价于二维 DP 中的 dp[i-1][j-w[i]]。
    """
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        # 逆向遍历：防止重复放入同一物品
        for j in range(W, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])

    return dp[W]


# ─────────────────────────────────────────────
# 扩展1：方案数（能否恰好装满背包）
# ─────────────────────────────────────────────
def knapsack_exactly(W: int, weights: List[int]) -> bool:
    """
    判断能否从 weights 中选若干件恰好凑出重量 W（每件只用一次）。
    等价于: 分割等和子集 LeetCode #416。

    dp[j] = 能否恰好凑出重量 j
    转移: dp[j] = dp[j] or dp[j - w[i]]  （逆向遍历）
    """
    dp = [False] * (W + 1)
    dp[0] = True
    for w in weights:
        for j in range(W, w - 1, -1):
            dp[j] = dp[j] or dp[j - w]
    return dp[W]


# ─────────────────────────────────────────────
# 扩展2：路径回溯（输出选了哪些物品）
# ─────────────────────────────────────────────
def knapsack_with_trace(W: int, weights: List[int], values: List[int]) -> Tuple[int, List[int]]:
    """
    返回 (最大价值, 选取的物品下标列表)。
    使用二维 DP，然后从 dp[n][W] 反向回溯。
    """
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w_i, v_i = weights[i - 1], values[i - 1]
        for j in range(W + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= w_i:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w_i] + v_i)

    # 回溯：从右下角往左上角追踪
    selected = []
    j = W
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:  # 第 i 件物品被选入
            selected.append(i - 1)
            j -= weights[i - 1]
    selected.reverse()
    return dp[n][W], selected


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_knapsack():
    # 经典用例
    W = 10
    weights = [2, 3, 4, 5]
    values  = [3, 4, 5, 6]
    # 选 w=3(v=4) + w=5(v=6) + w=2(v=3) = 10，价值=13
    # 实际最优：w=3+w=2+w=5 = 10, v=4+3+6=13
    assert knapsack_2d(W, weights, values) == 13
    assert knapsack_1d(W, weights, values) == 13
    print("knapsack_2d & knapsack_1d: all passed")

    # 单件放不下
    assert knapsack_2d(1, [2], [10]) == 0
    assert knapsack_1d(1, [2], [10]) == 0

    # 全部放得下
    assert knapsack_2d(100, [1, 2, 3], [10, 20, 30]) == 60
    assert knapsack_1d(100, [1, 2, 3], [10, 20, 30]) == 60
    print("edge cases passed")

    # 恰好装满
    assert knapsack_exactly(9, [2, 3, 4, 5]) == True    # 4+5=9
    assert knapsack_exactly(8, [2, 3, 4, 5]) == True    # 3+5=8
    assert knapsack_exactly(1, [2, 3, 4, 5]) == False
    print("knapsack_exactly: all passed")

    # 路径回溯
    max_val, selected = knapsack_with_trace(10, weights, values)
    assert max_val == 13
    # 验证选取的物品总重 <= W 且总价值 == max_val
    total_w = sum(weights[i] for i in selected)
    total_v = sum(values[i] for i in selected)
    assert total_w <= W and total_v == max_val
    print(f"knapsack_with_trace: max_val={max_val}, selected indices={selected}")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_knapsack()
