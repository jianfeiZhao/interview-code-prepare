"""
最长递增子序列 (LIS)
LeetCode #300 (Medium)
高频考点: 字节跳动 / 阿里巴巴

============================================================

题目描述
---------
给你一个整数数组 nums，找到其中最长严格递增子序列的长度。
子序列是由数组派生而来的序列，可以删除（或不删除）数组中的元素而不改变其余元素的顺序。

示例
------
输入: nums = [10, 9, 2, 5, 3, 7, 101, 18]
输出: 4  （[2,3,7,101]）

输入: nums = [0,1,0,3,2,3]
输出: 4

约束
------
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

TL;DR
============================================================
方法1 - DP O(n^2):
  状态: dp[i] = 以 nums[i] 结尾的 LIS 长度
  转移: dp[i] = max(dp[j] + 1)  for j < i if nums[j] < nums[i]
  答案: max(dp)

方法2 - 贪心 + 二分 O(n log n):
  维护一个"耐心牌堆" tails，tails[i] = 长度为 i+1 的递增子序列的最小末尾元素
  对每个 nums[x]：
    若 nums[x] > tails[-1]，追加（LIS 变长）
    否则二分找第一个 >= nums[x] 的位置，替换（维护最优末尾）
  答案: len(tails)

关键：tails 数组本身不是 LIS，只是长度记录的辅助结构。
============================================================
"""

from typing import List
import bisect


# ─────────────────────────────────────────────
# 方法1：DP O(n^2)
# ─────────────────────────────────────────────
def lis_dp(nums: List[int]) -> int:
    """
    时间: O(n^2)，空间: O(n)
    适合数据规模 n <= 1000。
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# ─────────────────────────────────────────────
# 方法2：贪心 + 二分 O(n log n)
# ─────────────────────────────────────────────
def lis_binary_search(nums: List[int]) -> int:
    """
    tails[i] 记录长度为 i+1 的所有递增子序列中，末尾元素的最小值。
    tails 始终有序（单调递增），因此可以用二分查找。

    bisect_left(tails, x) 找到第一个 >= x 的位置:
      - 等于 len(tails)：x 比所有末尾都大，LIS 变长，追加
      - 否则：替换 tails[pos]，维护"相同长度下最小末尾"

    时间: O(n log n)，空间: O(n)
    """
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)  # 找第一个 >= x 的位置
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ─────────────────────────────────────────────
# 扩展1：输出具体的 LIS（路径还原）
# ─────────────────────────────────────────────
def lis_with_path(nums: List[int]) -> List[int]:
    """
    在 DP 基础上维护前驱数组 prev，回溯还原路径。
    返回一条最长递增子序列（若有多条，返回字典序任意一条）。
    """
    if not nums:
        return []
    n = len(nums)
    dp = [1] * n
    prev = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 找最大 dp 值的末尾位置
    max_len = max(dp)
    end = dp.index(max_len)

    # 回溯路径
    path = []
    idx = end
    while idx != -1:
        path.append(nums[idx])
        idx = prev[idx]
    path.reverse()
    return path


# ─────────────────────────────────────────────
# 扩展2：最长非递减子序列（允许相等元素）
# ─────────────────────────────────────────────
def lis_non_decreasing(nums: List[int]) -> int:
    """
    将 bisect_left 改为 bisect_right，允许相等元素出现在同一序列中。
    """
    tails = []
    for x in nums:
        pos = bisect.bisect_right(tails, x)  # 允许等于，找第一个 > x 的位置
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ─────────────────────────────────────────────
# 扩展3：俄罗斯套娃信封 (#354) — 二维 LIS
# ─────────────────────────────────────────────
def max_envelopes(envelopes: List[List[int]]) -> int:
    """
    LeetCode #354 Hard: 每个信封 [w, h]，只有 w 和 h 都严格小于另一个才能套入。
    策略：按 w 升序、w 相同时按 h 降序排列，然后对 h 求 LIS。
    w 相同时 h 降序可避免同 w 的信封互相套入（因为 LIS 只取一个）。
    """
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    heights = [e[1] for e in envelopes]
    return lis_binary_search(heights)


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_lis():
    cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),  # [2,3,7,101]
        ([0, 1, 0, 3, 2, 3], 4),             # [0,1,2,3]
        ([7, 7, 7, 7], 1),                   # 严格递增，只能选一个
        ([1], 1),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
    ]
    for nums, expected in cases:
        r1 = lis_dp(nums)
        r2 = lis_binary_search(nums)
        assert r1 == expected, f"lis_dp({nums}) = {r1}, expected {expected}"
        assert r2 == expected, f"lis_binary_search({nums}) = {r2}, expected {expected}"
    print("lis_dp & lis_binary_search: all passed")

    # 路径还原
    path = lis_with_path([10, 9, 2, 5, 3, 7, 101, 18])
    assert len(path) == 4
    for i in range(1, len(path)):
        assert path[i] > path[i - 1], f"Path not strictly increasing: {path}"
    print(f"lis_with_path: {path}")

    # 非递减
    assert lis_non_decreasing([1, 3, 3, 5]) == 4
    assert lis_non_decreasing([1, 2, 3]) == 3
    print("lis_non_decreasing: all passed")

    # 俄罗斯套娃
    assert max_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3  # [2,3]->[5,4]->[6,7]
    assert max_envelopes([[1, 1], [1, 1], [1, 1]]) == 1
    print("max_envelopes: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_lis()
