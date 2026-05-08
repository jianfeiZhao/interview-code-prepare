"""
最大正方形
LeetCode #221 (Medium)
高频考点: 字节跳动 / 阿里巴巴

============================================================

题目描述
---------
在一个由 '0' 和 '1' 组成的二维矩阵内，找到只包含 '1' 的最大正方形，并返回其面积。

示例
------
输入: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],
                ["1","1","1","1","1"],["1","0","0","1","0"]]
输出: 4  （边长为 2 的正方形）

输入: matrix = [["0","1"],["1","0"]]
输出: 1

约束
------
- m == matrix.length，n == matrix[i].length
- 1 <= m, n <= 300
- matrix[i][j] 为 '0' 或 '1'

TL;DR
============================================================
状态: dp[i][j] = 以 (i,j) 为右下角能形成的最大全 '1' 正方形的边长
转移:
  若 matrix[i][j] == '1':
      dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
  否则:
      dp[i][j] = 0
答案: max(dp)^2（面积）

关键直觉：右下角能扩展出边长为 k 的正方形，要求其左、上、左上三格
          的最大正方形边长均 >= k-1，取三者最小值 + 1。
陷阱：返回的是面积，不是边长！
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：二维 DP
# ─────────────────────────────────────────────
def maximal_square(matrix: List[List[str]]) -> int:
    """
    时间: O(m * n)，空间: O(m * n)
    """
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    max_side = 0

    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_side = max(max_side, dp[i][j])
    return max_side * max_side


# ─────────────────────────────────────────────
# 方法2：空间优化（滚动一行 + 变量保存左上角）
# ─────────────────────────────────────────────
def maximal_square_optimized(matrix: List[List[str]]) -> int:
    """
    只保留当前行 dp，用变量 prev 保存 dp[i-1][j-1]（左上角）。
    时间: O(m * n)，空间: O(n)
    """
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [0] * n
    max_side = 0

    for i in range(m):
        prev = 0  # 代表 dp[i-1][j-1]
        for j in range(n):
            temp = dp[j]  # 保存 dp[i-1][j]，即将被覆盖
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[j] = 1
                else:
                    dp[j] = min(dp[j], dp[j - 1], prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp  # 下一列的 prev 就是本列更新前的值
    return max_side * max_side


# ─────────────────────────────────────────────
# 扩展：最大矩形（#85 Hard）
# 柱状图最大面积的矩阵版本
# ─────────────────────────────────────────────
def maximal_rectangle(matrix: List[List[str]]) -> int:
    """
    LeetCode #85 Hard.
    逐行构建高度直方图，对每行调用"柱状图最大矩形面积"（单调栈）。
    时间: O(m * n)，空间: O(n)
    """
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    def largest_in_histogram(h: List[int]) -> int:
        stack = [-1]
        area = 0
        for i, val in enumerate(h):
            while stack[-1] != -1 and h[stack[-1]] >= val:
                height = h[stack.pop()]
                width = i - stack[-1] - 1
                area = max(area, height * width)
            stack.append(i)
        while stack[-1] != -1:
            height = h[stack.pop()]
            width = len(h) - stack[-1] - 1
            area = max(area, height * width)
        return area

    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        max_area = max(max_area, largest_in_histogram(heights))
    return max_area


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_maximal_square():
    matrix1 = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    assert maximal_square(matrix1) == 4
    assert maximal_square_optimized(matrix1) == 4

    matrix2 = [["0", "1"], ["1", "0"]]
    assert maximal_square(matrix2) == 1
    assert maximal_square_optimized(matrix2) == 1

    assert maximal_square([["0"]]) == 0
    assert maximal_square([["1"]]) == 1
    assert maximal_square([]) == 0

    # 全 1 矩阵
    full = [["1"] * 4 for _ in range(4)]
    assert maximal_square(full) == 16
    assert maximal_square_optimized(full) == 16
    print("maximal_square: all passed")

    # 最大矩形（#85）
    assert maximal_rectangle(matrix1) == 6
    assert maximal_rectangle([["1", "0"], ["1", "0"]]) == 2
    print("maximal_rectangle: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_maximal_square()
