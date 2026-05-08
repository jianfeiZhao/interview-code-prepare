"""
题目：找到字符串中所有字母异位词
难度：Medium | 高频出现：字节/阿里/腾讯
标签：滑动窗口、哈希表、字符串
LeetCode：#438


题目描述
---------
给定两个字符串 s 和 p，找到 s 中所有 p 的异位词的子串，返回这些子串的起始索引。
答案以任意顺序返回。异位词是指由相同字母重排列形成的字符串（包含相同的字母，数量也相同）。

示例
------
输入: s = "cbaebabacd", p = "abc"
输出: [0, 6]  （s[0..2]="cba" 和 s[6..8]="bac" 都是 "abc" 的异位词）

输入: s = "abab", p = "ab"
输出: [0, 1, 2]

约束
------
- 1 <= s.length, p.length <= 3 * 10^4
- s 和 p 仅包含小写字母

TL;DR（30秒速览）
- 固定长度滑动窗口（len(p)），维护字符频率差，统计"need==0的字符数"
- 时间 O(n)，空间 O(1)（字符集大小 26）
- 关键陷阱：窗口滑动时既要加新字符又要减去旧字符，need 计数变化要精确

详细解析
---------
此题与 #567（字符串的排列）几乎相同，区别是返回所有起始位置而非布尔值。

固定窗口 + need 计数法：
  need = 需要满足频率要求的字符种数（初始化为 len(set(p))）
  count = Counter(p)（目标频率）
  维护窗口 [left, right]，窗口大小固定为 len(p)

  进入窗口（right 扩展）：
    count[c] -= 1；若 count[c] == 0，need -= 1

  离开窗口（left 收缩，窗口大小超过 len(p)）：
    count[c] += 1；若 count[c] == 1（从 0 变正），need += 1

  need == 0 时记录 left 为异位词起始位置。
"""

from typing import List
from collections import Counter


def find_anagrams(s: str, p: str) -> List[int]:
    if len(s) < len(p):
        return []

    count = Counter(p)
    need = len(count)   # 需要满足条件的字符种数
    left = 0
    result = []

    for right, c in enumerate(s):
        # 新字符进入窗口
        count[c] -= 1
        if count[c] == 0:
            need -= 1

        # 窗口大小超过 len(p)，左端字符离开
        window_size = right - left + 1
        if window_size > len(p):
            out_char = s[left]
            count[out_char] += 1
            if count[out_char] == 1:
                need += 1
            left += 1

        # 窗口大小等于 len(p) 且所有字符满足
        if need == 0:
            result.append(left)

    return result


# 方法二：直接比较 Counter（更简洁但略慢 O(26) 比较）
def find_anagrams_v2(s: str, p: str) -> List[int]:
    n, m = len(s), len(p)
    if n < m:
        return []

    target = Counter(p)
    window = Counter(s[:m])
    result = [0] if window == target else []

    for i in range(m, n):
        window[s[i]] += 1
        old = s[i - m]
        window[old] -= 1
        if window[old] == 0:
            del window[old]
        if window == target:
            result.append(i - m + 1)

    return result


if __name__ == "__main__":
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]
    assert find_anagrams("abab", "ab") == [0, 1, 2]
    assert find_anagrams("aa", "bb") == []
    assert find_anagrams("a", "a") == [0]

    assert find_anagrams_v2("cbaebabacd", "abc") == [0, 6]
    assert find_anagrams_v2("abab", "ab") == [0, 1, 2]

    print("All tests passed.")
