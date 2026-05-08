"""
题目：最长公共子序列（LCS）
难度：Medium | 高频出现：字节/腾讯/阿里
标签：动态规划、字符串
LeetCode：#1143

题目描述
---------
给定两个字符串 text1 和 text2，返回它们最长公共子序列的长度。
子序列是从原字符串中按顺序删除若干字符（不改变相对顺序）得到的字符串，不要求连续。
若不存在公共子序列则返回 0。

示例
------
输入: text1 = "abcde", text2 = "ace"
输出: 3  # "ace" 是最长公共子序列

输入: text1 = "abc", text2 = "def"
输出: 0

约束
------
- 1 <= len(text1), len(text2) <= 1000
- 字符串仅包含小写英文字母

TL;DR（30秒速览）
- 思路：二维 DP，dp[i][j] 表示 text1[:i] 和 text2[:j] 的 LCS 长度
- 时间：O(m×n)  空间：O(m×n)，可优化至 O(min(m,n))
- 转移：字符相等则 dp[i][j]=dp[i-1][j-1]+1，否则 max(dp[i-1][j], dp[i][j-1])

详细解析
---------
dp[i][j] = LCS(text1[0..i-1], text2[0..j-1]) 的长度
  - text1[i-1] == text2[j-1]：dp[i][j] = dp[i-1][j-1] + 1
  - 不等：dp[i][j] = max(dp[i-1][j], dp[i][j-1])

关联题：
  - 编辑距离 (LeetCode #72)：相等 dp[i][j]=dp[i-1][j-1]，不等取三个方向最小值+1
  - 最长公共子串（连续）：相等则+1，不等则0（同时记录最大值）
"""

def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]


def lcs_space_optimized(text1: str, text2: str) -> int:
    """滚动数组优化至 O(n) 空间"""
    m, n = len(text1), len(text2)
    if m < n:
        text1, text2 = text2, text1
        m, n = n, m
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]


if __name__ == "__main__":
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    assert lcs_space_optimized("abcde", "ace") == 3
    print("All tests passed.")
