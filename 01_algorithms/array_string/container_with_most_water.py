"""
题目：盛最多水的容器
难度：Medium | 高频出现：字节/阿里/腾讯/百度
标签：数组、双指针、贪心
LeetCode：#11


题目描述
---------
给定一个长度为 n 的整数数组 height，有 n 条垂线，第 i 条线的两个端点是
(i, 0) 和 (i, height[i])。找出其中的两条线，使得它们与 x 轴共同构成的
容器可以容纳最多的水。返回容器可以储存的最大水量。

示例
------
输入: height = [1,8,6,2,5,4,8,3,7]
输出: 49

输入: height = [1,1]
输出: 1

约束
------
- n == height.length，2 <= n <= 10^5
- 0 <= height[i] <= 10^4

TL;DR（30秒速览）
- 思路：左右双指针，每次移动较矮的那侧（移高侧面积必减，无意义）
- 时间：O(n)  空间：O(1)
- 陷阱：面积 = min(h[l], h[r]) * (r - l)，移动较矮侧才有机会增大面积

详细解析
---------
暴力法：枚举所有 (i, j) 对，O(n²)，面试不可接受。

双指针贪心（最优）：
  - 初始 left=0, right=n-1，此时宽度最大。
  - 每次计算当前面积 min(h[l], h[r]) * (r-l)，更新最大值。
  - 移动策略：移动较矮一侧——因为宽度必然减少，只有换到更高的板才可能
    增大面积；若移动较高侧，高度上限不变甚至降低，面积只减不增。
  - 双指针相遇时遍历结束。

正确性证明（面试可提）：
  设 h[l] <= h[r]，当前面积 = h[l]*(r-l)。
  固定 l，任意 r' < r 的面积 = min(h[l], h[r'])*(r'-l) <= h[l]*(r'-l) < h[l]*(r-l)。
  故以 l 为左边界的最大面积已找到，可以安全移动 l。
"""

from typing import List


def max_area(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        area = min(height[left], height[right]) * (right - left)
        best = max(best, area)
        # 移动较矮的一侧
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1

    return best


if __name__ == "__main__":
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    assert max_area([4, 3, 2, 1, 4]) == 16
    assert max_area([1, 2, 1]) == 2
    print("All tests passed.")
