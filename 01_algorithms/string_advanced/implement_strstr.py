"""
LeetCode #28 - 找出字符串中第一个匹配项的下标（实现 strStr）
难度: Easy | 频率: 字节/腾讯/阿里（考KMP）

=== 题目描述 ===
给你两个字符串 haystack 和 needle，请你在 haystack 字符串中找出 needle 字符串的第一个匹配项的下标（下标从 0 开始）。
如果 needle 不是 haystack 的一部分，则返回 -1。

示例 1:
  输入: haystack = "sadbutsad", needle = "sad"
  输出: 0

示例 2:
  输入: haystack = "leetcode", needle = "leeto"
  输出: -1

=== TL;DR ===
核心思路:
  方法1（暴力）: 枚举 haystack 的每个起点，逐字符比较 — O(m*n) 时间
  方法2（KMP）: 预处理 needle 的 failure function（部分匹配表），匹配失败时跳过已匹配前缀
    — O(m+n) 时间，O(n) 空间（面试重点考察）
  方法3（Python内置）: haystack.find(needle) 或 haystack.index(needle)

时间复杂度: O(m+n)（KMP），m 为 haystack 长度，n 为 needle 长度
空间复杂度: O(n)（KMP），存储 failure function

=== 详细解析 ===
KMP 算法核心:
1. 构建 failure function（next 数组）: next[i] 表示 needle[0..i] 中最长的真前缀等于真后缀的长度
   - 用双指针: j=0（较短），i=1（较长），若 needle[i]==needle[j] 则 j++，否则回退 j=next[j-1]
2. 匹配时: i 遍历 haystack，j 遍历 needle
   - 若字符相等则 i++，j++
   - 若 j==len(needle) 则找到，返回 i-j
   - 若不等且 j>0，则 j = next[j-1]（不回退 i！）
   - 若不等且 j==0，则 i++

failure function 构建示例（needle = "aabaaab"）:
  i:    0 1 2 3 4 5 6
  c:    a a b a a a b
  next: 0 1 0 1 2 2 3
"""


# ===== 方法1: 暴力匹配 =====
def str_str_brute(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    m, n = len(haystack), len(needle)
    for i in range(m - n + 1):
        if haystack[i:i + n] == needle:
            return i
    return -1


# ===== 方法2: KMP 算法（面试重点）=====
def str_str_kmp(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    m, n = len(haystack), len(needle)

    # 1. 构建 failure function（next 数组）
    def build_next(pattern: str) -> list:
        nxt = [0] * len(pattern)
        j = 0  # 前缀指针
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = nxt[j - 1]  # 回退
            if pattern[i] == pattern[j]:
                j += 1
            nxt[i] = j
        return nxt

    nxt = build_next(needle)

    # 2. 用 next 数组进行匹配
    j = 0  # needle 的指针
    for i in range(m):
        while j > 0 and haystack[i] != needle[j]:
            j = nxt[j - 1]  # 回退，不回退 i
        if haystack[i] == needle[j]:
            j += 1
        if j == n:
            return i - n + 1  # 找到匹配，返回起始位置

    return -1


# ===== 方法3: Python 内置 =====
def str_str_builtin(haystack: str, needle: str) -> int:
    return haystack.find(needle)


# ===== 辅助: 验证 failure function =====
def get_failure_function(pattern: str) -> list:
    """调试用: 返回 KMP failure function"""
    nxt = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j
    return nxt


# ===== 测试 =====
if __name__ == "__main__":
    # 验证 failure function
    assert get_failure_function("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert get_failure_function("aaaa") == [0, 1, 2, 3]
    assert get_failure_function("abcabc") == [0, 0, 0, 1, 2, 3]
    assert get_failure_function("abcabcd") == [0, 0, 0, 1, 2, 3, 0]

    funcs = [str_str_brute, str_str_kmp, str_str_builtin]
    for func in funcs:
        assert func("sadbutsad", "sad") == 0,   func.__name__
        assert func("leetcode", "leeto") == -1, func.__name__
        assert func("hello", "ll") == 2,        func.__name__
        assert func("aaaaa", "bba") == -1,       func.__name__
        assert func("", "") == 0,                func.__name__
        assert func("a", "") == 0,               func.__name__
        assert func("a", "a") == 0,              func.__name__
        assert func("aabaaab", "aaab") == 3,     func.__name__
        assert func("mississippi", "issip") == 4, func.__name__
        assert func("abcabcabc", "abcabc") == 0, func.__name__

    print("All tests passed!")
