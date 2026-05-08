"""
题目：最大连续1的个数III
难度：Medium | 高频出现：字节/阿里
标签：滑动窗口
LeetCode：#1004

题目描述
---------
给定一个由 0 和 1 组成的二进制数组 nums 和一个整数 k。
最多可以将 k 个 0 翻转为 1，返回翻转后数组中最长的连续 1 的个数。

示例
------
输入: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
输出: 6  # 翻转下标3和4的两个0，得到 [1,1,1,1,1,1,1,1,1,1,0]，最长连续1为6

输入: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
输出: 10

约束
------
- 1 <= len(nums) <= 10^5
- nums[i] 为 0 或 1
- 0 <= k <= len(nums)

TL;DR（30秒速览）
- 滑动窗口：窗口内最多k个0，维护最长合法窗口
- 时间 O(n)，空间 O(1)

详细解析
---------
窗口 [l, r] 内0的个数不超过k。
当0的个数 > k 时，移动 l 直到窗口合法。
答案为最大窗口长度。
"""

from typing import List


def longest_ones(nums: List[int], k: int) -> int:
    l = zeros = 0
    result = 0
    for r, val in enumerate(nums):
        if val == 0:
            zeros += 1
        while zeros > k:
            if nums[l] == 0:
                zeros -= 1
            l += 1
        result = max(result, r - l + 1)
    return result


if __name__ == "__main__":
    assert longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
    assert longest_ones([1, 1, 1], 0) == 3
    print("All tests passed.")
