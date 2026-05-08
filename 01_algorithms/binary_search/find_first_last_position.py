"""
题目: 在排序数组中查找元素的第一个和最后一个位置
LeetCode: #34 (Medium)
高频公司: 全系（字节、阿里、腾讯、美团等）

题目描述:
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。
请你找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。
你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。

示例 1: nums = [5,7,7,8,8,10], target = 8 -> [3,4]
示例 2: nums = [5,7,7,8,8,10], target = 6 -> [-1,-1]
示例 3: nums = [], target = 0 -> [-1,-1]

================================================================================
TL;DR (核心思路):
  - 两次二分：分别找左边界（第一个 >= target 的位置）和右边界（第一个 > target 的位置 - 1）
  - 左边界：当 nums[mid] >= target 时 right = mid，否则 left = mid + 1
  - 右边界：当 nums[mid] > target 时 right = mid，否则 left = mid + 1；最终结果 -1

时间复杂度: O(log n)
空间复杂度: O(1)
================================================================================
"""

from typing import List


def searchRange(nums: List[int], target: int) -> List[int]:
    """
    两次二分查找定位左右边界。
    """
    if not nums:
        return [-1, -1]

    left_bound = find_left(nums, target)

    # 若左边界不存在（target 不在数组中），直接返回
    if left_bound == len(nums) or nums[left_bound] != target:
        return [-1, -1]

    right_bound = find_right(nums, target)
    return [left_bound, right_bound]


def find_left(nums: List[int], target: int) -> int:
    """
    找第一个 >= target 的索引（lower_bound）。
    返回值范围 [0, len(nums)]，len(nums) 表示不存在。
    """
    left, right = 0, len(nums)  # 左闭右开区间 [left, right)

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] >= target:
            right = mid       # mid 可能就是左边界，缩小右侧
        else:
            left = mid + 1    # nums[mid] < target，左边界在 mid 右侧

    return left  # left == right，即目标左边界位置


def find_right(nums: List[int], target: int) -> int:
    """
    找最后一个 == target 的索引（upper_bound - 1）。
    利用 upper_bound 找第一个 > target 的位置，减 1 即右边界。
    """
    left, right = 0, len(nums)  # 左闭右开区间 [left, right)

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > target:
            right = mid       # 第一个 > target 的位置在 [left, mid]
        else:
            left = mid + 1    # nums[mid] <= target，继续向右

    return left - 1  # upper_bound - 1 = 最后一个等于 target 的位置


def searchRange_single_func(nums: List[int], target: int) -> List[int]:
    """
    将左右边界统一用一个辅助函数实现，通过 bias 参数区分。
    bias=0 找左边界（第一个 >= target），bias=1 找右边界（第一个 >= target+1，然后-1）。
    """
    def lower_bound(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    lb = lower_bound(nums, target)
    if lb == len(nums) or nums[lb] != target:
        return [-1, -1]
    rb = lower_bound(nums, target + 1) - 1
    return [lb, rb]


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    assert searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4], "标准用例"
    assert searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1], "不存在"
    assert searchRange([], 0) == [-1, -1], "空数组"
    assert searchRange([1], 1) == [0, 0], "单元素等于target"
    assert searchRange([1], 2) == [-1, -1], "单元素不等于target"
    assert searchRange([1, 1, 1, 1], 1) == [0, 3], "全等于target"
    assert searchRange([1, 2, 3], 1) == [0, 0], "target在左端"
    assert searchRange([1, 2, 3], 3) == [2, 2], "target在右端"
    assert searchRange([1, 2, 2, 2, 3], 2) == [1, 3], "target在中间"

    # 两种实现结果一致
    test_cases = [
        ([5, 7, 7, 8, 8, 10], 8),
        ([5, 7, 7, 8, 8, 10], 6),
        ([1, 1, 1, 1], 1),
    ]
    for nums, target in test_cases:
        assert searchRange(nums, target) == searchRange_single_func(nums, target)

    print("所有测试通过!")

    # 示例输出
    print(f"[5,7,7,8,8,10], target=8: {searchRange([5,7,7,8,8,10], 8)}")  # [3,4]
    print(f"[5,7,7,8,8,10], target=6: {searchRange([5,7,7,8,8,10], 6)}")  # [-1,-1]
    print(f"[], target=0: {searchRange([], 0)}")                            # [-1,-1]
