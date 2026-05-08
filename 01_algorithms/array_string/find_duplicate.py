"""
题目：寻找重复数
难度：Medium | 高频出现：字节/阿里/腾讯
标签：数组、双指针、Floyd判圈算法、二分查找
LeetCode：#287

题目描述
---------
给定一个包含 n+1 个整数的数组 nums，其中每个整数在 [1, n] 之间，因此至少存在一个重复数字。
假设只有一个重复的整数，找出这个重复数并返回。
要求不修改原数组，且只使用常数额外空间（不能用哈希集合）。

示例
------
输入: nums = [1, 3, 4, 2, 2]
输出: 2

输入: nums = [3, 1, 3, 4, 2]
输出: 3

约束
------
- 1 <= n <= 10⁵，数组长度为 n+1
- 每个元素满足 1 <= nums[i] <= n
- 只有一个重复数字，但可能重复多次

TL;DR（30秒速览）
- 思路：把数组当链表（i → nums[i]），必有环，用 Floyd 龟兔算法找环入口
- 时间：O(n)  空间：O(1)
- 陷阱：题目要求不修改数组、不用额外空间，排除排序/哈希/修改原数组解法

详细解析
---------
题目约束：n+1 个整数，范围 [1,n]，恰好有一个重复，不能修改数组，O(1) 额外空间。

方法1：哈希集合 O(n) 空间 —— 违反空间约束，不符合要求。

方法2：排序后找相邻重复 O(n log n) —— 违反不修改约束。

方法3：二分答案 O(n log n) O(1)：
  对 mid = (lo+hi)//2，统计 nums 中 <= mid 的个数。
  若 count > mid，重复数在 [lo, mid]；否则在 [mid+1, hi]。

方法4：Floyd 判圈（最优 O(n) O(1)）：
  构造隐式链表：从下标 0 出发，0 → nums[0] → nums[nums[0]] → ...
  因有重复，必有环。
  - 阶段1：快慢指针找相遇点（快指针每步走2，慢指针每步走1）。
  - 阶段2：将慢指针移到 0，快指针留在相遇点，两者同速前进，
    再次相遇即环入口 = 重复数。
  原理同链表找环入口（LeetCode #142）。
"""

from typing import List


# ---- Floyd 判圈 O(n) O(1) ----
def find_duplicate_floyd(nums: List[int]) -> int:
    slow, fast = nums[0], nums[nums[0]]

    # 阶段1：找相遇点
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # 阶段2：找环入口
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


# ---- 二分答案 O(n log n) O(1) ----
def find_duplicate_binary(nums: List[int]) -> int:
    lo, hi = 1, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(1 for x in nums if x <= mid)
        if count > mid:
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    cases = [
        ([1, 3, 4, 2, 2], 2),
        ([3, 1, 3, 4, 2], 3),
        ([1, 1], 1),
        ([1, 1, 2], 1),
        ([2, 2, 2, 2, 2], 2),
    ]
    for nums, expected in cases:
        assert find_duplicate_floyd(nums) == expected, f"Floyd failed on {nums}"
        assert find_duplicate_binary(nums) == expected, f"Binary failed on {nums}"
    print("All tests passed.")
