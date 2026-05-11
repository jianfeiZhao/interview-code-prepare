"""
题目：两数之和
难度：Easy | 高频出现：字节/阿里/腾讯/美团
标签：哈希表、数组
LeetCode：#1


题目描述
---------
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出
和为目标值 target 的那两个整数，并返回它们的数组下标。
可以假设每种输入只对应一个答案，且同一元素不能使用两次。
可以按任意顺序返回答案。

示例
------
输入: nums = [2, 7, 11, 15], target = 9
输出: [0, 1]  （nums[0] + nums[1] = 2 + 7 = 9）

输入: nums = [3, 2, 4], target = 6
输出: [1, 2]

约束
------
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- 只有一个有效答案

TL;DR（30秒速览）
- 思路：哈希表记录「目标值-当前值」，遍历时查表
- 时间：O(n)  空间：O(n)
- 陷阱：同一元素不能使用两次，注意用下标区分

详细解析
---------
暴力法：两重循环 O(n²)，面试不可接受。

哈希表法：
  遍历 nums[i]，查找 target - nums[i] 是否已在表中。
  若在 → 返回两个下标。
  若不在 → 把 nums[i] 存入表（key=值, value=下标）。
  只需一次遍历，边查边存，避免用到自身。
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def two_sum_v2(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        num2 = target - num 
        if num2 in seen:
            return [seen[num2], i]
        seen[num] = i
    return []


if __name__ == "__main__":
    assert two_sum_v2([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_v2([3, 2, 4], 6) == [1, 2]
    assert two_sum_v2([3, 3], 6) == [0, 1]
    print("All tests passed.")
