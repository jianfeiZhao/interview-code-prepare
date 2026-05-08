"""
题目: 丑数 II（三指针 / 堆）
LeetCode: #264 (Medium)
高频公司: 字节跳动、阿里巴巴

题目描述:
给你一个整数 n，请你找出并返回第 n 个丑数。
丑数就是质因子只包含 2、3 和 5 的正整数。

示例 1: n = 10 -> 12
        前10个丑数: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12]
示例 2: n = 1 -> 1   (1 也是丑数)

================================================================================
TL;DR:

方法1 - 三指针（DP，推荐）:
  - dp[i] 表示第 i+1 个丑数
  - 维护三个指针 p2, p3, p5，分别指向下一个待乘以 2/3/5 的丑数位置
  - 每次取 dp[p2]*2, dp[p3]*3, dp[p5]*5 的最小值，对应指针 +1
  - 天然去重（三个候选值相等时同步推进）
  时间: O(n)，空间: O(n)

方法2 - 小顶堆:
  - 初始堆中只有 1
  - 每次弹出最小值，将其乘以 2/3/5 后入堆
  - 用 set 去重（避免重复入堆）
  时间: O(n log n)，空间: O(n)
================================================================================
"""

import heapq


# ===================== 方法1: 三指针 DP（最优）=====================

def nthUglyNumber_dp(n: int) -> int:
    """
    三指针动态规划：
    每个丑数都是由某个更小的丑数乘以 2、3 或 5 得到的。
    用三个指针追踪「下一个应该被乘的丑数位置」。
    """
    dp = [0] * n
    dp[0] = 1  # 第 1 个丑数是 1

    p2 = p3 = p5 = 0  # 三个指针，分别等待乘以 2/3/5

    for i in range(1, n):
        # 三个候选下一个丑数
        next2 = dp[p2] * 2
        next3 = dp[p3] * 3
        next5 = dp[p5] * 5

        # 取最小值
        dp[i] = min(next2, next3, next5)

        # 推进对应指针（可能同时推进多个，处理重复）
        if dp[i] == next2:
            p2 += 1
        if dp[i] == next3:
            p3 += 1
        if dp[i] == next5:
            p5 += 1

    return dp[n - 1]


# ===================== 方法2: 小顶堆 =====================

def nthUglyNumber_heap(n: int) -> int:
    """
    小顶堆模拟：每次弹出最小的丑数，并将其 *2、*3、*5 加入堆。
    用 visited 集合去重。
    """
    heap = [1]
    visited = {1}
    val = 1

    for _ in range(n):
        val = heapq.heappop(heap)
        for factor in [2, 3, 5]:
            nxt = val * factor
            if nxt not in visited:
                visited.add(nxt)
                heapq.heappush(heap, nxt)

    return val


# ===================== 延伸：超级丑数（任意质因子集合）=====================

def nthSuperUglyNumber(n: int, primes: list) -> int:
    """
    #313 超级丑数：质因子不限于 2/3/5，可以是任意 primes。
    将三指针推广为 k 指针（k = len(primes)）。
    """
    dp = [0] * n
    dp[0] = 1
    # 每个质因子对应一个指针
    pointers = [0] * len(primes)

    for i in range(1, n):
        # 计算每个质因子对应的候选值
        candidates = [dp[pointers[j]] * primes[j] for j in range(len(primes))]
        dp[i] = min(candidates)

        # 推进所有等于最小值的指针
        for j in range(len(primes)):
            if candidates[j] == dp[i]:
                pointers[j] += 1

    return dp[n - 1]


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 前 15 个丑数
    ugly_seq = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24]

    for i, expected in enumerate(ugly_seq, 1):
        r1 = nthUglyNumber_dp(i)
        r2 = nthUglyNumber_heap(i)
        assert r1 == expected, f"dp: n={i}, got={r1}, expected={expected}"
        assert r2 == expected, f"heap: n={i}, got={r2}, expected={expected}"

    # 边界
    assert nthUglyNumber_dp(1) == 1
    assert nthUglyNumber_dp(1690) == 2123366400  # LeetCode 约束上界

    # 超级丑数测试（primes=[2,7,13,19]）
    # 第7个超级丑数: [1,2,4,7,8,13,14,...] -> 14
    assert nthSuperUglyNumber(7, [2, 7, 13, 19]) == 14

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"第10个丑数: {nthUglyNumber_dp(10)}")  # 12
    print(f"第1个丑数:  {nthUglyNumber_dp(1)}")   # 1
    print(f"前15个丑数: {[nthUglyNumber_dp(i) for i in range(1, 16)]}")

    print(f"\n三指针过程（前8个丑数）:")
    # 手动演示三指针逻辑
    dp_demo = [0] * 8
    dp_demo[0] = 1
    p2 = p3 = p5 = 0
    for i in range(1, 8):
        next2, next3, next5 = dp_demo[p2]*2, dp_demo[p3]*3, dp_demo[p5]*5
        dp_demo[i] = min(next2, next3, next5)
        if dp_demo[i] == next2: p2 += 1
        if dp_demo[i] == next3: p3 += 1
        if dp_demo[i] == next5: p5 += 1
        print(f"  dp[{i}]={dp_demo[i]}, p2={p2}, p3={p3}, p5={p5}")
