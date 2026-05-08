"""
题目：分割回文串
难度：Medium | 高频出现：字节/阿里/腾讯
标签：回溯、动态规划
LeetCode：#131


题目描述
---------
给你一个字符串 s，请你将 s 分割成一些子串，使每个子串都是回文串。
返回 s 所有可能的分割方案。

示例
------
输入: s = "aab"
输出: [["a","a","b"],["aa","b"]]

输入: s = "a"
输出: [["a"]]

约束
------
- 1 <= s.length <= 16
- s 仅由小写英文字母组成

TL;DR（30秒速览）
- 回溯：枚举每个前缀，若是回文则递归处理剩余部分
- 预处理：dp[i][j] 标记所有回文子串，O(n²)
- 时间 O(n*2^n)，空间 O(n²)

详细解析
---------
优化：先用 DP 预计算所有 [i,j] 是否为回文，避免回溯时重复判断
dp[i][j] = s[i]==s[j] and (j-i<2 or dp[i+1][j-1])
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    n = len(s)
    # 预处理回文判断
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_palindrome[i+1][j-1]):
                is_palindrome[i][j] = True

    result = []

    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if is_palindrome[start][end]:
                path.append(s[start:end+1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result


if __name__ == "__main__":
    result = partition("aab")
    assert sorted(result) == sorted([["a","a","b"],["aa","b"]])

    result2 = partition("a")
    assert result2 == [["a"]]

    result3 = partition("aba")
    assert sorted(result3) == sorted([["a","b","a"],["aba"]])
    print("All tests passed.")
