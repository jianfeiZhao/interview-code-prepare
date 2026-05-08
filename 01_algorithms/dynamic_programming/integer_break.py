"""
整数拆分
LeetCode #343 (Medium)
高频考点: 字节跳动 / 阿里巴巴

题目描述
---------
给定一个正整数 n，将其拆分为至少两个正整数的和，使这些正整数的乘积最大化。
返回可以获得的最大乘积。拆分出的正整数不要求互不相同。

示例
------
输入: n = 10
输出: 36  # 10 = 3 + 3 + 4，乘积 3 * 3 * 4 = 36

输入: n = 2
输出: 1  # 2 = 1 + 1，乘积 1 * 1 = 1

约束
------
- 2 <= n <= 58

============================================================
TL;DR
============================================================
将正整数 n 拆成至少 2 个正整数之和，使乘积最大。

方法A - DP:
  状态: dp[i] = 整数 i 拆分后的最大乘积
  转移: dp[i] = max(j * (i-j), j * dp[i-j])  for j in [1, i)
        - j*(i-j): 只拆成两段
        - j*dp[i-j]: j 不继续拆，但 (i-j) 继续拆
  初始: dp[1]=1, dp[2]=1
  答案: dp[n]

方法B - 数学贪心（面试可直接说结论）:
  尽量拆成 3，若余 1 则用 2+2 替换 3+1（4>3）。
  n%3==0 → 3^(n/3)
  n%3==1 → 4 * 3^((n-4)/3)
  n%3==2 → 2 * 3^((n-2)/3)

原理：e ≈ 2.718，最优分拆单位是 e，整数最接近的是 3。
============================================================
"""

import math


# ─────────────────────────────────────────────
# 方法1：DP
# ─────────────────────────────────────────────
def integer_break_dp(n: int) -> int:
    """
    dp[i] 表示正整数 i 拆分后的最大乘积。
    对每个 i，枚举第一段长度 j（1 <= j < i）：
      - 不继续拆 (i-j)：乘积为 j * (i-j)
      - 继续拆 (i-j)：乘积为 j * dp[i-j]
    取最大值。

    时间: O(n^2)，空间: O(n)
    """
    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        for j in range(1, i):
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])

    return dp[n]


# ─────────────────────────────────────────────
# 方法2：数学贪心（O(1) 时间）
# ─────────────────────────────────────────────
def integer_break_math(n: int) -> int:
    """
    数学结论：
      - n <= 3：特殊处理（无法多拆）
      - n%3==0：全拆成 3
      - n%3==1：剩 4 → 拆成 2*2
      - n%3==2：剩 2 → 保留一个 2

    直觉：每段长度为 2 时单位乘积 2/2=1，为 3 时 3/3=1，
          但 3 段比两段 2 更大 (3 > 2+2/2)。避免使用 1（乘以 1 无益）。

    时间: O(1)，空间: O(1)
    """
    if n <= 2:
        return 1
    if n == 3:
        return 2
    if n == 4:
        return 4  # 2*2

    q, r = divmod(n, 3)
    if r == 0:
        return 3 ** q
    elif r == 1:
        # 最后一段 4 拆成 2+2，而不是 3+1
        return 4 * (3 ** (q - 1))
    else:  # r == 2
        return 2 * (3 ** q)


# ─────────────────────────────────────────────
# 扩展：完全平方数（#279 Medium）
# ─────────────────────────────────────────────
def num_squares(n: int) -> int:
    """
    LeetCode #279: 最少用几个完全平方数（1,4,9,...）之和凑出 n。
    等价于完全背包求最少物品数。

    dp[i] = 凑出 i 的最少完全平方数个数
    转移: dp[i] = min(dp[i - j*j] + 1)  for j*j <= i
    时间: O(n * sqrt(n))，空间: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    squares = [j * j for j in range(1, int(math.isqrt(n)) + 1)]
    for i in range(1, n + 1):
        for sq in squares:
            if sq > i:
                break
            dp[i] = min(dp[i], dp[i - sq] + 1)
    return dp[n]


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_integer_break():
    cases = [
        (2, 1),    # 1*1
        (3, 2),    # 1*2
        (4, 4),    # 2*2
        (5, 6),    # 2*3
        (6, 9),    # 3*3
        (7, 12),   # 3*4 (3*(2+2))
        (8, 18),   # 2*3*3
        (9, 27),   # 3*3*3
        (10, 36),  # 3*3*4
    ]
    for n, expected in cases:
        r1 = integer_break_dp(n)
        r2 = integer_break_math(n)
        assert r1 == expected, f"dp({n})={r1}, expected {expected}"
        assert r2 == expected, f"math({n})={r2}, expected {expected}"
    print("integer_break: all passed")

    # 大规模验证两种方法一致
    for n in range(2, 50):
        assert integer_break_dp(n) == integer_break_math(n), f"mismatch at n={n}"
    print("integer_break consistency check (n=2..49): all passed")

    # 完全平方数
    assert num_squares(12) == 3   # 4+4+4
    assert num_squares(13) == 2   # 4+9
    assert num_squares(1) == 1
    assert num_squares(4) == 1    # 4
    assert num_squares(7) == 4    # 4+1+1+1
    print("num_squares: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_integer_break()
