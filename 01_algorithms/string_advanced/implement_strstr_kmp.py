"""
题目：实现 strStr（KMP 算法）
难度：Easy（KMP：Hard） | 高频出现：字节/腾讯/阿里
标签：KMP、字符串匹配
LeetCode：#28


题目描述
---------
实现 strStr() 函数：给你两个字符串 haystack 和 needle，在 haystack 字符串中找出
needle 字符串的第一个匹配项的下标（下标从 0 开始）。如果 needle 不在 haystack 中则返回 -1。
本文件使用 KMP 算法（O(m+n) 时间）实现。

示例
------
输入: haystack = "sadbutsad", needle = "sad"
输出: 0

输入: haystack = "leetcode", needle = "leeto"
输出: -1

约束
------
- 1 <= haystack.length, needle.length <= 10^4
- haystack 和 needle 仅由小写英文字符组成

TL;DR（30秒速览）
- KMP：利用「部分匹配表（next数组）」避免重复匹配，O(m+n)
- next[i]：pattern[0..i] 中最长公共前后缀的长度
- 匹配失败时，模式串指针不从头开始，跳到 next[j-1]

详细解析
---------
next 数组构建（前缀函数）：
  k=0, next[0]=0
  对每个 i：若 pattern[k]==pattern[i]，next[i]=k+1, k++
  否则回退：k = next[k-1]

KMP 匹配：
  text 指针 i 不回退
  pattern 指针 j 失配时跳到 next[j-1]
"""


def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    # 构建 next 数组（部分匹配表）
    n, m = len(text), len(pattern)
    next_arr = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = next_arr[k-1]
        if pattern[k] == pattern[i]:
            k += 1
        next_arr[i] = k

    # KMP 匹配
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = next_arr[j-1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1  # 返回第一次出现的下标
    return -1


if __name__ == "__main__":
    assert kmp_search("sadbutsad", "sad") == 0
    assert kmp_search("leetcode", "leeto") == -1
    assert kmp_search("hello", "ll") == 2
    assert kmp_search("aabaabaaf", "aabaaf") == 3
    assert kmp_search("", "") == 0
    print("All tests passed.")
