"""
解码方法
LeetCode #91 (Medium)
高频考点: 字节跳动 / 阿里巴巴

题目描述
---------
给定一个只含数字的字符串 s，将其映射到字母编码（'A'->1, 'B'->2, ..., 'Z'->26）。
返回 s 所有可能的解码方式的数目。
注意：'0' 不能单独解码，双字符解码范围为 10~26。

示例
------
输入: s = "12"
输出: 2  # "AB"（1,2）或 "L"（12）

输入: s = "226"
输出: 3  # "BZ"(2,26)、"VF"(22,6)、"BBF"(2,2,6)

约束
------
- 1 <= len(s) <= 100
- s 仅包含数字，可能含有前导零

============================================================
TL;DR
============================================================
状态: dp[i] = 字符串 s[:i] 的解码方式数
初始: dp[0] = 1（空串，1种解法）
转移:
  单字符解码（s[i-1]）：
    若 s[i-1] != '0'：dp[i] += dp[i-1]
  双字符解码（s[i-2:i]）：
    若 s[i-2] == '1' or (s[i-2] == '2' and s[i-1] <= '6')：
        dp[i] += dp[i-2]
答案: dp[n]

关键边界：
  - '0' 不能单独解码
  - 双字符范围 10~26
  - "00", "30" 等无效 → dp[i] = 0
============================================================
"""


# ─────────────────────────────────────────────
# 方法1：DP（数组）
# ─────────────────────────────────────────────
def num_decodings(s: str) -> int:
    """
    时间: O(n)，空间: O(n)
    """
    n = len(s)
    if n == 0 or s[0] == '0':
        return 0

    dp = [0] * (n + 1)
    dp[0] = 1   # 空串
    dp[1] = 1   # 第一个字符（已确认不是 '0'）

    for i in range(2, n + 1):
        # 单字符解码
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        # 双字符解码
        two = int(s[i - 2: i])
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]

    return dp[n]


# ─────────────────────────────────────────────
# 方法2：空间优化（滚动变量）
# ─────────────────────────────────────────────
def num_decodings_optimized(s: str) -> int:
    """
    只需保留 dp[i-1] 和 dp[i-2]，空间 O(1)。
    时间: O(n)，空间: O(1)
    """
    n = len(s)
    if n == 0 or s[0] == '0':
        return 0

    prev2 = 1   # dp[i-2]，初始 dp[0]=1
    prev1 = 1   # dp[i-1]，初始 dp[1]=1

    for i in range(2, n + 1):
        curr = 0
        if s[i - 1] != '0':
            curr += prev1
        two = int(s[i - 2: i])
        if 10 <= two <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr

    return prev1


# ─────────────────────────────────────────────
# 扩展：解码方法 II（#639）
# 含 '*' 通配符（代表 1-9 中任意数字）
# ─────────────────────────────────────────────
def num_decodings_with_wildcard(s: str) -> int:
    """
    LeetCode #639 Hard.
    '*' 可代表 '1'~'9' 任意一个数字。
    分情况讨论单字符和双字符的组合数。
    结果对 1e9+7 取模。
    """
    MOD = 10 ** 9 + 7
    n = len(s)

    def single(c: str) -> int:
        """单字符 c 的解码数量"""
        if c == '*':
            return 9  # 1~9
        return 0 if c == '0' else 1

    def double(c1: str, c2: str) -> int:
        """双字符 c1c2 的解码数量"""
        if c1 == '*' and c2 == '*':
            return 15   # 11-19(9种) + 21-26(6种)
        if c1 == '*':
            # c1 可以是 1(c2=0-9都行) 或 2(c2=0-6才行)
            return 2 if c2 <= '6' else 1
        if c2 == '*':
            # c1='1' → 11-19，9种；c1='2' → 21-26，6种；否则 0
            if c1 == '1':
                return 9
            if c1 == '2':
                return 6
            return 0
        # 两者均为数字
        two = int(c1 + c2)
        return 1 if 10 <= two <= 26 else 0

    prev2, prev1 = 1, single(s[0])
    for i in range(1, n):
        curr = single(s[i]) * prev1 + double(s[i - 1], s[i]) * prev2
        prev2, prev1 = prev1, curr % MOD
    return prev1 % MOD


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_decode_ways():
    cases = [
        ("12", 2),      # "AB"(1,2) or "L"(12)
        ("226", 3),     # "BZ"(2,26) or "VF"(22,6) or "BBF"(2,2,6)
        ("0", 0),       # '0' 无法解码
        ("06", 0),      # '0' 开头无效
        ("10", 1),      # "J"(10)
        ("110", 1),     # "KA"(11,0) or "AAJ"? "AJ"=1,10=1种; "KA"=11,0: "0" 只能配对使用
        ("1", 1),
        ("11106", 2),   # "AAJF"(1,1,10,6) or "KJF"(11,10,6)
        ("2101", 1),    # "U"+"A" = "UA" (21,0,1) → 0无效，只能 2,10,1 = 1种
    ]
    for s, expected in cases:
        r1 = num_decodings(s)
        r2 = num_decodings_optimized(s)
        assert r1 == expected, f"dp({s!r})={r1}, expected {expected}"
        assert r2 == expected, f"opt({s!r})={r2}, expected {expected}"
    print("num_decodings: all passed")

    # 通配符版
    assert num_decodings_with_wildcard("*") == 9     # 1~9
    assert num_decodings_with_wildcard("1*") == 18   # 10-19各1种，共10；加上1*(1+*)
    # 官方用例
    assert num_decodings_with_wildcard("*") == 9
    assert num_decodings_with_wildcard("1*") == 18
    assert num_decodings_with_wildcard("2*") == 15
    print("num_decodings_with_wildcard: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_decode_ways()
