"""
LeetCode #7 - 整数反转 (Reverse Integer)
难度: Medium | 频率: 全系

=== 题目描述 ===
给你一个 32 位的有符号整数 x，返回将 x 中的数字部分反转后的结果。
如果反转后整数超过 32 位的有符号整数的范围 [−2^31, 2^31 − 1]，就返回 0。
假设环境不允许存储 64 位整数（有符号或无符号）。

示例 1: 输入: x = 123    输出: 321
示例 2: 输入: x = -123   输出: -321
示例 3: 输入: x = 120    输出: 21（末尾0消失）
示例 4: 输入: x = 0      输出: 0

=== TL;DR ===
核心思路: 逐位取出 x 末尾数字，拼到结果上，每次拼前先检查是否会溢出。
  方法1（字符串）: 转字符串翻转后检查溢出（Python 最简洁，但面试通常要求不用字符串）
  方法2（数学取模）: 用 x % 10 取末位，x // 10 去掉末位，每步检查溢出 — O(log x) 时间

时间复杂度: O(log|x|)，最多处理 10 位数字
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. Python 取模对负数的行为与 C++ 不同: Python 中 -123 % 10 = 7（而非 -3）
   需要用 int(x % 10) 并对负数特殊处理，或先取 abs 再还原符号
2. 溢出判断（重点）: 设 INT_MAX = 2^31-1 = 2147483647
   - 在追加最后一位前: 若 result > INT_MAX // 10，必然溢出
   - 若 result == INT_MAX // 10，判断最后一位是否 > 7（INT_MAX末位）
3. Python 没有整数溢出，但面试通常要求按 32 位处理，最后 clamp 一下
4. 处理负号: 记录符号位，对 abs(x) 操作，最后还原
"""

INT_MAX = 2 ** 31 - 1    # 2147483647
INT_MIN = -(2 ** 31)     # -2147483648


# ===== 方法1: 字符串翻转（Python 简洁，面试快速写）=====
def reverse_string(x: int) -> int:
    sign = -1 if x < 0 else 1
    s = str(abs(x))[::-1]
    result = sign * int(s)
    if result < INT_MIN or result > INT_MAX:
        return 0
    return result


# ===== 方法2: 数学取模（模拟 32 位逐位处理，面试推荐）=====
def reverse_math(x: int) -> int:
    sign = -1 if x < 0 else 1
    x = abs(x)
    result = 0

    while x != 0:
        digit = x % 10
        x //= 10
        # 提前检查溢出: result * 10 + digit > INT_MAX
        if result > (INT_MAX - digit) // 10:
            return 0
        result = result * 10 + digit

    return sign * result


# ===== 方法3: 模拟 C++ 行为（处理负数取模）=====
def reverse_cpp_style(x: int) -> int:
    """模拟 C++ 中 x % 10 对负数的行为（截断除法），不依赖符号分离"""
    result = 0
    while x != 0:
        # C++ 截断除法的模拟: 取末位（保留符号）
        digit = int(x % 10)
        if x < 0 and digit > 0:
            digit -= 10
        x = int((x - digit) / 10)
        result = result * 10 + digit
    if result < INT_MIN or result > INT_MAX:
        return 0
    return result


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        (123, 321),
        (-123, -321),
        (120, 21),
        (0, 0),
        (1534236469, 0),   # 溢出返回0
        (-2147483648, 0),  # 翻转后溢出
        (1000000003, 0),   # 3000000001 > INT_MAX
        (10, 1),
        (-10, -1),
        (7, 7),
    ]
    for func in [reverse_string, reverse_math, reverse_cpp_style]:
        for x, expected in cases:
            result = func(x)
            assert result == expected, f"{func.__name__}({x}) = {result}, expected {expected}"

    print("All tests passed!")
