"""
题目: x 的平方根（二分整数解）
LeetCode: #69 (Easy)
高频公司: 全系（字节、阿里、腾讯、百度等）

题目描述:
给你一个非负整数 x，计算并返回 x 的算术平方根。
由于返回类型是整数，结果只保留整数部分，小数部分将被舍去。
注意：不允许使用任何内置指数函数和算符，例如 pow(x, 0.5) 或者 x ** 0.5 。

示例 1: x = 4 -> 2
示例 2: x = 8 -> 2   (sqrt(8) ≈ 2.828，舍去小数后为 2)

================================================================================
TL;DR (核心思路):
  - 二分整数解：在 [1, x] 上找最大的 mid 使得 mid*mid <= x
  - 变体：找最后一个满足条件的数（右边界二分）
  - 注意 x=0 和 x=1 的边界情况
  - 牛顿迭代法（扩展）：x_{n+1} = (x_n + S/x_n) / 2，收敛更快

时间复杂度: O(log x)
空间复杂度: O(1)
================================================================================
"""


def mySqrt_binary(x: int) -> int:
    """
    二分搜索：找最大的 mid 使得 mid * mid <= x。
    这是"找右边界"的二分模板。
    """
    if x < 2:
        return x  # x=0 -> 0, x=1 -> 1

    left, right = 1, x // 2  # sqrt(x) <= x//2（x>=4时）

    while left <= right:
        mid = left + (right - left) // 2

        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1   # mid 可能是答案，但还有更大的满足条件的值
        else:
            right = mid - 1  # mid*mid > x，mid 太大

    # 循环结束时 right < left，right 是最后一个 mid*mid <= x 的值
    return right


def mySqrt_clean(x: int) -> int:
    """
    更简洁的写法，直接在 [0, x] 上使用左闭右开二分。
    找第一个 mid 使得 mid*mid > x，然后返回 mid-1。
    """
    if x < 2:
        return x

    left, right = 0, x + 1  # 左闭右开 [0, x+1)

    while left < right:
        mid = left + (right - left) // 2
        if mid * mid > x:
            right = mid      # mid 太大，缩小右边界
        else:
            left = mid + 1   # mid*mid <= x，可能的答案，但尝试更大

    return left - 1  # left 是第一个 mid*mid > x 的值，left-1 是答案


def mySqrt_newton(x: int) -> int:
    """
    牛顿迭代法（扩展思路）：
    求 f(r) = r^2 - x = 0，迭代公式: r = (r + x/r) / 2。
    从 x 开始迭代，快速收敛到 sqrt(x)。
    """
    if x < 2:
        return x

    r = x
    while r * r > x:
        r = (r + x // r) // 2  # 整数除法保证收敛

    return r


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    import math

    test_cases = [0, 1, 2, 3, 4, 8, 9, 15, 16, 100, 101, 2147395599]

    for x in test_cases:
        expected = int(math.isqrt(x))  # Python 内置整数平方根
        r1 = mySqrt_binary(x)
        r2 = mySqrt_clean(x)
        r3 = mySqrt_newton(x)

        assert r1 == expected, f"binary: x={x}, got={r1}, expected={expected}"
        assert r2 == expected, f"clean: x={x}, got={r2}, expected={expected}"
        assert r3 == expected, f"newton: x={x}, got={r3}, expected={expected}"

    print("所有测试通过!")

    # 打印示例
    print(f"\nmySqrt(4)  = {mySqrt_binary(4)}")   # 2
    print(f"mySqrt(8)  = {mySqrt_binary(8)}")   # 2
    print(f"mySqrt(9)  = {mySqrt_binary(9)}")   # 3
    print(f"mySqrt(16) = {mySqrt_binary(16)}")  # 4
    print(f"mySqrt(0)  = {mySqrt_binary(0)}")   # 0
    print(f"mySqrt(1)  = {mySqrt_binary(1)}")   # 1

    # 比较三种方法
    print(f"\n三种方法对比（x=8）:")
    print(f"  binary:  {mySqrt_binary(8)}")
    print(f"  clean:   {mySqrt_clean(8)}")
    print(f"  newton:  {mySqrt_newton(8)}")
