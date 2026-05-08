"""
题目：最大矩形
难度：Hard | 高频出现：字节/腾讯/阿里
标签：栈、动态规划、数组、矩阵
LeetCode：#85


题目描述
---------
给定一个仅包含 0 和 1 的二维二进制矩阵 matrix，找出只包含 1 的最大矩形，并返回其面积。

示例
------
输入: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],
                ["1","1","1","1","1"],["1","0","0","1","0"]]
输出: 6  （最大矩形面积）

约束
------
- rows == matrix.length，cols == matrix[0].length
- 1 <= rows, cols <= 200
- matrix[i][j] 为 '0' 或 '1'

TL;DR（30秒速览）
- 逐行构建"柱状图高度数组"，对每行调用 #84 最大矩形面积（单调栈）
- 时间 O(m*n)，空间 O(n)
- 关键陷阱：heights 数组遇到 '0' 要清零；单调栈弹出时宽度计算用 i - stack[-1] - 1

详细解析
---------
第一步（降维）：
  heights[j] 表示以第 i 行为底、第 j 列连续向上 '1' 的高度。
  若 matrix[i][j] == '0'，则 heights[j] = 0；否则 heights[j] += 1。

第二步（#84 柱状图最大矩形）：
  使用单调递增栈，栈中存下标。
  遍历时若当前高度 < 栈顶高度，弹出栈顶 h：
    宽度 = i - stack[-1] - 1（stack[-1] 是新的左边界，-1 是哨兵情况）
    面积 = h * width，更新答案。
  末尾追加高度 0 的哨兵强制清空栈。
"""

from typing import List


def largest_rectangle_in_histogram(heights: List[int]) -> int:
    """#84 柱状图中最大的矩形（单调递增栈）"""
    stack: List[int] = [-1]   # 哨兵：模拟左边界 -1
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        h = heights[i] if i < n else 0   # 末尾追加 0，强制清栈
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


def maximal_rectangle(matrix: List[List[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    ans = 0

    for i in range(m):
        # 更新高度数组
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
        # 对当前行的高度数组求最大矩形
        ans = max(ans, largest_rectangle_in_histogram(heights))

    return ans


if __name__ == "__main__":
    matrix1 = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    assert maximal_rectangle(matrix1) == 6

    matrix2 = [["0"]]
    assert maximal_rectangle(matrix2) == 0

    matrix3 = [["1"]]
    assert maximal_rectangle(matrix3) == 1

    print("All tests passed.")
