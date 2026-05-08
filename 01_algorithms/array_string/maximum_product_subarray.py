"""
题目：乘积最大子数组
难度：Medium | 高频出现：字节/阿里/腾讯
标签：动态规划、数组
LeetCode：#152

题目描述
---------
给定一个整数数组 nums，找出一个连续子数组（至少包含一个元素），使得该子数组中所有整数的乘积最大。
返回该子数组对应的最大乘积。与最大子数组和不同，乘积存在"负负得正"的特性，需要同时跟踪最大值与最小值。

示例
------
输入: nums = [2, 3, -2, 4]
输出: 6  （子数组 [2, 3]）

输入: nums = [-2, 3, -4]
输出: 24  （子数组 [-2, 3, -4]）

约束
------
- 1 <= nums.length <= 2 * 10⁴
- -10 <= nums[i] <= 10
- 数组中至少有一个元素

TL;DR（30秒速览）
- 同时维护以当前元素结尾的最大值和最小值（负数乘以最小值变最大）
- 时间 O(n)，空间 O(1)

详细解析
---------
与最大子数组和不同：乘积的负负得正特性需要同时跟踪最大和最小。
状态：
  max_prod：以 nums[i] 结尾的最大乘积
  min_prod：以 nums[i] 结尾的最小乘积（可能是大负数）
转移：
  new_max = max(nums[i], max_prod * nums[i], min_prod * nums[i])
  new_min = min(nums[i], max_prod * nums[i], min_prod * nums[i])
"""

from typing import List


def max_product(nums: List[int]) -> int:
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    return result


if __name__ == "__main__":
    assert max_product([2, 3, -2, 4]) == 6
    assert max_product([-2, 0, -1]) == 0
    assert max_product([-2, 3, -4]) == 24
    assert max_product([0, 2]) == 2
    assert max_product([-2]) == -2
    print("All tests passed.")
