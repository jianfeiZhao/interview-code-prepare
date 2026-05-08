"""
LeetCode #44 - 通配符匹配 (Wildcard Matching)
难度: Hard | 频率: 字节/阿里

=== 题目描述 ===
给你一个输入字符串 s 和一个字符规律 p，请你实现一个支持 '?' 和 '*' 的通配符匹配。
  '?' 可以匹配任何单个字符。
  '*' 可以匹配任意字符串（包括空字符串）。
匹配应覆盖整个输入字符串（而不是部分字符串）。

示例 1: s = "aa",   p = "a"    -> false
示例 2: s = "aa",   p = "*"    -> true（'*' 匹配整个字符串）
示例 3: s = "cb",   p = "?a"   -> false
示例 4: s = "adceb", p = "*a*b" -> true
示例 5: s = "acdcb", p = "a*c?b" -> false

=== TL;DR ===
核心思路:
  方法1（DP）: dp[i][j] = s[0..i-1] 与 p[0..j-1] 是否匹配
    - p[j-1]=='?': dp[i][j] = dp[i-1][j-1]
    - p[j-1]=='*': dp[i][j] = dp[i-1][j] or dp[i][j-1]（匹配一个字符 or 匹配空串）
    - 否则: dp[i][j] = dp[i-1][j-1] and s[i-1]==p[j-1]
  方法2（双指针贪心）: 记录 '*' 的位置和当时匹配到的 s 的位置，失败时回溯

时间复杂度: O(m*n)，m 为 s 长度，n 为 p 长度
空间复杂度: O(m*n)（DP）/ O(1)（贪心）

=== 详细解析 ===
关键技巧:
1. DP 初始化: dp[0][0]=True；dp[0][j]: p 的前 j 个字符全是'*'时才为 True
2. '*' 的 DP 转移: dp[i][j] = dp[i][j-1]（'*'匹配空） or dp[i-1][j]（'*'匹配一个字符）
3. 贪心双指针: 维护 star_j（上一个'*'在 p 中的位置）和 match（当时 i 的位置），
   匹配失败时 i 回到 match+1，j 回到 star_j+1，match++
4. 注意区分 #44 通配符匹配（'*' 匹配任意序列）和 #10 正则匹配（'*' 匹配零或多个前驱字符）
"""


# ===== 方法1: 动态规划（面试推荐）=====
def is_match_dp(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[i][j]: s 的前 i 个字符与 p 的前 j 个字符是否匹配
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True  # 两个空串匹配

    # 初始化: p 的前 j 个字符全是 '*' 时，dp[0][j] = True
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
        else:
            break  # 一旦遇到非 '*'，后面全是 False

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' 匹配空串: dp[i][j-1]
                # '*' 匹配一个字符: dp[i-1][j]（等价于 '*' 还没"用完"）
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


# ===== 方法2: 贪心双指针（O(1) 空间）=====
def is_match_greedy(s: str, p: str) -> bool:
    i, j = 0, 0        # s 和 p 的指针
    star_j = -1        # 上一个 '*' 在 p 中的位置
    match_i = 0        # 上一个 '*' 匹配时，s 的位置

    while i < len(s):
        if j < len(p) and (p[j] == '?' or p[j] == s[i]):
            i += 1
            j += 1
        elif j < len(p) and p[j] == '*':
            star_j = j  # 记录 '*' 位置
            match_i = i  # 记录当前 i（'*' 先匹配空串）
            j += 1
        elif star_j != -1:
            # 回溯: '*' 多匹配一个字符
            match_i += 1
            i = match_i
            j = star_j + 1
        else:
            return False

    # p 剩余部分必须全是 '*'
    while j < len(p) and p[j] == '*':
        j += 1

    return j == len(p)


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ("aa", "a", False),
        ("aa", "*", True),
        ("cb", "?a", False),
        ("adceb", "*a*b", True),
        ("acdcb", "a*c?b", False),
        ("", "", True),
        ("", "*", True),
        ("", "?", False),
        ("abc", "abc", True),
        ("abc", "a*c", True),
        ("abc", "a*b", False),
        ("abc", "***", True),
        ("ab", "?*", True),
        ("b", "?*?", False),
        ("ho", "**ho", True),
    ]

    for func in [is_match_dp, is_match_greedy]:
        for s, p, expected in cases:
            result = func(s, p)
            assert result == expected, \
                f"{func.__name__}({s!r}, {p!r}) = {result}, expected {expected}"

    print("All tests passed!")
