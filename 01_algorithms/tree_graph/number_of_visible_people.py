"""
题目：可以被一步捕获的棋子数 / 每个人能看到的人数
难度：Hard | 高频出现：字节/阿里
标签：单调栈
LeetCode：#1944 队列中可以看到的人数

题目描述
---------
有 n 个人站成一排，给定整数数组 heights 表示每个人的身高，所有身高互不相同。
对于位置 i 的人，他能"看到"位置 j（j > i）的人，当且仅当 i 和 j 之间没有任何人的
身高同时大于等于两人中较矮者且遮挡视线——即 heights[k] < min(heights[i], heights[j])
对所有 i < k < j 成立，或更简洁地：i 能看到 j 当且仅当两人之间不存在身高 >= heights[j] 的人。
返回数组 answer，其中 answer[i] 是第 i 个人能看到的人数。

示例
------
输入: heights = [10, 6, 8, 5, 11, 9]
输出: [3, 1, 2, 1, 1, 0]

输入: heights = [5, 1, 2, 3, 10]
输出: [4, 1, 1, 1, 0]

约束
------
- n == heights.length
- 1 <= n <= 10^5
- 1 <= heights[i] <= 10^5，且所有值互不相同

TL;DR（30秒速览）
- 单调递减栈：从右向左处理，每个人能看到的是右侧第一个更高的人的路上所有人
- 时间 O(n)，空间 O(n)

详细解析
---------
从右向左遍历，维护单调递减栈：
  对当前人 heights[i]，右边高于他的第一个人就是栈中第一个 >= heights[i] 的
  在此之前弹出的所有人（比 heights[i] 矮的）都能被 i 看到
  最后若栈非空，i 还能看到栈顶（比 i 高的那个）
"""

from typing import List


def can_see_persons_count(heights: List[int]) -> List[int]:
    n = len(heights)
    result = [0] * n
    stack = []  # 单调递减栈（存高度）

    for i in range(n - 1, -1, -1):
        count = 0
        while stack and stack[-1] < heights[i]:
            stack.pop()
            count += 1
        if stack:
            count += 1  # 能看到第一个比自己高的
        result[i] = count
        stack.append(heights[i])

    return result


if __name__ == "__main__":
    assert can_see_persons_count([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
    assert can_see_persons_count([5, 1, 2, 3, 10]) == [4, 1, 1, 1, 0]
    assert can_see_persons_count([1]) == [0]
    print("All tests passed.")
