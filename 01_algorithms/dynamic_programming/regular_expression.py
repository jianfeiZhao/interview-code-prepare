"""
题目：正则表达式匹配
难度：Hard | 高频出现：字节/阿里/腾讯
标签：动态规划、字符串
LeetCode：#10

题目描述
---------
给定字符串 s 和模式串 p，实现支持 '.' 和 '*' 的正则表达式匹配。
'.' 匹配任意单个字符，'*' 匹配零个或多个前面的元素。
匹配应覆盖整个字符串 s（而非部分），返回是否匹配成功。

示例
------
输入: s = "aa", p = "a*"
输出: True  # "a*" 可匹配零个或多个 'a'

输入: s = "aab", p = "c*a*b"
输出: True  # "c*" 匹配零个 'c'，"a*" 匹配两个 'a'，"b" 匹配 'b'

约束
------
- 1 <= len(s) <= 20，s 仅含小写英文字母
- 1 <= len(p) <= 30，p 仅含小写英文字母、'.' 和 '*'，且 '*' 不出现在首位

TL;DR（30秒速览）
- dp[i][j] = s[0..i-1] 能否被 p[0..j-1] 匹配
- 关键：'*' 匹配0个或多个前一字符
- 时间 O(m*n)，空间 O(m*n)

详细解析
---------
状态转移：
  若 p[j-1] == s[i-1] 或 p[j-1] == '.'：dp[i][j] = dp[i-1][j-1]
  若 p[j-1] == '*'：
    - 匹配0次：dp[i][j] = dp[i][j-2]
    - 匹配>=1次（前提 p[j-2] 能匹配 s[i-1]）：dp[i][j] = dp[i-1][j]
"""


def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # 初始化：空字符串和 "a*b*c*..." 类型的模式
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] in (s[i-1], '.'):
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-2]  # 匹配0次
                if p[j-2] in (s[i-1], '.'):
                    dp[i][j] = dp[i][j] or dp[i-1][j]  # 匹配>=1次
    return dp[m][n]


if __name__ == "__main__":
    assert is_match("aa", "a") is False
    assert is_match("aa", "a*") is True
    assert is_match("ab", ".*") is True
    assert is_match("aab", "c*a*b") is True
    assert is_match("mississippi", "mis*is*p*.") is False
    assert is_match("", ".*") is True
    assert is_match("", "") is True
    print("All tests passed.")
