"""
题目: 最小覆盖子串
LeetCode: #76 (Hard)
高频公司: 字节跳动、腾讯、阿里巴巴（超高频）

题目描述:
给你一个字符串 s 、一个字符串 t 。返回 s 中涵盖 t 所有字符的最小子串。
如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 ""。

注意：
- 对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。
- 如果 s 中存在这样的子串，我们保证它是唯一的答案。

示例 1: s = "ADOBECODEBANC", t = "ABC" -> "BANC"
示例 2: s = "a", t = "a" -> "a"
示例 3: s = "a", t = "aa" -> ""

================================================================================
TL;DR（核心思路）:
- 双指针滑动窗口：right 扩张直到覆盖 t，left 收缩找最小
- need[c] 记录还需要的字符数量（初始 = Counter(t)，窗口内出现则减少）
- formed 统计已满足条件的字符种数
- 当 formed == len(need_original) 时，窗口有效，记录最小，收缩 left

时间复杂度: O(|s| + |t|)
空间复杂度: O(|t|)
================================================================================"""

from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)  # 需要满足的字符种数
    formed = 0
    left = 0
    min_len = float('inf')
    result = ""

    for right, c in enumerate(s):
        need[c] -= 1
        if need[c] == 0:
            formed += 1
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right+1]
            need[s[left]] += 1
            if need[s[left]] > 0:
                formed -= 1
            left += 1

    return result


if __name__ == "__main__":
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("aa", "aa") == "aa"
    assert min_window("bba", "ab") == "ba"        # 从右侧找到更短的
    assert min_window("abc", "b") == "b"          # t是单字符
    assert min_window("", "a") == ""              # 空串
    assert min_window("abc", "") == ""            # t为空
    assert min_window("ab", "b") == "b"
    print("所有测试通过!")
    print(f"\n示例结果:")
    print(f"'ADOBECODEBANC', t='ABC': '{min_window('ADOBECODEBANC', 'ABC')}'")  # BANC
    print(f"'a', t='a': '{min_window('a', 'a')}'")                              # a
    print(f"'a', t='aa': '{min_window('a', 'aa')}'")                            # 空
