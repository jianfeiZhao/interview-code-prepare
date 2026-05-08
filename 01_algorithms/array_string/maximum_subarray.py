"""
题目：最大子数组和（Kadane 算法）
难度：Medium | 高频出现：字节/阿里/腾讯/美团/百度（全系）
标签：数组、动态规划、分治
LeetCode：#53


题目描述
---------
给你一个整数数组 nums，请你找出一个具有最大和的连续子数组
（子数组最少包含一个元素），返回其最大和。

示例
------
输入: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
输出: 6  （子数组 [4,-1,2,1] 的和最大）

输入: nums = [1]
输出: 1

约束
------
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

TL;DR（30秒速览）
- 思路：Kadane 算法——当前子数组若为负则「断开」重新从当前元素开始
- 时间：O(n)  空间：O(1)
- 陷阱：全为负数时答案是最大的负数，不能返回 0；需用实际最大值初始化

详细解析
---------
暴力法：枚举所有 (i,j) 子数组 O(n²)，不可接受。

分治法：O(n log n)，将区间一分为二，答案在左/右/跨中点三者之一；
  面试中偶有考查，但实现复杂，不如 Kadane。

Kadane 动态规划（最优）：
  定义 dp[i] = 以 nums[i] 结尾的子数组的最大和。
  转移：dp[i] = max(nums[i], dp[i-1] + nums[i])
           = nums[i] + max(0, dp[i-1])
  若 dp[i-1] < 0，则抛弃前段，重新从 nums[i] 开始。
  答案 = max(dp[0..n-1])。

空间优化：dp[i] 只依赖 dp[i-1]，用滚动变量 cur 替代数组，O(1) 空间。

进阶：若还需返回子数组的起止下标，额外维护 start/end/temp_start 即可。
"""

from typing import List, Tuple


def max_sub_array(nums: List[int]) -> int:
    """返回最大子数组和（Kadane 算法）。"""
    cur = best = nums[0]
    for num in nums[1:]:
        cur = num + max(0, cur)
        best = max(best, cur)
    return best


def max_sub_array_with_indices(nums: List[int]) -> Tuple[int, int, int]:
    """返回 (最大和, 起始下标, 结束下标)。"""
    best = cur = nums[0]
    best_start = best_end = temp_start = 0

    for i in range(1, len(nums)):
        if cur < 0:
            cur = nums[i]
            temp_start = i
        else:
            cur += nums[i]

        if cur > best:
            best = cur
            best_start = temp_start
            best_end = i

    return best, best_start, best_end


if __name__ == "__main__":
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_sub_array([1]) == 1
    assert max_sub_array([5, 4, -1, 7, 8]) == 23
    assert max_sub_array([-1]) == -1                  # 全负
    assert max_sub_array([-2, -1]) == -1              # 全负，返回最大负数

    val, s, e = max_sub_array_with_indices([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert val == 6 and s == 3 and e == 6             # nums[3:7] = [4,-1,2,1]

    print("All tests passed.")
