"""
题目：Pow(x, n)
难度：Medium | 高频出现：字节/阿里/腾讯
标签：递归、快速幂
LeetCode：#50

题目描述
---------
实现 pow(x, n) 函数，计算 x 的 n 次幂（即 x^n）。n 可以是正整数、负整数或零。
要求时间复杂度优于 O(n) 的朴素连乘，使用快速幂算法在 O(log n) 内完成计算。
n 为负数时结果为 1 / x^|n|。

示例
------
输入: x = 2.00000, n = 10
输出: 1024.00000

输入: x = 2.00000, n = -2
输出: 0.25000（即 1 / 2^2 = 0.25）

约束
------
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- n 为 INT_MIN 时取绝对值需注意溢出（使用 long 或先做特殊处理）
- 结果在 [-10^4, 10^4] 范围内

TL;DR（30秒速览）
- 快速幂：x^n = x^(n/2) * x^(n/2)，递归/迭代，O(log n)
- 注意 n 为负数时取倒数，n 为 INT_MIN 时取绝对值溢出问题

详细解析
---------
递归快速幂：
  n 为偶数：x^n = (x^(n/2))^2
  n 为奇数：x^n = x * x^(n-1)

迭代快速幂（位运算）：
  将 n 写成二进制，对每个1位累乘对应的 x^(2^i)
"""


def my_pow_recursive(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    if n < 0:
        return 1.0 / my_pow_recursive(x, -n)
    if n % 2 == 0:
        half = my_pow_recursive(x, n // 2)
        return half * half
    return x * my_pow_recursive(x, n - 1)


def my_pow_iterative(x: float, n: int) -> float:
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


if __name__ == "__main__":
    assert abs(my_pow_recursive(2.0, 10) - 1024.0) < 1e-9
    assert abs(my_pow_recursive(2.1, 3) - 9.261000000000001) < 1e-6
    assert abs(my_pow_recursive(2.0, -2) - 0.25) < 1e-9
    assert abs(my_pow_iterative(2.0, 10) - 1024.0) < 1e-9
    assert abs(my_pow_iterative(2.0, -2) - 0.25) < 1e-9
    print("All tests passed.")
