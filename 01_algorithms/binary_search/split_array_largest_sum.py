"""
题目：分割数组的最大值
难度：Hard | 高频出现：字节/阿里
标签：二分查找、动态规划
LeetCode：#410

题目描述
---------
给定整数数组 nums 和正整数 k，将数组分成 k 个非空连续子数组。
最小化所有子数组中最大子数组和，返回该最小值。
每个元素必须恰好属于某一个子数组，子数组必须连续。

示例
------
输入: nums = [7, 2, 5, 10, 8], k = 2
输出: 18  # 分成 [7,2,5] 和 [10,8]，最大和 = 18

输入: nums = [1, 2, 3, 4, 5], k = 2
输出: 9  # 分成 [1,2,3,4] 和 [5]，或 [1,2,3] 和 [4,5]，最优为 9

约束
------
- 1 <= len(nums) <= 1000
- 0 <= nums[i] <= 10^6
- 1 <= k <= min(50, len(nums))

TL;DR（30秒速览）
- 二分答案：在 [max(nums), sum(nums)] 上二分，验证能否用k段使最大段和不超过mid
- 时间 O(n log(sum))，空间 O(1)

详细解析
---------
二分答案模板：
  答案范围：[max(nums), sum(nums)]
  check(mid)：贪心验证，能否将数组分成 <= k 段，每段之和 <= mid
    从左到右累加，超过mid则开一段，统计段数 <= k 则可行

同类问题：#875 爱吃香蕉的珂珂、#1011 在D天内送达包裹的能力
"""

from typing import List


def split_array(nums: List[int], k: int) -> int:
    def can_split(max_sum):
        segments = 1
        cur_sum = 0
        for num in nums:
            if cur_sum + num > max_sum:
                segments += 1
                cur_sum = num
                if segments > k:
                    return False
            else:
                cur_sum += num
        return True

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    assert split_array([7, 2, 5, 10, 8], 2) == 18
    assert split_array([1, 2, 3, 4, 5], 2) == 9
    assert split_array([1, 4, 4], 3) == 4
    assert split_array([2, 3, 1, 2, 4, 3], 5) == 4
    print("All tests passed.")
