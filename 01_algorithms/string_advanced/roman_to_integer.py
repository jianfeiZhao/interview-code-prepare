"""
LeetCode #13 - 罗马数字转整数 (Roman to Integer)
难度: Easy | 频率: 全系

=== 题目描述 ===
罗马数字包含以下七种字符: I, V, X, L, C, D 和 M。
  字符   数值
  I       1
  V       5
  X       10
  L       50
  C       100
  D       500
  M       1000

通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，
如 4 写作 IV（而非 IIII），6 写作 VI；以下六种情况使用减法:
  IV=4, IX=9, XL=40, XC=90, CD=400, CM=900

给定一个罗马数字，将其转换成整数。输入确保在 1 到 3999 的范围内。

示例:
  "III"  -> 3
  "LVIII" -> 58   (L=50, V=5, III=3)
  "MCMXCIV" -> 1994  (M=1000, CM=900, XC=90, IV=4)

=== TL;DR ===
核心思路: 从右向左扫描，若当前字符对应值 < 右边字符对应值，则减去当前值；否则加上。
  等价思路（从左向右）: 若当前值 < 下一个值，减去当前值；否则加上当前值。
时间复杂度: O(n)，n 为字符串长度（最多13个字符，即 O(1)）
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. 核心规律: 当较小符号出现在较大符号左边时，做减法；否则做加法
2. 从右向左扫: 与前一次记录的值比较，更直观
3. 从左向右扫: 比较 s[i] 和 s[i+1]，若 val[s[i]] < val[s[i+1]] 则减，否则加
4. 不需要特判 IV/IX 等组合，用大小关系就能处理
"""

# ===== 方法1: 从左向右扫描（推荐）=====
def roman_to_int(s: str) -> int:
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}
    result = 0
    n = len(s)
    for i in range(n):
        # 若当前值小于下一个值，减去（如 I 在 V 前面 -> 减法）
        if i < n - 1 and val[s[i]] < val[s[i + 1]]:
            result -= val[s[i]]
        else:
            result += val[s[i]]
    return result


# ===== 方法2: 从右向左扫描 =====
def roman_to_int_rtl(s: str) -> int:
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}
    result = val[s[-1]]
    for i in range(len(s) - 2, -1, -1):
        if val[s[i]] < val[s[i + 1]]:
            result -= val[s[i]]
        else:
            result += val[s[i]]
    return result


# ===== 方法3: 替换特殊组合后求和 =====
def roman_to_int_replace(s: str) -> int:
    # 先替换6种减法组合，再对单字符求和
    replacements = [
        ('CM', 'DCCCC'), ('CD', 'CCCC'),
        ('XC', 'LXXXX'), ('XL', 'XXXX'),
        ('IX', 'VIIII'), ('IV', 'IIII'),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    return sum(val[c] for c in s)


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ("I", 1),
        ("III", 3),
        ("IV", 4),
        ("IX", 9),
        ("LVIII", 58),
        ("MCMXCIV", 1994),
        ("XIV", 14),
        ("XLII", 42),
        ("XC", 90),
        ("CD", 400),
        ("CM", 900),
        ("MMMCMXCIX", 3999),
    ]

    for func in [roman_to_int, roman_to_int_rtl, roman_to_int_replace]:
        for roman, expected in cases:
            assert func(roman) == expected, f"{func.__name__}({roman!r}) = {func(roman)}, expected {expected}"

    print("All tests passed!")
