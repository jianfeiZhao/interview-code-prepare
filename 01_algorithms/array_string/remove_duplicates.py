"""
题目：删除有序数组中的重复项 / 最多保留两次
难度：Easy / Medium | 高频出现：字节/阿里/腾讯
标签：数组、双指针
LeetCode：#26 Remove Duplicates from Sorted Array / #80 Remove Duplicates II


题目描述
---------
给你一个非严格递增排列的数组 nums，请你原地删除重复出现的元素，
使每个元素只出现一次，返回删除后数组的新长度。
不要使用额外的数组空间，必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

示例
------
输入: nums = [1,1,2]
输出: 2, nums = [1,2,_]

输入: nums = [0,0,1,1,1,2,2,3,3,4]
输出: 5, nums = [0,1,2,3,4,_,_,_,_,_]

约束
------
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100，nums 已按升序排列

TL;DR（30秒速览）
- #26：慢指针 slow 记写入位置，快指针 fast 找下一个不重复元素
- #80：通用模板：每个元素与 nums[slow-k] 比较（k=2），可复用到最多保留k次
- 时间 O(n)，空间 O(1)
- 关键陷阱：返回值是新长度 k，前 k 个元素合法；原地修改，不需要 new 数组

详细解析
---------
#26（最多保留1个）：
  slow 从 1 开始，fast 从 1 开始扫描：
    - nums[fast] != nums[slow-1]：写入 nums[slow]，slow++
    - 否则跳过（重复元素）

#80（最多保留2个）：
  通用化：k=2，slow 从 2 开始，fast 从 2 开始扫描：
    - nums[fast] != nums[slow-2]：写入 nums[slow]，slow++
    - 否则跳过

  为什么 nums[fast] != nums[slow-k] 就可以写入？
    因为有序数组中，若当前写入位置前 k 个都是同一值，再写就超过 k 次了；
    若不同，则当前值要么是新值，要么是该值第 <= k 次出现，均合法。

通用模板（最多保留 k 个）：
  def remove_duplicates_k(nums, k):
      slow = 0
      for fast in range(len(nums)):
          if slow < k or nums[fast] != nums[slow - k]:
              nums[slow] = nums[fast]
              slow += 1
      return slow
"""

from typing import List


def remove_duplicates_26(nums: List[int]) -> int:
    """
    #26：删除有序数组重复项，每个元素只保留一次。
    O(n) 时间，O(1) 空间。
    """
    if not nums:
        return 0

    slow = 1  # slow 指向下一个写入位置
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow - 1]:   # 遇到新元素
            nums[slow] = nums[fast]
            slow += 1

    return slow


def remove_duplicates_80(nums: List[int]) -> int:
    """
    #80：删除有序数组重复项，每个元素最多保留两次。
    O(n) 时间，O(1) 空间。
    """
    slow = 0
    for fast in range(len(nums)):
        # slow < 2：前两个元素无条件保留
        # nums[fast] != nums[slow-2]：当前元素与写入区倒数第2个不同，可写入
        if slow < 2 or nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1

    return slow


def remove_duplicates_k(nums: List[int], k: int) -> int:
    """
    通用版：有序数组中每个元素最多保留 k 次。
    O(n) 时间，O(1) 空间。
    """
    slow = 0
    for fast in range(len(nums)):
        if slow < k or nums[fast] != nums[slow - k]:
            nums[slow] = nums[fast]
            slow += 1
    return slow


if __name__ == "__main__":
    # #26 测试
    nums = [1, 1, 2]
    k = remove_duplicates_26(nums)
    assert k == 2 and nums[:k] == [1, 2], f"Got k={k}, nums={nums[:k]}"

    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates_26(nums)
    assert k == 5 and nums[:k] == [0, 1, 2, 3, 4]

    # 空数组
    assert remove_duplicates_26([]) == 0

    # #80 测试
    nums = [1, 1, 1, 2, 2, 3]
    k = remove_duplicates_80(nums)
    assert k == 5 and nums[:k] == [1, 1, 2, 2, 3], f"Got k={k}, nums={nums[:k]}"

    nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    k = remove_duplicates_80(nums)
    assert k == 7 and nums[:k] == [0, 0, 1, 1, 2, 3, 3]

    # 通用版验证
    nums = [1, 1, 1, 2, 2, 3]
    assert remove_duplicates_k(nums[:], 1) == 3
    assert remove_duplicates_k(nums[:], 2) == 5
    assert remove_duplicates_k(nums[:], 3) == 6

    print("All tests passed.")
