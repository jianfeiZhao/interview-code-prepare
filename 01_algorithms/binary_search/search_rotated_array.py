"""
题目：搜索旋转排序数组
难度：Medium | 高频出现：字节/阿里/腾讯
标签：二分查找
LeetCode：#33 搜索旋转排序数组，#81 存在重复元素

题目描述
---------
给定一个原本升序排列但在某个未知下标处旋转过的整数数组 nums（元素互不相同）和目标值 target。
在数组中搜索 target，若存在则返回其下标，否则返回 -1。必须在 O(log n) 时间内完成。
#81 为含重复元素的变体，返回布尔值表示 target 是否存在。

示例
------
输入: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
输出: 4

输入: nums = [4, 5, 6, 7, 0, 1, 2], target = 3
输出: -1

约束
------
- 1 <= len(nums) <= 5000
- -10^4 <= nums[i], target <= 10^4
- nums 中每个元素互不相同（#81 允许重复）

TL;DR（30秒速览）
- 二分时判断哪半部分是有序的，再判断目标在哪半
- #81（含重复）：当 nums[l]==nums[m] 时 l++ 缩减范围
- 时间 O(log n)，空间 O(1)

详细解析
---------
旋转数组二分的关键：
  每次mid将数组分为两半，其中至少有一半是有序的
  若 nums[l] <= nums[m]：左半有序
    若 nums[l] <= target < nums[m]：在左半，r=m-1
    否则在右半，l=m+1
  否则：右半有序
    若 nums[m] < target <= nums[r]：在右半，l=m+1
    否则在左半，r=m-1
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[l] <= nums[m]:  # 左半有序
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        else:  # 右半有序
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return -1


def search_with_duplicates(nums: List[int], target: int) -> bool:
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return True
        if nums[l] == nums[m]:  # 无法判断哪半有序
            l += 1
        elif nums[l] < nums[m]:  # 左半有序
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        else:  # 右半有序
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return False


if __name__ == "__main__":
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search([1], 0) == -1
    assert search([1, 3], 3) == 1

    assert search_with_duplicates([2, 5, 6, 0, 0, 1, 2], 0) is True
    assert search_with_duplicates([2, 5, 6, 0, 0, 1, 2], 3) is False
    print("All tests passed.")
