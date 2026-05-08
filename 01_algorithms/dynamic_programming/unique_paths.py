"""
不同路径 I + II
LeetCode #62 (Medium) + #63 (Medium)
高频考点: 全系大厂

题目描述
---------
给定一个 m x n 的网格，机器人从左上角出发，每次只能向右或向下移动一步，目标是到达右下角。
问共有多少条不同的路径？（#62 无障碍版；#63 有障碍版：obstacleGrid[i][j]==1 的格子不可通行）

示例
------
输入: m = 3, n = 7
输出: 28

输入: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
输出: 2  # 中间格子有障碍，只剩 2 条路径

约束
------
- 1 <= m, n <= 100
- obstacleGrid[i][j] 为 0 或 1

============================================================
TL;DR
============================================================
I (无障碍):
  状态: dp[i][j] = 到达格子 (i,j) 的路径总数
  转移: dp[i][j] = dp[i-1][j] + dp[i][j-1]
  初始: 第一行、第一列全为 1（只能直线走）
  数学公式: C(m+n-2, m-1)（从 m+n-2 步中选 m-1 步向下）

II (有障碍):
  遇到障碍格：dp[i][j] = 0
  其余转移不变

空间优化：一维滚动数组 O(n)，dp[j] += dp[j-1]
============================================================
"""

from typing import List
import math


# ─────────────────────────────────────────────
# I. 不同路径（无障碍）
# ─────────────────────────────────────────────
def unique_paths(m: int, n: int) -> int:
    """
    空间优化版：一维 dp，dp[j] 表示当前行到达第 j 列的路径数。
    初始全 1（第一行），逐行更新：dp[j] += dp[j-1]。
    时间: O(m*n)，空间: O(n)
    """
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]


def unique_paths_math(m: int, n: int) -> int:
    """
    数学公式：从左上到右下共走 m+n-2 步，选其中 m-1 步向下（或 n-1 步向右）。
    C(m+n-2, m-1)
    时间: O(min(m,n))，空间: O(1)
    """
    return math.comb(m + n - 2, m - 1)


# ─────────────────────────────────────────────
# II. 不同路径 II（有障碍）
# ─────────────────────────────────────────────
def unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:
    """
    遇到障碍（值为 1）的格子，路径数强制置 0。
    第一列初始化时需特别处理：一旦某格是障碍，其下方格子均不可达。

    时间: O(m*n)，空间: O(n)
    """
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [0] * n
    dp[0] = 1  # 起点（若起点有障碍则为 0，循环内会覆盖）

    for i in range(m):
        # 处理第一列
        if obstacle_grid[i][0] == 1:
            dp[0] = 0
        for j in range(1, n):
            if obstacle_grid[i][j] == 1:
                dp[j] = 0
            else:
                dp[j] += dp[j - 1]
    return dp[n - 1]


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_unique_paths():
    # I. 无障碍
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(1, 1) == 1
    assert unique_paths(1, 5) == 1
    assert unique_paths(5, 1) == 1
    print("unique_paths (DP): all passed")

    # 数学公式结果一致
    for m, n in [(3, 7), (3, 2), (5, 5), (10, 10)]:
        assert unique_paths(m, n) == unique_paths_math(m, n), f"mismatch at ({m},{n})"
    print("unique_paths_math: all passed")

    # II. 有障碍
    grid1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert unique_paths_with_obstacles(grid1) == 2

    grid2 = [[0, 1], [0, 0]]
    assert unique_paths_with_obstacles(grid2) == 1

    # 起点或终点有障碍
    assert unique_paths_with_obstacles([[1, 0]]) == 0
    assert unique_paths_with_obstacles([[0, 0], [0, 1]]) == 0

    # 全无障碍结果应与 I 一致
    grid3 = [[0] * 7 for _ in range(3)]
    assert unique_paths_with_obstacles(grid3) == unique_paths(3, 7)
    print("unique_paths_with_obstacles: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_unique_paths()
