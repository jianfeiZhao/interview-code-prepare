"""
目标和
LeetCode #494 (Medium)
高频考点: 字节跳动 / 腾讯

题目描述
---------
给你一个整数数组 nums 和一个整数 target。向数组中的每个整数前添加 '+' 或 '-'，
然后串联起所有整数，可以构造一个表达式。返回可以通过上述方法构造的、运算结果等于 target 的不同表达式的数目。

示例
------
输入: nums = [1,1,1,1,1], target = 3
输出: 5  （共 5 种方式，如 -1+1+1+1+1=3）

输入: nums = [1], target = 1
输出: 1

约束
------
- 1 <= nums.length <= 20，0 <= nums[i] <= 1000
- 0 <= sum(nums[i]) <= 1000，-1000 <= target <= 1000

============================================================
TL;DR
============================================================
问题：给每个数加 + 或 - 号，求结果等于 target 的方案数。

方法A - DFS + 记忆化: O(n * sum)
  dfs(i, remain) = 从第 i 个数开始、剩余目标为 remain 的方案数

方法B - 0-1 背包转化 O(n * sum):
  设加正号的数之和为 P，加负号的数之和为 N。
  P - N = target  且  P + N = sum
  → P = (sum + target) / 2
  等价于：从 nums 中选若干数使其和恰好为 P（每个只用一次）
  → 0-1 背包计数：dp[j] += dp[j - num]，内层逆序

关键：(sum + target) 必须为非负偶数，否则返回 0。
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：DFS + 记忆化（直观）
# ─────────────────────────────────────────────
def find_target_sum_ways_dfs(nums: List[int], target: int) -> int:
    """
    时间: O(n * sum)，空间: O(n * sum)（memo 大小）
    """
    memo = {}

    def dfs(i: int, remain: int) -> int:
        if i == len(nums):
            return 1 if remain == 0 else 0
        if (i, remain) in memo:
            return memo[(i, remain)]
        result = dfs(i + 1, remain - nums[i]) + dfs(i + 1, remain + nums[i])
        memo[(i, remain)] = result
        return result

    return dfs(0, target)


# ─────────────────────────────────────────────
# 方法2：0-1 背包转化（最优）
# ─────────────────────────────────────────────
def find_target_sum_ways(nums: List[int], target: int) -> int:
    """
    转化推导：
      设正数集合和为 P，则 P = (sum + target) / 2
      问题变为：从 nums 选若干数（每个只用一次）使和恰好等于 P，求方案数。

    0-1 背包计数：
      dp[j] = 和为 j 的方案数
      转移：dp[j] += dp[j - num]（逆序遍历）

    时间: O(n * P)，空间: O(P)
    """
    total = sum(nums)
    # 不可能情况：target 超范围，或 (sum+target) 不是偶数
    if abs(target) > total or (total + target) % 2 != 0:
        return 0

    positive_sum = (total + target) // 2

    dp = [0] * (positive_sum + 1)
    dp[0] = 1  # 空集，和为 0，1 种方案

    for num in nums:
        for j in range(positive_sum, num - 1, -1):
            dp[j] += dp[j - num]

    return dp[positive_sum]


# ─────────────────────────────────────────────
# 扩展：输出所有满足条件的方案
# ─────────────────────────────────────────────
def find_target_sum_all_paths(nums: List[int], target: int) -> List[List[str]]:
    """
    返回所有使结果等于 target 的符号分配方案。
    每个方案以 ['+','-',...] 形式返回。
    纯 DFS 枚举，适合小规模输出。
    """
    result = []

    def dfs(i: int, remain: int, path: List[str]):
        if i == len(nums):
            if remain == 0:
                result.append(path[:])
            return
        path.append('+')
        dfs(i + 1, remain - nums[i], path)
        path.pop()
        path.append('-')
        dfs(i + 1, remain + nums[i], path)
        path.pop()

    dfs(0, target, [])
    return result


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_target_sum():
    # 基本用例
    cases = [
        ([1, 1, 1, 1, 1], 3, 5),    # C(5,4)=5种（选4个正号）
        ([1], 1, 1),
        ([1], -1, 1),
        ([1, 0], 1, 2),             # +1+0 or +1-0 都行，0无影响
        ([0, 0, 0, 0, 0, 0, 0, 0, 1], 1, 256),  # 前8个0有2^8种组合
        ([100], -200, 0),           # 不可能
        ([1, 2, 3, 4, 5], 3, 3),
    ]
    for nums, target, expected in cases:
        r1 = find_target_sum_ways_dfs(nums, target)
        r2 = find_target_sum_ways(nums, target)
        assert r1 == expected, f"dfs({nums},{target})={r1}, expected {expected}"
        assert r2 == expected, f"dp({nums},{target})={r2}, expected {expected}"
    print("find_target_sum_ways: all passed")

    # 验证所有方案枚举
    paths = find_target_sum_all_paths([1, 1, 1, 1, 1], 3)
    assert len(paths) == 5
    for path in paths:
        total = sum((n if s == '+' else -n) for s, n in zip(path, [1, 1, 1, 1, 1]))
        assert total == 3
    print("find_target_sum_all_paths: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_target_sum()
