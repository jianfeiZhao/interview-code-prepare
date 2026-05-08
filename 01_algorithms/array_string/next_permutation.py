"""
题目：下一个排列
难度：Medium | 高频出现：字节/阿里/腾讯
标签：数组、双指针
LeetCode：#31

题目描述
---------
给定一个整数数组 nums，将其重新排列为字典序中下一个更大的排列。
如果当前排列已经是字典序最大的（即整体降序），则将其重排为字典序最小的排列（即升序）。
必须原地修改数组，只允许使用常数额外空间。

示例
------
输入: nums = [1, 2, 3]
输出: [1, 3, 2]

输入: nums = [3, 2, 1]
输出: [1, 2, 3]

约束
------
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

TL;DR（30秒速览）
- 从右找第一个下降点i，再从右找第一个比nums[i]大的j，交换，然后翻转i+1..末尾
- 时间 O(n)，空间 O(1)，原地修改

详细解析
---------
步骤：
  1. 从右到左找第一个下降点：nums[i] < nums[i+1]
  2. 从右到左找第一个比 nums[i] 大的位置 j，交换 nums[i] 和 nums[j]
  3. 翻转 nums[i+1:] 使其变为最小排列

若找不到下降点（全降序），直接翻转整个数组（最小排列）
"""

from typing import List


def next_permutation(nums: List[int]) -> None:
    n = len(nums)
    i = n - 2
    # 找第一个下降点
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # 从右找第一个比 nums[i] 大的
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # 翻转 i+1 到末尾
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


if __name__ == "__main__":
    nums = [1, 2, 3]
    next_permutation(nums)
    assert nums == [1, 3, 2]

    nums = [3, 2, 1]
    next_permutation(nums)
    assert nums == [1, 2, 3]

    nums = [1, 1, 5]
    next_permutation(nums)
    assert nums == [1, 5, 1]

    nums = [1]
    next_permutation(nums)
    assert nums == [1]
    print("All tests passed.")
