"""
题目：移动零
难度：Easy | 高频出现：字节/腾讯
标签：数组、双指针
LeetCode：#283 Move Zeroes

题目描述
---------
给定一个整数数组 nums，将所有 0 移动到数组末尾，同时保持非零元素的相对顺序。
必须在原数组上进行操作，不能拷贝额外数组。

示例
------
输入: nums = [0, 1, 0, 3, 12]
输出: [1, 3, 12, 0, 0]

输入: nums = [0]
输出: [0]

约束
------
- 1 <= nums.length <= 10⁴
- -2³¹ <= nums[i] <= 2³¹ - 1

TL;DR（30秒速览）
- 核心思路：慢指针 slow 记非零写入位置，快指针 fast 扫描非零元素并写入
- 时间 O(n)，空间 O(1)
- 关键陷阱：需保持非零元素的相对顺序；最后将 slow 及之后全置 0

详细解析
---------
方法一：双指针（两步法）
  1. fast 扫描，遇非零：nums[slow] = nums[fast]，slow++
  2. slow 之后全置 0
  操作次数：写入 n-zero_count 次 + 清零 zero_count 次

方法二：双指针（交换法，操作次数更少）
  slow 指向第一个0，fast 指向其后第一个非零
  每次把非零元素与 slow 位置交换，slow++
  好处：只需 zero_count 次交换（而非两趟）
  注意：当 slow == fast 时也可以交换（与自身交换无副作用），可简化逻辑

方法三：类 remove_duplicates 写法（最简洁）
  slow 记写入位置，fast 遇非零就写入，最后补零

对比：
  | 方法       | 时间  | 空间 | 写/交换次数        |
  |------------|-------|------|--------------------|
  | 两步法     | O(n)  | O(1) | n 次写             |
  | 交换法     | O(n)  | O(1) | zero_count 次交换  |
  | remove模板 | O(n)  | O(1) | n 次写             |
"""

from typing import List


def move_zeroes(nums: List[int]) -> None:
    """
    方法一：两步法双指针，O(n) 时间，O(1) 空间。
    Do not return anything, modify nums in-place instead.
    """
    slow = 0
    # Step 1：将所有非零元素依次写入 slow 位置
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
    # Step 2：slow 及之后的位置全部置 0
    for i in range(slow, len(nums)):
        nums[i] = 0


def move_zeroes_swap(nums: List[int]) -> None:
    """
    方法二：交换法，slow 指向第一个0，fast 找非零元素后交换，减少写操作。
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    # 无需额外清零步骤，交换已将0推到末尾


def move_zeroes_clean(nums: List[int]) -> None:
    """
    方法三：最简洁写法，与 remove_duplicates 同构。
    """
    pos = 0
    for x in nums:
        if x != 0:
            nums[pos] = x
            pos += 1
    nums[pos:] = [0] * (len(nums) - pos)


import copy

if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([0, 0, 0], [0, 0, 0]),
        ([1, 2, 3], [1, 2, 3]),
        ([1, 0], [1, 0]),
    ]

    for func in [move_zeroes, move_zeroes_swap, move_zeroes_clean]:
        for nums, expected in test_cases:
            arr = copy.deepcopy(nums)
            func(arr)
            assert arr == expected, f"{func.__name__}: input={nums}, got={arr}, expected={expected}"

    print("All tests passed.")
