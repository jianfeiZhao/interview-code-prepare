"""
题目：有序数组的平方
难度：Easy | 高频出现：字节/阿里
标签：数组、双指针、排序
LeetCode：#977 Squares of a Sorted Array


题目描述
---------
给你一个按非递减顺序排序的整数数组 nums，返回每个数字的平方组成的新数组，
要求也按非递减顺序排序。

示例
------
输入: nums = [-4,-1,0,3,10]
输出: [0,1,9,16,100]

输入: nums = [-7,-3,2,3,11]
输出: [4,9,9,49,121]

约束
------
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums 已按非递减顺序排序

TL;DR（30秒速览）
- 核心思路：双指针从两端向中间，每次将较大平方值从结果数组末尾填入
- 时间 O(n)，空间 O(n)（结果数组）
- 关键陷阱：数组含负数，平方后最大值在两端而非中间；从末尾填入结果避免逆序

详细解析
---------
方法一：暴力排序（不推荐，面试需说明更优解）
  直接平方后排序，O(n log n)，空间 O(n) 或 O(1)（忽略返回值）

方法二：双指针（推荐，O(n)）
  思路：非递减数组，绝对值最大的元素在两端（最左或最右）
  - left 指向左端，right 指向右端
  - 比较两端绝对值大小，较大的平方写入 result[pos]，pos 从末尾倒序
  - 对应指针内移
  - 循环直到 left > right

为什么从尾部填入？
  每次取的是当前最大值，正序写会导致已写位置被覆盖；
  倒序写则每次确定一个最终位置，无需额外操作。
"""

from typing import List


def sorted_squares_sort(nums: List[int]) -> List[int]:
    """
    方法一：暴力平方后排序，O(n log n)。
    """
    return sorted(x * x for x in nums)


def sorted_squares(nums: List[int]) -> List[int]:
    """
    方法二：双指针，O(n) 时间，O(n) 空间。
    """
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    pos = n - 1           # 结果数组从末尾开始填

    while left <= right:
        sq_left = nums[left] * nums[left]
        sq_right = nums[right] * nums[right]

        if sq_left > sq_right:
            result[pos] = sq_left
            left += 1
        else:
            result[pos] = sq_right
            right -= 1

        pos -= 1

    return result


if __name__ == "__main__":
    test_cases = [
        ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
        ([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121]),
        ([-5, -3, -2, -1],   [1, 4, 9, 25]),         # 全负数
        ([0, 1, 2, 3, 4],    [0, 1, 4, 9, 16]),       # 全非负
        ([0],                [0]),                     # 单元素
        ([-1],               [1]),
    ]

    for nums, expected in test_cases:
        assert sorted_squares_sort(nums) == expected, \
            f"sort: input={nums}, got={sorted_squares_sort(nums)}"
        assert sorted_squares(nums[:]) == expected, \
            f"two-ptr: input={nums}, got={sorted_squares(nums[:])}"

    print("All tests passed.")
