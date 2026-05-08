"""
题目：接雨水
难度：Hard | 高频出现：字节/阿里/腾讯
标签：双指针、单调栈、动态规划
LeetCode：#42


题目描述
---------
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，
下雨之后能接多少雨水。

示例
------
输入: height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出: 6

输入: height = [4,2,0,3,2,5]
输出: 9

约束
------
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

TL;DR（30秒速览）
- 思路（双指针）：左右指针向中间收缩，较小一侧决定当前格能接多少水
- 时间：O(n)  空间：O(1)
- 陷阱：每格能接的水 = min(左最高, 右最高) - 当前高度

详细解析
---------
方法1 - 预处理数组（易理解）：
  left_max[i] = max(height[0..i])
  right_max[i] = max(height[i..n-1])
  ans += min(left_max[i], right_max[i]) - height[i]
  时间 O(n)，空间 O(n)

方法2 - 双指针（空间O(1)，推荐）：
  left, right 指针，left_max, right_max 实时维护
  哪边更低，处理哪边：
    height[left] < height[right]:
      若 height[left] >= left_max → 更新 left_max
      否则 ans += left_max - height[left]
      left++
    反之同理处理右边

方法3 - 单调栈：
  维护一个单调递减栈（存下标），遇到比栈顶高的柱子时，
  弹出栈顶作为"谷底"，计算以该谷底为底的横向积水。
"""

from typing import List


def trap_two_pointers(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    ans = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                ans += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                ans += right_max - height[right]
            right -= 1
    return ans


def trap_monotonic_stack(height: List[int]) -> int:
    stack = []  # 存下标，单调递减
    ans = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(h, height[stack[-1]]) - height[bottom]
            ans += width * bounded_height
        stack.append(i)
    return ans


if __name__ == "__main__":
    assert trap_two_pointers([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
    assert trap_two_pointers([4,2,0,3,2,5]) == 9
    assert trap_monotonic_stack([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
    print("All tests passed.")
