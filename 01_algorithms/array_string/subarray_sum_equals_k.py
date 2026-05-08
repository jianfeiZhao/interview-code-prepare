"""
题目：和为 K 的子数组
难度：Medium | 高频出现：字节/阿里/腾讯/微软
标签：数组、哈希表、前缀和
LeetCode：#560 Subarray Sum Equals K

题目描述
---------
给定一个整数数组 nums 和一个整数 k，统计数组中连续子数组（至少含一个元素）的和恰好等于 k 的子数组个数。
数组中元素可以为负数，不能用滑动窗口，需用前缀和 + 哈希表解决。

示例
------
输入: nums = [1, 1, 1], k = 2
输出: 2  （[1,1] 出现两次）

输入: nums = [1, 2, 3], k = 3
输出: 2  （[1,2] 和 [3]）

约束
------
- 1 <= nums.length <= 2 * 10⁴
- -1000 <= nums[i] <= 1000
- -10⁷ <= k <= 10⁷

TL;DR（30秒速览）
- 核心思路：前缀和 prefix[i] - prefix[j] == k 等价于 prefix[j] == prefix[i] - k，
  用哈希表存前缀和出现次数，O(1) 查询
- 时间 O(n)，空间 O(n)
- 关键陷阱：哈希表初始化 {0: 1}（空前缀），处理子数组从头开始的情况

详细解析
---------
方法一：暴力 O(n²)
  枚举所有 [i, j] 区间，累加判断，适合理解问题但超时

方法二：前缀和 + 哈希表（推荐）
  定义 prefix[i] = nums[0] + ... + nums[i-1]（prefix[0] = 0）
  子数组 nums[j..i-1] 的和 = prefix[i] - prefix[j]
  问题转化：统计有多少对 (j, i) 使得 prefix[i] - prefix[j] == k
           即 prefix[j] == prefix[i] - k

  做法：
    - count_map = {0: 1}（空前缀，处理从 index 0 开始的子数组）
    - 遍历，维护当前前缀和 curr
    - ans += count_map.get(curr - k, 0)
    - count_map[curr] += 1（先查询再记录，避免重复使用同一位置）

  关键顺序：先查询再记录（反之会统计到长度为0的子数组）

扩展题：
  #974 和可被 K 整除的子数组（前缀和取模 + 哈希表）
  #523 连续的子数组和（前缀和取模，判断 map 中是否有相同余数且长度>=2）
"""

from typing import List
from collections import defaultdict


def subarray_sum_brute(nums: List[int], k: int) -> int:
    """
    方法一：暴力双层循环，O(n²) 时间，O(1) 空间。
    """
    count = 0
    n = len(nums)
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total == k:
                count += 1
    return count


def subarray_sum(nums: List[int], k: int) -> int:
    """
    方法二：前缀和 + 哈希表，O(n) 时间，O(n) 空间。
    """
    count_map = defaultdict(int)
    count_map[0] = 1     # 空前缀，处理从 index 0 开始的有效子数组
    curr = 0
    ans = 0

    for num in nums:
        curr += num                          # 当前前缀和
        ans += count_map[curr - k]           # 查询之前有多少前缀和等于 curr-k
        count_map[curr] += 1                 # 记录当前前缀和（先查询再记录）

    return ans


def subarray_sum_annotated(nums: List[int], k: int) -> int:
    """
    方法二的等价写法，更清晰注释版。
    """
    prefix_count = {0: 1}   # {前缀和: 出现次数}
    prefix_sum = 0
    result = 0

    for i, num in enumerate(nums):
        prefix_sum += num
        # 若存在 prefix_sum - k 的前缀和，说明从那个位置到当前位置的子数组和为 k
        need = prefix_sum - k
        if need in prefix_count:
            result += prefix_count[need]
        # 更新当前前缀和出现次数（必须在查询之后）
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return result


if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1], 2, 2),                    # [1,1] x2
        ([1, 2, 3], 3, 2),                    # [1,2] 和 [3]
        ([1, -1, 1, -1, 1], 0, 4),            # 含负数
        ([-1, -1, 1], 0, 1),
        ([1], 1, 1),
        ([1], 0, 0),
        ([0, 0, 0, 0], 0, 10),               # 全0，C(5,2)=10
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ]

    for nums, k, expected in test_cases:
        r1 = subarray_sum_brute(nums, k)
        r2 = subarray_sum(nums, k)
        r3 = subarray_sum_annotated(nums, k)
        assert r1 == r2 == r3 == expected, \
            f"input={nums}, k={k}: brute={r1}, hash={r2}, anno={r3}, expected={expected}"

    print("All tests passed.")
