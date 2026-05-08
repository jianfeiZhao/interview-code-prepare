"""
题目：K 个不同整数的子数组
难度：Hard | 高频出现：字节/阿里
标签：滑动窗口、哈希表、数组
LeetCode：#992

题目描述
---------
给定整数数组 nums 和正整数 k，返回恰好包含 k 个不同整数的子数组数目。
子数组是数组中连续的部分，不同整数是指数值不同（相同值只计一种）。

示例
------
输入: nums = [1, 2, 1, 2, 3], k = 2
输出: 7  # [1,2],[2,1],[1,2],[2,3],[1,2,1],[2,1,2],[1,2,1,2] 共7个

输入: nums = [1, 2, 1, 3, 4], k = 3
输出: 3  # [1,2,1,3],[2,1,3],[1,3,4] 共3个

约束
------
- 1 <= len(nums) <= 2 * 10^4
- 1 <= nums[i] <= len(nums)
- 1 <= k <= len(nums)

TL;DR（30秒速览）
- 恰好 K 个不同整数 = at_most(K) - at_most(K-1)
- at_most(k)：扩展右端，收缩左端使窗口内不同整数 <= k，贡献 right - left + 1 个子数组
- 时间 O(n)，空间 O(n)
- 关键陷阱：at_most 模板计数时每次扩展右端后累加 right - left + 1（以 right 结尾的子数组数）

详细解析
---------
核心思路（转化）：
  恰好 K 个 = 至多 K 个 - 至多 K-1 个
  这是滑动窗口计数的经典转化，因为"恰好"的窗口不好直接维护。

at_most(k) 模板：
  freq 记录窗口内每个数字的频率
  distinct 记录当前不同整数数量
  每次右端加入新元素：
    若 freq[num] == 0（新数字），distinct += 1
    freq[num] += 1
  若 distinct > k，收缩左端直到 distinct <= k：
    freq[left] -= 1
    若 freq[left] == 0，distinct -= 1
    left += 1
  此时以 right 结尾的合法子数组数 = right - left + 1
  累加到结果。
"""

from typing import List
from collections import defaultdict


def subarrays_with_k_distinct(nums: List[int], k: int) -> int:
    def at_most(limit: int) -> int:
        """至多 limit 个不同整数的子数组数"""
        freq: dict = defaultdict(int)
        distinct = 0
        left = 0
        count = 0

        for right, num in enumerate(nums):
            if freq[num] == 0:
                distinct += 1
            freq[num] += 1

            # 收缩左端，确保不同整数 <= limit
            while distinct > limit:
                freq[nums[left]] -= 1
                if freq[nums[left]] == 0:
                    distinct -= 1
                left += 1

            # 以 right 结尾、左端在 [left, right] 的所有子数组均合法
            count += right - left + 1

        return count

    return at_most(k) - at_most(k - 1)


if __name__ == "__main__":
    assert subarrays_with_k_distinct([1, 2, 1, 2, 3], 2) == 7
    assert subarrays_with_k_distinct([1, 2, 1, 3, 4], 3) == 3
    assert subarrays_with_k_distinct([1], 1) == 1
    assert subarrays_with_k_distinct([1, 2, 1, 2, 3], 1) == 4

    print("All tests passed.")
