"""
题目：等差数列划分
难度：Medium | 高频出现：字节/阿里
标签：动态规划、数组
LeetCode：#413


题目描述
---------
如果一个数列至少有三个元素，并且任意两个相邻元素之差相同，那么这个数列就叫等差数列。
给你一个整数数组 nums，返回数组 nums 中所有为等差数列的子数组数目。

示例
------
输入: nums = [1, 2, 3, 4]
输出: 3  （[1,2,3], [2,3,4], [1,2,3,4]）

输入: nums = [1]
输出: 0

约束
------
- 1 <= nums.length <= 5000
- -1000 <= nums[i] <= 1000

TL;DR（30秒速览）
- dp[i] = 以 i 结尾的等差子数组数量，若差值延续则 dp[i] = dp[i-1] + 1，否则 0
- 时间 O(n)，空间 O(1)（滚动变量）
- 关键陷阱：长度为 k 的等差数列贡献 k-2 个新子数组（而非 1 个）

详细解析
---------
设 diff = A[i] - A[i-1]，若与前一步差值相同，则：
  dp[i] = dp[i-1] + 1
  新增的 dp[i] 个子数组是：长度为 3 的、长度为 4 的 ... 结尾在 i 的所有等差子数组。

举例：[1, 2, 3, 4]
  i=2：diff=1==1，dp=1，ans+=1 → ans=1  [1,2,3]
  i=3：diff=1==1，dp=2，ans+=2 → ans=3  新增 [2,3,4] 和 [1,2,3,4]

总答案 = sum(dp[i]) 等价于每次 ans += dp（当前滚动值）。
"""

from typing import List


def number_of_arithmetic_slices(nums: List[int]) -> int:
    n = len(nums)
    if n < 3:
        return 0

    dp = 0    # 以当前位置结尾的等差子数组数量
    ans = 0

    for i in range(2, n):
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            dp += 1
            ans += dp
        else:
            dp = 0   # 等差关系中断，重置

    return ans


# 方法二：直观的滑动计数（等价）
def number_of_arithmetic_slices_v2(nums: List[int]) -> int:
    """统计每段连续等差序列的贡献"""
    n = len(nums)
    ans = 0
    i = 1

    while i < n - 1:
        if nums[i + 1] - nums[i] == nums[i] - nums[i - 1]:
            # 找到等差段，计算这段的长度
            length = 3
            i += 1
            while i < n - 1 and nums[i + 1] - nums[i] == nums[i] - nums[i - 1]:
                length += 1
                i += 1
            # 长度为 k 的等差数列贡献 (k-1)*(k-2)/2 个子数组
            ans += (length - 1) * (length - 2) // 2
        else:
            i += 1

    return ans


if __name__ == "__main__":
    assert number_of_arithmetic_slices([1, 2, 3, 4]) == 3
    assert number_of_arithmetic_slices([1]) == 0
    assert number_of_arithmetic_slices([1, 2, 3, 8, 9, 10]) == 2
    assert number_of_arithmetic_slices([1, 2, 3]) == 1

    assert number_of_arithmetic_slices_v2([1, 2, 3, 4]) == 3
    assert number_of_arithmetic_slices_v2([1, 2, 3, 8, 9, 10]) == 2

    print("All tests passed.")
