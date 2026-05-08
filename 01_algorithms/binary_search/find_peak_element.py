"""
题目：寻找峰值
难度：Medium | 高频出现：字节/阿里
标签：二分查找
LeetCode：#162

题目描述
---------
给定整数数组 nums，峰值元素是指其值严格大于左右相邻值的元素。
数组边界外视为负无穷，数组中任意两个相邻元素不相等。
返回任意一个峰值元素的下标（存在多个峰值时返回任意一个即可）。

示例
------
输入: nums = [1, 2, 3, 1]
输出: 2  # nums[2]=3 是峰值（3 > 2 且 3 > 1）

输入: nums = [1, 2, 1, 3, 5, 6, 4]
输出: 1 或 5  # 两处峰值均可

约束
------
- 1 <= len(nums) <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- 相邻元素不相等，需在 O(log n) 时间内完成

TL;DR（30秒速览）
- 二分：若 nums[m] < nums[m+1]，峰值在右半；否则在左半或m本身
- 时间 O(log n)，空间 O(1)

详细解析
---------
关键性质：
  - 数组边界视为 -inf，所以一定存在峰值
  - 若 nums[m] < nums[m+1]，说明右侧有上升趋势，峰值在 (m, r]
  - 否则 nums[m] > nums[m-1]，峰值在 [l, m]

可以找任意一个峰值，不是全局最大值。
"""

from typing import List


def find_peak_element(nums: List[int]) -> int:
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] < nums[m + 1]:
            l = m + 1
        else:
            r = m
    return l


if __name__ == "__main__":
    result = find_peak_element([1, 2, 3, 1])
    assert result == 2

    result2 = find_peak_element([1, 2, 1, 3, 5, 6, 4])
    assert result2 in (1, 5)  # 任意峰值都可以

    assert find_peak_element([1]) == 0
    assert find_peak_element([1, 2]) == 1
    print("All tests passed.")
