"""
LeetCode #169 - 多数元素 (Majority Element)
难度: Easy | 频率: 全系必考

=== 题目描述 ===
给定一个大小为 n 的数组 nums，返回其中的多数元素。多数元素是指在数组中出现次数大于 ⌊n/2⌋ 的元素。
你可以假设数组是非空的，并且给定的数组总是存在多数元素。

示例 1: 输入: nums = [3,2,3]          输出: 3
示例 2: 输入: nums = [2,2,1,1,1,2,2]  输出: 2

进阶: 尝试设计时间复杂度为 O(n)、空间复杂度为 O(1) 的算法解决此问题。

=== TL;DR ===
核心思路:
  方法1（哈希计数）: 统计每个元素频次，返回频次 > n/2 的元素 — O(n) 时间，O(n) 空间
  方法2（排序）: 排序后中间位置必然是多数元素 — O(n log n) 时间，O(1) 空间
  方法3（Boyer-Moore 投票）: 维护候选元素和计数器，票数归零时换候选 — O(n) 时间，O(1) 空间（最优）

时间复杂度: O(n)
空间复杂度: O(1)（Boyer-Moore）

=== 详细解析 ===
Boyer-Moore 投票算法核心:
1. 维护 candidate（候选人）和 count（票数）
2. 遍历数组: 若 count==0，更新候选为当前元素
3. 若当前元素 == candidate，count++；否则 count--
4. 直觉: 多数元素与其他所有元素"对抗"，多数元素的票数永远不会耗尽
5. 此算法依赖多数元素存在的前提（若不保证，还需最后验证一次）
"""

from collections import Counter


# ===== 方法1: 哈希计数 =====
def majority_element_hash(nums: list) -> int:
    count = Counter(nums)
    return max(count, key=count.get)


# ===== 方法2: 排序取中 =====
def majority_element_sort(nums: list) -> int:
    nums.sort()
    return nums[len(nums) // 2]


# ===== 方法3: Boyer-Moore 投票（面试最推荐）=====
def majority_element_boyer_moore(nums: list) -> int:
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate


# ===== 方法4: 位运算（了解即可）=====
def majority_element_bit(nums: list) -> int:
    """对每一位统计1的个数，超过 n/2 则该位为1"""
    n = len(nums)
    result = 0
    for bit in range(32):
        bit_count = sum(1 for num in nums if num & (1 << bit))
        if bit_count > n // 2:
            result |= (1 << bit)
    return result


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [
        majority_element_hash,
        majority_element_sort,
        majority_element_boyer_moore,
        majority_element_bit,
    ]
    cases = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
        ([1, 1, 2], 1),
        ([3, 3, 4], 3),
        ([5, 5, 5, 1, 2], 5),
    ]
    for func in funcs:
        for nums, expected in cases:
            assert func(list(nums)) == expected, \
                f"{func.__name__}({nums}) = {func(list(nums))}, expected {expected}"

    print("All tests passed!")
