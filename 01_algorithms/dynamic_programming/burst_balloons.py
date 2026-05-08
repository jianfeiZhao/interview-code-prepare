"""
题目：戳气球
难度：Hard | 高频出现：字节/阿里
标签：区间DP
LeetCode：#312

题目描述
---------
给定一个整数数组 nums，代表 n 个气球，每个气球上标有一个数字。
戳破第 i 个气球可以获得 nums[i-1] * nums[i] * nums[i+1] 枚硬币（边界外视为 1）。
戳破后该气球消失，左右邻居随之相邻。
求按某种顺序戳破所有气球能获得的最多硬币数。

示例
------
输入: nums = [3, 1, 5, 8]
输出: 167  # 顺序 1,5,3,8 → 3*1*5 + 3*5*8 + 1*3*8 + 1*8*1 = 15+120+24+8 = 167

约束
------
- 1 <= n <= 300
- 0 <= nums[i] <= 100

TL;DR（30秒速览）
- 区间DP：dp[l][r] 表示戳破 (l,r) 开区间内所有气球的最大硬币数
- 枚举最后一个戳破的气球 k，nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r]
- 时间 O(n³)，空间 O(n²)

详细解析
---------
关键转化：考虑「最后」戳哪个，而非最先戳哪个
在 (l,r) 开区间内，最后戳气球 k 时：
  - 左边 [l,k) 已全部戳完，右边 (k,r] 已全部戳完
  - 戳 k 时相邻为 nums[l] 和 nums[r]
  - dp[l][r] = max(nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r])

两端添加虚拟气球1（哨兵），处理边界
"""

from typing import List


def max_coins(nums: List[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # 枚举区间长度
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r],
                               nums[l] * nums[k] * nums[r] + dp[l][k] + dp[k][r])
    return dp[0][n - 1]


if __name__ == "__main__":
    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10
    assert max_coins([1]) == 1
    print("All tests passed.")
