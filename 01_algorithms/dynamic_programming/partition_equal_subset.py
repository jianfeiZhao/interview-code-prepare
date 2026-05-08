"""
分割等和子集（布尔背包）
LeetCode #416 (Medium)
高频考点: 字节跳动 / 阿里巴巴

============================================================

题目描述
---------
给你一个只包含正整数的非空数组 nums，请你判断是否可以将这个数组分割成两个子集，
使得两个子集的元素和相等。

示例
------
输入: nums = [1, 5, 11, 5]
输出: True  （[1,5,5] 和 [11]）

输入: nums = [1, 2, 3, 5]
输出: False

约束
------
- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100

TL;DR
============================================================
问题转化: 判断能否从 nums 中选若干数，使子集和 = sum(nums) // 2
等价于 0-1 背包判断可行性问题。

状态: dp[j] = 能否从前 i 个数中选出若干个使和恰好为 j
初始: dp[0] = True，其余 False
转移: dp[j] = dp[j] or dp[j - num]
      内层倒序遍历（0-1 背包，每个数只用一次）
答案: dp[target]，target = total // 2

剪枝：
  - total 为奇数 → False
  - max(nums) > target → False
  - 提前找到 dp[target]=True 可 break
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：0-1 背包布尔 DP（一维滚动数组）
# ─────────────────────────────────────────────
def can_partition(nums: List[int]) -> bool:
    """
    时间: O(n * target)，空间: O(target)
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2

    # 剪枝：单个数已超目标
    if max(nums) > target:
        return False

    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        # 倒序遍历，防止同一数字被重复使用（0-1 背包特征）
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
        if dp[target]:   # 提前终止
            return True
    return dp[target]


# ─────────────────────────────────────────────
# 方法2：位运算优化（Python 大整数）
# ─────────────────────────────────────────────
def can_partition_bitset(nums: List[int]) -> bool:
    """
    用整数的二进制位表示可达集合：bits 的第 j 位为 1 表示可凑出 j。
    bits |= bits << num 等价于一次完整的 0-1 背包布尔更新。

    Python 支持任意长度整数，非常简洁。
    时间: O(n * target / 64)（位运算并行），空间: O(target / 64)
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2

    bits = 1  # 第 0 位为 1，表示可凑出 0
    for num in nums:
        bits |= (bits << num)
    # 检查第 target 位是否为 1
    return bool((bits >> target) & 1)


# ─────────────────────────────────────────────
# 扩展：统计满足条件的子集数量
# (等价于 #494 目标和 的子问题)
# ─────────────────────────────────────────────
def count_subsets_with_sum(nums: List[int], target: int) -> int:
    """
    统计从 nums 中选若干数（每个只能选一次）使和恰好等于 target 的方案数。
    0-1 背包计数版，内层倒序遍历。
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] += dp[j - num]
    return dp[target]


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_partition_equal_subset():
    assert can_partition([1, 5, 11, 5]) is True    # [1,5,5] 和 [11]
    assert can_partition([1, 2, 3, 5]) is False
    assert can_partition([1, 1]) is True
    assert can_partition([1]) is False              # 奇数总和
    assert can_partition([2, 2, 2, 2]) is True
    assert can_partition([100, 100]) is True
    assert can_partition([3, 3, 3, 4, 5]) is True  # [3,3,3]=9, [4,5]=9
    print("can_partition (DP): all passed")

    # 位运算版结果一致
    for nums in [[1, 5, 11, 5], [1, 2, 3, 5], [1, 1], [1], [2, 2, 2, 2]]:
        assert can_partition(nums) == can_partition_bitset(nums), f"mismatch: {nums}"
    print("can_partition_bitset: all passed")

    # 子集计数
    assert count_subsets_with_sum([1, 1, 1, 1, 1], 3) == 10  # C(5,3)=10
    assert count_subsets_with_sum([1, 2, 3], 3) == 2          # [3] or [1,2]
    assert count_subsets_with_sum([3, 3, 3, 4, 5], 9) == 2
    print("count_subsets_with_sum: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_partition_equal_subset()
