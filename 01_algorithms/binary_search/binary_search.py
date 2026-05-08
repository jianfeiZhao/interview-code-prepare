"""
题目：二分查找（模板 + 变体）
难度：Easy | 高频出现：全系大厂
标签：二分查找
LeetCode：#704


题目描述
---------
给定一个按照升序排列的整数数组 nums 和一个目标值 target，
写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。
要求时间复杂度为 O(log n)。

示例
------
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4

输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1

约束
------
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- nums 中的所有元素互不相同，nums 按升序排列

TL;DR（30秒速览）
- 思路：[left, right] 闭区间，mid = left + (right-left)//2 防溢出
- 时间：O(log n)  空间：O(1)
- 陷阱：while left <= right（包含等号）；找不到时返回 -1

详细解析
---------
三种模板：
1. 精确查找：找到目标即返回
2. 查找左边界（第一个 >= target 的位置）
3. 查找右边界（最后一个 <= target 的位置）

二分核心思路：
  每轮将搜索空间减半，关键是"什么时候该收缩哪侧边界"
  用 bisect 模块可快速完成标准操作
"""

from typing import List
import bisect


def search(nums: List[int], target: int) -> int:
    """标准二分查找，返回目标下标，不存在返回 -1"""
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def search_left_bound(nums: List[int], target: int) -> int:
    """查找第一个 >= target 的下标（左边界）"""
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left  # 等价于 bisect.bisect_left(nums, target)


def search_right_bound(nums: List[int], target: int) -> int:
    """查找最后一个 <= target 的下标（右边界）"""
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left - 1  # 等价于 bisect.bisect_right(nums, target) - 1


if __name__ == "__main__":
    assert search([-1,0,3,5,9,12], 9) == 4
    assert search([-1,0,3,5,9,12], 2) == -1
    assert search_left_bound([1,2,2,2,3], 2) == 1
    assert search_right_bound([1,2,2,2,3], 2) == 3
    # 验证与 bisect 一致
    assert search_left_bound([1,2,2,2,3], 2) == bisect.bisect_left([1,2,2,2,3], 2)
    print("All tests passed.")
