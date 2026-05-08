"""
题目：无重复字符的最长子串
难度：Medium | 高频出现：字节/美团/阿里
标签：滑动窗口、哈希表
LeetCode：#3

题目描述
---------
给定字符串 s，找出其中不含重复字符的最长子串的长度。
子串是字符串中连续的字符序列，不同于子序列（子序列可以不连续）。

示例
------
输入: s = "abcabcbb"
输出: 3  # 最长无重复子串为 "abc"

输入: s = "pwwkew"
输出: 3  # 最长无重复子串为 "wke"

约束
------
- 0 <= len(s) <= 5 * 10^4
- s 由英文字母、数字、符号和空格组成

TL;DR（30秒速览）
- 思路：滑动窗口，用哈希表记录字符最新下标，遇到重复则收缩左边界
- 时间：O(n)  空间：O(min(n, 字符集大小))
- 陷阱：left = max(left, seen[c]+1) 而非 left += 1，避免左边界回退

详细解析
---------
双指针（left, right）维护一个无重复窗口：
  - right 向右扩展
  - 若 s[right] 在窗口中已存在 → left 跳到该字符上次出现位置+1
  - 每步更新最大窗口长度

关键：seen[c] >= left 才说明字符在窗口内（用 max 防止 left 左移）
"""

def length_of_longest_substring(s: str) -> int:
    seen = {}  # char -> last index
    left = 0
    max_len = 0
    for right, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = right
        max_len = max(max_len, right - left + 1)
    return max_len


if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    print("All tests passed.")
