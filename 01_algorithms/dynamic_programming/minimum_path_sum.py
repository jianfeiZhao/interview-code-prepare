"""
最小路径和
LeetCode #64 (Medium)
高频考点: 字节跳动 / 腾讯

============================================================

题目描述
---------
给定一个包含非负整数的 m x n 网格 grid，请找出一条从左上角到右下角的路径，
使得路径上的数字总和最小。每次只能向下或者向右移动一步。

示例
------
输入: grid = [[1,3,1],[1,5,1],[4,2,1]]
输出: 7  （路径 1→3→1→1→1）

输入: grid = [[1,2,3],[4,5,6]]
输出: 12

约束
------
- m == grid.length，n == grid[i].length
- 1 <= m, n <= 200
- 0 <= grid[i][j] <= 200

TL;DR
============================================================
状态: dp[i][j] = 从左上角到 (i,j) 的最小路径和
初始: dp[0][0] = grid[0][0]
      第一行: dp[0][j] = dp[0][j-1] + grid[0][j]（只能从左来）
      第一列: dp[i][0] = dp[i-1][0] + grid[i][0]（只能从上来）
转移: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
答案: dp[m-1][n-1]

空间优化：原地修改 or 一维滚动数组 O(n)
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：原地修改（不额外开辟空间）
# ─────────────────────────────────────────────
def min_path_sum_inplace(grid: List[List[int]]) -> int:
    """
    直接在 grid 上进行 DP，节省 O(m*n) 的额外空间。
    注意：此方法会修改输入，若不允许可先深拷贝。
    时间: O(m*n)，空间: O(1)（不含输入）
    """
    m, n = len(grid), len(grid[0])

    # 初始化第一行
    for j in range(1, n):
        grid[0][j] += grid[0][j - 1]
    # 初始化第一列
    for i in range(1, m):
        grid[i][0] += grid[i - 1][0]

    for i in range(1, m):
        for j in range(1, n):
            grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])

    return grid[m - 1][n - 1]


# ─────────────────────────────────────────────
# 方法2：一维滚动数组（不修改输入）
# ─────────────────────────────────────────────
def min_path_sum(grid: List[List[int]]) -> int:
    """
    dp[j] 代表当前行到达第 j 列的最小路径和。
    逐行更新，dp[j] = grid[i][j] + min(dp[j], dp[j-1])
      dp[j]   表示从上方来（上一行同列）
      dp[j-1] 表示从左方来（当前行左列）
    时间: O(m*n)，空间: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(m):
        dp[0] += grid[i][0]  # 第一列只能从上来
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])

    return dp[n - 1]


# ─────────────────────────────────────────────
# 扩展：输出最小路径（回溯）
# ─────────────────────────────────────────────
def min_path_sum_with_path(grid: List[List[int]]):
    """
    返回 (最小路径和, 路径坐标列表)。
    使用二维 DP 后回溯。
    """
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

    # 回溯路径
    path = []
    i, j = m - 1, n - 1
    while i > 0 or j > 0:
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif dp[i - 1][j] < dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    path.append((0, 0))
    path.reverse()
    return dp[m - 1][n - 1], path


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_minimum_path_sum():
    import copy

    grid1 = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    # 1→3→1→1→1 = 7
    assert min_path_sum(grid1) == 7
    assert min_path_sum_inplace(copy.deepcopy(grid1)) == 7

    grid2 = [[1, 2, 3], [4, 5, 6]]
    # 1→2→3→6 = 12
    assert min_path_sum(grid2) == 12
    assert min_path_sum_inplace(copy.deepcopy(grid2)) == 12

    # 单行
    assert min_path_sum([[1, 2, 3]]) == 6
    # 单列
    assert min_path_sum([[1], [2], [3]]) == 6
    # 单格
    assert min_path_sum([[5]]) == 5
    print("min_path_sum: all passed")

    # 路径回溯
    val, path = min_path_sum_with_path([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    assert val == 7
    assert path[0] == (0, 0) and path[-1] == (2, 2)
    # 路径长度 = m + n - 1
    assert len(path) == 3 + 3 - 1
    print(f"path: {path}")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_minimum_path_sum()
