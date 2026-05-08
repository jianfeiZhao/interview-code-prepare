"""
LeetCode #85 - 最大矩形 (Maximal Rectangle)
难度: Hard | 频率: 字节/阿里

=== 题目描述 ===
给定一个仅包含 0 和 1、大小为 rows x cols 的二维二进制矩阵，找出只包含 1 的最大矩形，并返回其面积。

示例:
  输入: matrix = [
    ["1","0","1","0","0"],
    ["1","0","1","1","1"],
    ["1","1","1","1","1"],
    ["1","0","0","1","0"]
  ]
  输出: 6

=== TL;DR ===
核心思路: 逐行将矩阵转化为"柱状图高度数组"，然后对每行的高度数组调用 #84 的单调栈解法。
  - 对第 i 行，heights[j] = 从第 i 行往上连续 1 的个数（遇到 0 归零）
  - 每行都是一个独立的柱状图最大矩形问题

时间复杂度: O(m*n)，m 行 n 列
空间复杂度: O(n)，高度数组

=== 详细解析 ===
关键技巧:
1. 动态维护 heights 数组: heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
2. 对每行的 heights 调用 largest_rectangle_in_histogram（#84 单调栈）
3. #84 核心: 两端加 0 哨兵，单调递增栈，弹出时计算面积
4. 理解降维思路: 2D 矩形最大面积 = 逐行转化为 1D 柱状图 + 重用 #84 解法
5. 也可用 DP 解法（三个辅助数组 left/right/height），但单调栈更直观

相关题:
  - #84: 柱状图中最大的矩形（本题子问题）
  - #221: 最大正方形（DP 解法不同）
"""


# ===== #84 辅助: 柱状图最大矩形（单调栈）=====
def largest_rectangle_histogram(heights: list) -> int:
    heights = [0] + heights + [0]  # 两端加 0 哨兵
    stack = [0]
    max_area = 0
    for i in range(1, len(heights)):
        while heights[stack[-1]] > heights[i]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)
    return max_area


# ===== #85 主解法: 逐行展开为柱状图 =====
def maximal_rectangle(matrix: list) -> int:
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    for row in matrix:
        # 更新每列的高度
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        # 对当前行的高度数组求最大矩形
        max_area = max(max_area, largest_rectangle_histogram(heights))

    return max_area


# ===== 暴力解法（O(m^2*n^2)，用于小规模验证）=====
def maximal_rectangle_brute(matrix: list) -> int:
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    max_area = 0
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    # 检查 (r1,c1)-(r2,c2) 矩形是否全为 1
                    all_ones = all(
                        matrix[r][c] == '1'
                        for r in range(r1, r2 + 1)
                        for c in range(c1, c2 + 1)
                    )
                    if all_ones:
                        max_area = max(max_area, (r2 - r1 + 1) * (c2 - c1 + 1))
    return max_area


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        (
            [["1","0","1","0","0"],
             ["1","0","1","1","1"],
             ["1","1","1","1","1"],
             ["1","0","0","1","0"]],
            6
        ),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["1","1"]], 2),
        (
            [["1","1","1"],
             ["1","1","1"]],
            6
        ),
        (
            [["0","0","0"],
             ["0","0","0"]],
            0
        ),
        (
            [["1","0","1","1","1"],
             ["1","0","1","0","1"],
             ["1","1","1","0","1"]],
            3
        ),
    ]

    for matrix, expected in cases:
        res1 = maximal_rectangle(matrix)
        res2 = maximal_rectangle_brute(matrix)
        assert res1 == expected, f"maximal_rectangle({matrix}) = {res1}, expected {expected}"
        assert res2 == expected, f"maximal_rectangle_brute({matrix}) = {res2}, expected {expected}"

    print("All tests passed!")
