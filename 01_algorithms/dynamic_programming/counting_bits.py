"""
题目：比特位计数
难度：Easy | 高频出现：字节/阿里
标签：动态规划、位运算
LeetCode：#338


题目描述
---------
给你一个整数 n，对于 i ∈ [0, n] 中的每个 i，计算其二进制表示中 1 的个数，
返回一个长度为 n+1 的数组 ans，其中 ans[i] 为 i 的二进制表示中 1 的个数。

示例
------
输入: n = 2
输出: [0,1,1]

输入: n = 5
输出: [0,1,1,2,1,2]

约束
------
- 0 <= n <= 10^5
- 进阶：要求线性时间 O(n) 且只遍历一次

TL;DR（30秒速览）
- dp[i] = dp[i >> 1] + (i & 1)：右移一位的 1 个数 + 最低位是否为 1
- 时间 O(n)，空间 O(n)（输出数组本身）
- 关键陷阱：dp[i >> 1] 已经被计算过，利用子问题避免重复计算

详细解析
---------
核心递推：
  i >> 1 相当于去掉最低位，而 dp[i>>1] 已知。
  最低位 (i & 1) 贡献 0 或 1 个额外的 1。
  所以 dp[i] = dp[i >> 1] + (i & 1)。

变种递推（利用最低有效位 & 最低设置位）：
  dp[i] = dp[i & (i-1)] + 1
  i & (i-1) 清除最低位的 1，差值始终是 1 个 1。
"""

from typing import List


# 方法一：右移递推（推荐）
def count_bits(n: int) -> List[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


# 方法二：清除最低位递推
def count_bits_v2(n: int) -> List[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i & (i - 1)] + 1
    return dp


# 方法三：暴力（对照验证用）
def count_bits_brute(n: int) -> List[int]:
    return [bin(i).count('1') for i in range(n + 1)]


if __name__ == "__main__":
    assert count_bits(2) == [0, 1, 1]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert count_bits(0) == [0]

    for i in range(20):
        assert count_bits(i) == count_bits_brute(i), f"failed at n={i}"
        assert count_bits_v2(i) == count_bits_brute(i), f"v2 failed at n={i}"

    print("All tests passed.")
