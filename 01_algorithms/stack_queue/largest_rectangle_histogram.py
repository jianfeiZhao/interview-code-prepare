"""
LeetCode #84 - 柱状图中最大的矩形 (Largest Rectangle in Histogram)
难度: Hard | 频率: 字节/腾讯/阿里

=== 题目描述 ===
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1。
求在该柱状图中，能够勾勒出来的矩形的最大面积。

示例 1: heights = [2,1,5,6,2,3]  输出: 10
示例 2: heights = [2,4]           输出: 4

=== TL;DR ===
核心思路（单调栈）: 维护单调递增栈，当遇到比栈顶矮的柱时，弹出并计算以该柱为高的最大宽度。
  - 两端加 0 哨兵，简化边界处理
  - 弹出下标 i 时：高度 = heights[i]，宽度 = 当前下标 - 新栈顶下标 - 1
时间复杂度: O(n)
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. 哨兵: heights = [0] + heights + [0]，右哨兵 0 保证所有元素都会被弹出处理
2. 栈中存下标，弹出时宽度 = i - stack[-1] - 1（新栈顶到当前位置之间）
3. 单调递增栈保证栈顶左侧第一个更矮的柱就是 stack[-1]，右侧第一个更矮的就是 i
4. 面积 = 高度 * 宽度 = heights[pop] * (i - new_stack_top - 1)
5. 暴力解法: O(n^2)，对每个柱向左右扩展找边界
6. DP 解法: 预处理每个柱的左右边界 — O(n) 时间，O(n) 空间（单调栈更简洁）
"""


# ===== 方法1: 单调栈 + 哨兵（面试推荐）=====
def largest_rectangle_area(heights: list) -> int:
    heights = [0] + heights + [0]  # 两端加 0 哨兵
    stack = [0]  # 存下标，初始放左哨兵
    max_area = 0

    for i in range(1, len(heights)):
        # 遇到更矮的柱，弹出并计算面积
        while heights[stack[-1]] > heights[i]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1   # 左边界是新栈顶，右边界是 i
            max_area = max(max_area, h * w)
        stack.append(i)

    return max_area


# ===== 方法2: 暴力（O(n^2) 用于验证）=====
def largest_rectangle_brute(heights: list) -> int:
    n = len(heights)
    max_area = 0
    for i in range(n):
        min_h = heights[i]
        for j in range(i, n):
            min_h = min(min_h, heights[j])
            max_area = max(max_area, min_h * (j - i + 1))
    return max_area


# ===== 方法3: DP（预处理左右边界）=====
def largest_rectangle_dp(heights: list) -> int:
    n = len(heights)
    # left[i]: 左侧第一个比 heights[i] 小的下标
    # right[i]: 右侧第一个比 heights[i] 小的下标
    left = [0] * n
    right = [n] * n

    # 预处理 left
    for i in range(n):
        j = i - 1
        while j >= 0 and heights[j] >= heights[i]:
            j = left[j] - 1  # 跳过已知区间（加速）
        left[i] = j + 1

    # 预处理 right
    for i in range(n - 1, -1, -1):
        j = i + 1
        while j < n and heights[j] >= heights[i]:
            j = right[j]
        right[i] = j

    max_area = 0
    for i in range(n):
        max_area = max(max_area, heights[i] * (right[i] - left[i]))
    return max_area


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([1], 1),
        ([0], 0),
        ([5, 4, 1, 2], 8),
        ([1, 2, 3, 4, 5], 9),
        ([5, 5, 5, 5, 5], 25),
        ([6, 2, 5, 4, 5, 1, 6], 12),
        ([3, 6, 5, 7, 4, 8, 1, 0], 20),
    ]
    for func in [largest_rectangle_area, largest_rectangle_brute, largest_rectangle_dp]:
        for heights, expected in cases:
            result = func(list(heights))
            assert result == expected, \
                f"{func.__name__}({heights}) = {result}, expected {expected}"

    print("All tests passed!")
