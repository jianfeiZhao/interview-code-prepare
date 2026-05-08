"""
题目：完全平方数
难度：Medium | 高频出现：字节/阿里
标签：动态规划、BFS、数学
LeetCode：#279

题目描述
---------
给定一个正整数 n，返回和为 n 的完全平方数（1, 4, 9, 16, ...）的最少数量。
完全平方数是某个整数的平方，每个完全平方数可以重复使用任意次。

示例
------
输入: n = 12
输出: 3  # 12 = 4 + 4 + 4

输入: n = 13
输出: 2  # 13 = 4 + 9

约束
------
- 1 <= n <= 10^4

TL;DR（30秒速览）
- 完全背包DP：dp[i] = min(dp[i - j*j] + 1)，O(n√n)
- BFS：每层为同一步数能到达的数，第一次到n即答案
- 数学：Legendre四平方和定理，O(√n)

详细解析
---------
完全背包DP：
  dp[0]=0，dp[i]为最少几个完全平方数凑成i
  对每个 i，枚举所有 j 使得 j*j <= i：dp[i] = min(dp[i-j*j]+1)

四平方和定理（数学最优）：
  任意正整数最多用4个完全平方数表示
  只需要4个的条件：n = 4^a(8b+7)
"""

from typing import List
import math


def num_squares_dp(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    squares = [i * i for i in range(1, int(n**0.5) + 1)]
    for i in range(1, n + 1):
        for sq in squares:
            if sq > i:
                break
            dp[i] = min(dp[i], dp[i - sq] + 1)
    return dp[n]


def num_squares_math(n: int) -> int:
    def is_perfect_square(x):
        s = int(x**0.5)
        return s * s == x

    if is_perfect_square(n):
        return 1
    # 判断是否为2
    for i in range(1, int(n**0.5) + 1):
        if is_perfect_square(n - i * i):
            return 2
    # 判断是否为4：n = 4^a * (8b + 7)
    while n % 4 == 0:
        n //= 4
    if n % 8 == 7:
        return 4
    return 3


if __name__ == "__main__":
    assert num_squares_dp(12) == 3   # 4+4+4
    assert num_squares_dp(13) == 2   # 4+9
    assert num_squares_dp(1) == 1
    assert num_squares_dp(4) == 1

    assert num_squares_math(12) == 3
    assert num_squares_math(13) == 2
    assert num_squares_math(1) == 1
    print("All tests passed.")
