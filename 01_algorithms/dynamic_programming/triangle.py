"""
题目：三角形最小路径和
难度：Medium | 高频出现：字节/阿里
标签：动态规划、数组
LeetCode：#120

题目描述
---------
给定一个三角形 triangle，找出自顶向下的最小路径和。
每一步只能移动到下一行中相邻的结点（即从位置 j 只能移动到下一行的 j 或 j+1）。
返回从顶部到底部的最小路径和。

示例
------
输入: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
输出: 11  # 路径 2 → 3 → 5 → 1，和为 11

约束
------
- 1 <= triangle.length <= 200
- triangle[i].length == i + 1
- -10^4 <= triangle[i][j] <= 10^4

TL;DR（30秒速览）
- 自底向上原地修改 triangle，dp[j] = min(dp[j], dp[j+1]) + triangle[i][j]
- 时间 O(n^2)，空间 O(n)（复用最后一行）
- 关键陷阱：自顶向下需要考虑边界，自底向上更简洁

详细解析
---------
设 n 行三角形。令 dp 数组初始化为最后一行的值。
从倒数第二行向上遍历：
  dp[j] = min(dp[j], dp[j+1]) + triangle[i][j]
最终 dp[0] 即为答案。

为什么自底向上更好？
  - 不需要判断边界（最后一行每个格子都有两个下方邻居 dp[j] 和 dp[j+1]）
  - 原地修改 triangle 也可以，但传入 dp 副本更安全
"""

from typing import List


def minimum_total(triangle: List[List[int]]) -> int:
    n = len(triangle)
    # 复制最后一行作为 DP 数组
    dp = triangle[-1][:]

    # 从倒数第二行向上推
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):  # 第 i 行有 i+1 个元素
            dp[j] = min(dp[j], dp[j + 1]) + triangle[i][j]

    return dp[0]


# 方法二：自顶向下（使用 O(n^2) dp 表，更直观）
def minimum_total_top_down(triangle: List[List[int]]) -> int:
    n = len(triangle)
    dp = [[0] * (i + 1) for i in range(n)]
    dp[0][0] = triangle[0][0]

    for i in range(1, n):
        dp[i][0] = dp[i - 1][0] + triangle[i][0]
        dp[i][i] = dp[i - 1][i - 1] + triangle[i][i]
        for j in range(1, i):
            dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j]) + triangle[i][j]

    return min(dp[n - 1])


if __name__ == "__main__":
    t1 = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    assert minimum_total(t1) == 11           # 2 -> 3 -> 5 -> 1
    assert minimum_total_top_down(t1) == 11

    t2 = [[-10]]
    assert minimum_total(t2) == -10

    print("All tests passed.")
