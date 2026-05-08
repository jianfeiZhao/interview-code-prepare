"""
题目：爬楼梯（Fibonacci 变体）
难度：Easy | 高频出现：全系大厂
标签：动态规划、递推
LeetCode：#70

题目描述
---------
给定一个正整数 n，代表一个有 n 阶的楼梯。
每次可以爬 1 阶或 2 阶，问共有多少种不同方法爬到楼顶？

示例
------
输入: n = 3
输出: 3  # 1+1+1、1+2、2+1 三种方法

输入: n = 5
输出: 8

约束
------
- 1 <= n <= 45

TL;DR（30秒速览）
- 思路：dp[i] = dp[i-1] + dp[i-2]，本质是斐波那契数列
- 时间：O(n)  空间：O(1)（滚动变量优化）
- 陷阱：初始值 dp[1]=1, dp[2]=2（不是 dp[0]=1, dp[1]=1）

详细解析
---------
每次可爬 1 或 2 步，到达第 n 阶的方法数：
  状态：dp[i] = 到达第 i 阶的方法数
  转移：dp[i] = dp[i-1] + dp[i-2]（最后一步爬1阶 or 2阶）
  初始：dp[1]=1, dp[2]=2

空间优化：只需保留前两个状态，O(1) 空间

进阶：
  - 每次可爬 1/2/.../k 步 → dp[i] = sum(dp[i-j] for j in 1..k)
  - 有坏台阶（LeetCode #198 打家劫舍变体）
"""

def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


def climb_stairs_dp(n: int) -> int:
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]


if __name__ == "__main__":
    assert climb_stairs(1) == 1
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    assert climb_stairs(10) == 89
    print("All tests passed.")
