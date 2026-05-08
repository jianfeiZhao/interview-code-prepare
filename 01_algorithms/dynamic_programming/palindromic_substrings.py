"""
回文子串 + 最长回文子串
LeetCode #647 (Medium) + #5 (Medium)
高频考点: 字节跳动 / 腾讯

============================================================

题目描述
---------
给你一个字符串 s，统计并返回这个字符串中回文子串的数目。
具有不同起始位置或结束位置的子串，即使是由相同的字符组成，也会被视作不同的子串。

扩展题 #5（最长回文子串）：返回 s 中最长的回文子串。

示例
------
#647 输入: s = "abc"   输出: 3  （"a", "b", "c"）
#647 输入: s = "aaa"   输出: 6  （"a"×3, "aa"×2, "aaa"×1）
#5   输入: s = "babad"  输出: "bab" 或 "aba"

约束
------
- 1 <= s.length <= 1000
- s 由小写英文字母组成

TL;DR
============================================================
#647 统计回文子串个数:
  方法A - 中心扩展: 枚举每个中心（奇/偶长度），向两侧扩展统计
  方法B - DP: dp[i][j] = s[i..j] 是否为回文
              dp[i][j] = (s[i]==s[j]) and (j-i<=2 or dp[i+1][j-1])

#5 最长回文子串:
  中心扩展: O(n^2) 时间 O(1) 空间（面试首选）
  DP: O(n^2) 时间 O(n^2) 空间
  Manacher 算法: O(n) 时间 O(n) 空间（了解即可）

核心：中心扩展比 DP 代码更简洁，面试推荐。
============================================================
"""


# ─────────────────────────────────────────────
# #647 统计回文子串个数 - 中心扩展
# ─────────────────────────────────────────────
def count_substrings_expand(s: str) -> int:
    """
    以每个位置为中心，分别扩展奇数长度和偶数长度的回文串。
    时间: O(n^2)，空间: O(1)
    """
    n = len(s)
    count = 0

    def expand(left: int, right: int) -> int:
        cnt = 0
        while left >= 0 and right < n and s[left] == s[right]:
            cnt += 1
            left -= 1
            right += 1
        return cnt

    for i in range(n):
        count += expand(i, i)      # 奇数长度，中心为 s[i]
        count += expand(i, i + 1)  # 偶数长度，中心为 s[i]s[i+1]

    return count


# ─────────────────────────────────────────────
# #647 统计回文子串个数 - DP
# ─────────────────────────────────────────────
def count_substrings_dp(s: str) -> int:
    """
    dp[i][j] = s[i..j] 是否为回文。
    按子串长度由小到大填表（必须先计算短的再计算长的）。
    时间: O(n^2)，空间: O(n^2)
    """
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0

    # 枚举子串长度 length = 1, 2, ..., n
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length <= 2:
                    dp[i][j] = True        # 单字符或双字符相等
                else:
                    dp[i][j] = dp[i + 1][j - 1]  # 依赖内部子串
            if dp[i][j]:
                count += 1
    return count


# ─────────────────────────────────────────────
# #5 最长回文子串 - 中心扩展
# ─────────────────────────────────────────────
def longest_palindrome_expand(s: str) -> str:
    """
    对每个中心扩展，记录最长回文的起始位置和长度。
    时间: O(n^2)，空间: O(1)（面试推荐）
    """
    start, max_len = 0, 1

    def expand(left: int, right: int):
        nonlocal start, max_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                max_len = right - left + 1
                start = left
            left -= 1
            right += 1

    for i in range(len(s)):
        expand(i, i)       # 奇数
        expand(i, i + 1)   # 偶数

    return s[start: start + max_len]


# ─────────────────────────────────────────────
# #5 最长回文子串 - DP
# ─────────────────────────────────────────────
def longest_palindrome_dp(s: str) -> str:
    """
    时间: O(n^2)，空间: O(n^2)
    """
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length <= 2:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i + 1][j - 1]
            if dp[i][j] and length > max_len:
                max_len = length
                start = i
    return s[start: start + max_len]


# ─────────────────────────────────────────────
# Manacher 算法 O(n) - 了解即可
# ─────────────────────────────────────────────
def longest_palindrome_manacher(s: str) -> str:
    """
    Manacher 算法：线性时间求最长回文子串。
    思路：将字符串插入分隔符（如 #），统一处理奇偶情况。
         利用已知回文的对称性，避免重复扩展。
    p[i] = 以 t[i] 为中心的最长回文半径（含中心）
    """
    # 插入特殊字符
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    center = right = 0  # 目前最右回文的中心和右边界

    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        # 尝试继续扩展
        a, b = i - p[i] - 1, i + p[i] + 1
        while a >= 0 and b < n and t[a] == t[b]:
            p[i] += 1
            a -= 1
            b += 1
        # 更新最右回文边界
        if i + p[i] > right:
            center, right = i, i + p[i]

    # 找最大 p[i]，还原到原始下标
    max_len_idx = p.index(max(p))
    max_len = p[max_len_idx]
    orig_start = (max_len_idx - max_len) // 2
    return s[orig_start: orig_start + max_len]


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_palindromic():
    # #647 统计个数
    assert count_substrings_expand("abc") == 3    # a, b, c
    assert count_substrings_expand("aaa") == 6    # a,a,a,aa,aa,aaa
    assert count_substrings_expand("abba") == 6   # a,b,b,a,bb,abba
    assert count_substrings_expand("racecar") == 10

    assert count_substrings_dp("abc") == 3
    assert count_substrings_dp("aaa") == 6
    assert count_substrings_dp("abba") == 6
    print("#647 count_substrings: all passed")

    # #5 最长回文子串
    r1 = longest_palindrome_expand("babad")
    assert r1 in ("bab", "aba")

    r2 = longest_palindrome_expand("cbbd")
    assert r2 == "bb"

    r3 = longest_palindrome_expand("a")
    assert r3 == "a"

    r4 = longest_palindrome_expand("ac")
    assert r4 in ("a", "c")

    # DP 与扩展结果一致（长度）
    for t in ["babad", "cbbd", "racecar", "abcba", "aacabdkacaa"]:
        l1 = len(longest_palindrome_expand(t))
        l2 = len(longest_palindrome_dp(t))
        l3 = len(longest_palindrome_manacher(t))
        assert l1 == l2 == l3, f"mismatch on {t!r}: expand={l1}, dp={l2}, manacher={l3}"
    print("#5 longest_palindrome: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_palindromic()
