"""
题目：字符串的排列 + 找到字符串中所有字母异位词
难度：Medium | 高频出现：字节/阿里/腾讯
标签：滑动窗口、哈希表
LeetCode：#567 字符串的排列，#438 找到字符串中所有字母异位词


题目描述
---------
#567 字符串的排列：给你两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的排列。
如果是，返回 True；否则返回 False。换句话说就是 s1 的排列之一是 s2 的子串。

#438 找到字符串中所有字母异位词：给定两个字符串 s 和 p，返回 s 中所有 p 的异位词的子串起始索引。

示例
------
#567 输入: s1="ab", s2="eidbaooo"  输出: True（s2 中 "ba" 是 s1 的排列）
#438 输入: s="cbaebabacd", p="abc"  输出: [0,6]

约束
------
- 1 <= s1.length, s2.length <= 10^4
- s1 和 s2 仅包含小写字母

TL;DR（30秒速览）
- 固定大小窗口（len(s1)），用字符频率数组比较
- 维护 need（需要的字符计数）和 match（满足条件的字符种类数）
- 时间 O(n)，空间 O(1)（字母表大小26）

详细解析
---------
优化：维护 diff（窗口与目标的差值字典），当 diff 中所有值为0时即找到答案
或维护 need 字典 + match 计数（满足条件的字符种类数）
"""

from typing import List
from collections import Counter


def check_inclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        # 加入右端字符
        window[s2[i]] += 1
        # 移除左端字符
        left = s2[i - len(s1)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]
        if window == need:
            return True
    return False


def find_anagrams(s: str, p: str) -> List[int]:
    result = []
    if len(p) > len(s):
        return result
    need = Counter(p)
    window = Counter(s[:len(p)])
    if window == need:
        result.append(0)
    for i in range(len(p), len(s)):
        window[s[i]] += 1
        left = s[i - len(p)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]
        if window == need:
            result.append(i - len(p) + 1)
    return result


if __name__ == "__main__":
    assert check_inclusion("ab", "eidbaooo") is True
    assert check_inclusion("ab", "eidboaoo") is False

    assert find_anagrams("cbaebabacd", "abc") == [0, 6]
    assert find_anagrams("abab", "ab") == [0, 1, 2]
    assert find_anagrams("baa", "aa") == [1]
    print("All tests passed.")
