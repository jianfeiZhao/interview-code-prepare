"""
LeetCode #231 - 2的幂 (Power of Two)
难度: Easy | 频率: 全系

=== 题目描述 ===
给你一个整数 n，请你判断该整数是否是 2 的幂次方。如果是，返回 true；否则，返回 false。
如果存在一个整数 x 使得 n == 2^x，则认为 n 是 2 的幂次方。

示例 1: 输入: n = 1   输出: true  (2^0 = 1)
示例 2: 输入: n = 16  输出: true  (2^4 = 16)
示例 3: 输入: n = 3   输出: false

进阶: 不使用循环/递归，尝试用 O(1) 解决此问题。

=== TL;DR ===
核心思路:
  方法1（位运算）: 2的幂的二进制表示只有一个1位。n & (n-1) == 0 当且仅当 n 是2的幂
  方法2（位计数）: bin(n).count('1') == 1
  方法3（数学）: n > 0 and 2^30 % n == 0（任何2的幂都是最大2的幂的因子）
  方法4（循环除2）: 不断除以2，若余数不为0则不是2的幂

时间复杂度: O(1)（位运算方法）
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. n & (n-1): 将 n 最低位的1清零。若 n 是2的幂，清零后变为0
   例: n=8=1000, n-1=0111, n&(n-1)=0000
   例: n=6=0110, n-1=0101, n&(n-1)=0100 (非0，故不是2的幂)
2. 注意: n <= 0 时必须返回 False（0和负数不是2的幂）
3. lowbit 技巧: n & (-n) 取出最低位1，若 == n 则 n 是2的幂
4. 同类题: #342 4的幂（n>0 and n&(n-1)==0 and n%3==1），#191 位1的个数
"""


# ===== 方法1: 位运算 n & (n-1)（O(1) 面试推荐）=====
def is_power_of_two_bit(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


# ===== 方法2: lowbit（n & -n == n）=====
def is_power_of_two_lowbit(n: int) -> bool:
    return n > 0 and (n & -n) == n


# ===== 方法3: bin 计数 =====
def is_power_of_two_bin(n: int) -> bool:
    return n > 0 and bin(n).count('1') == 1


# ===== 方法4: 取模最大幂 =====
def is_power_of_two_mod(n: int) -> bool:
    return n > 0 and (1 << 30) % n == 0


# ===== 方法5: 循环 =====
def is_power_of_two_loop(n: int) -> bool:
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


# ===== 进阶: #342 4的幂 =====
def is_power_of_four(n: int) -> bool:
    """4的幂: 首先是2的幂，且唯一的1位在奇数位（0-indexed）
    0x55555555 = 0101...0101，掩码奇数位"""
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [
        is_power_of_two_bit,
        is_power_of_two_lowbit,
        is_power_of_two_bin,
        is_power_of_two_mod,
        is_power_of_two_loop,
    ]
    cases = [
        (1, True),
        (2, True),
        (3, False),
        (4, True),
        (16, True),
        (0, False),
        (-1, False),
        (-16, False),
        (1024, True),
        (1023, False),
        (2**30, True),
        (2**30 - 1, False),
    ]
    for func in funcs:
        for n, expected in cases:
            assert func(n) == expected, f"{func.__name__}({n}) = {func(n)}, expected {expected}"

    # 4的幂测试
    assert is_power_of_four(1) == True
    assert is_power_of_four(4) == True
    assert is_power_of_four(16) == True
    assert is_power_of_four(2) == False
    assert is_power_of_four(8) == False
    assert is_power_of_four(64) == True

    print("All tests passed!")
