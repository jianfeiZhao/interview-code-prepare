"""
LeetCode #204 - 计数质数 (Count Primes)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
给定整数 n，返回所有小于非负整数 n 的质数的数量。

示例 1: 输入: n = 10  输出: 4  (2, 3, 5, 7)
示例 2: 输入: n = 0   输出: 0
示例 3: 输入: n = 1   输出: 0

=== TL;DR ===
核心思路:
  方法1（埃拉托色尼筛法，Sieve of Eratosthenes）: 标记所有合数，剩余未标记的即质数
    — O(n log log n) 时间，O(n) 空间（面试标准答案）
  方法2（线性筛，欧拉筛）: 每个合数只被其最小质因子筛一次 — O(n) 时间，O(n) 空间

时间复杂度: O(n log log n)（埃氏筛）/ O(n)（线性筛）
空间复杂度: O(n)

=== 详细解析 ===
埃氏筛关键技巧:
1. 初始化 is_prime = [True] * n，0 和 1 标记为非质数
2. 从 2 开始，若 is_prime[i] 为真，则将 i 的所有倍数（从 i*i 开始）标记为合数
3. 从 i*i 开始: 因为 i*k（k<i）已被更小的质数筛掉了
4. 外层循环只需到 sqrt(n): i*i >= n 时可停止
5. 最后 sum(is_prime) 即质数个数

线性筛关键思路:
1. 维护质数列表 primes，对每个数 i 用 primes 中的质数筛
2. 当 i % primes[j] == 0 时停止（确保每个合数只被最小质因子筛一次）
"""

import math


# ===== 方法1: 埃拉托色尼筛法（面试推荐）=====
def count_primes_sieve(n: int) -> int:
    if n < 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    # 外层只需到 sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            # 从 i*i 开始标记，步长为 i
            for j in range(i * i, n, i):
                is_prime[j] = False

    return sum(is_prime)


# ===== 方法2: 埃氏筛（更 Pythonic，用切片赋值）=====
def count_primes_sieve_v2(n: int) -> int:
    if n < 2:
        return 0
    is_prime = bytearray([1]) * n  # bytearray 比 list 更节省内存
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = bytearray(len(is_prime[i * i::i]))  # 批量置0
    return sum(is_prime)


# ===== 方法3: 线性筛（欧拉筛，严格 O(n)）=====
def count_primes_linear(n: int) -> int:
    if n < 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, n):
        if is_prime[i]:
            primes.append(i)
        for p in primes:
            if i * p >= n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                break  # p 是 i 的最小质因子，确保线性

    return len(primes)


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 1),    # 只有 2
        (10, 4),   # 2, 3, 5, 7
        (20, 8),   # 2,3,5,7,11,13,17,19
        (100, 25),
        (1000, 168),
    ]
    for func in [count_primes_sieve, count_primes_sieve_v2, count_primes_linear]:
        for n, expected in cases:
            result = func(n)
            assert result == expected, f"{func.__name__}({n}) = {result}, expected {expected}"

    print("All tests passed!")
