"""
题目: 至多包含 K 个不同字符的最长子串
LeetCode: #340 (Medium, 会员题) / 变体
高频公司: 字节跳动

题目描述:
给你一个字符串 s 和一个整数 k，请找出至多含 k 个不同字符的最长子串，返回该子串的长度。

示例 1: s = "eceba", k = 2 -> 3   (子串 "ece")
示例 2: s = "aa", k = 1 -> 2
示例 3: s = "aabbcc", k = 2 -> 4  (子串 "aabb" 或 "bbcc")

延伸题目:
- #3  最长不含重复字符的子串（k 个不同 = 全不同）
- #904 水果成篮（k=2 时的整数版）
- 恰好含 k 个不同字符的子串数 = atMost(k) - atMost(k-1)（#992）

================================================================================
TL;DR（核心思路）:
- 滑动窗口 + 哈希表：维护窗口内不同字符种数不超过 k
- 当 len(window_count) > k 时，左指针右移（并更新计数）
- 答案 = max(right - left + 1)
- 模板可复用：改变 k 值即可解决不同类型的子串问题

时间复杂度: O(n)
空间复杂度: O(k)
================================================================================
"""

from collections import defaultdict


def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    """
    至多 k 个不同字符的最长子串（滑动窗口标准模板）。
    """
    if k == 0 or not s:
        return 0

    char_count = defaultdict(int)  # 窗口内字符频率
    left = 0
    max_len = 0

    for right in range(len(s)):
        char_count[s[right]] += 1

        # 不同字符种数超过 k，收缩左边界
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len


def countSubstringsExactlyK(s: str, k: int) -> int:
    """
    恰好含 k 个不同字符的子串数量（#992 变体）。
    利用公式：恰好k = atMost(k) - atMost(k-1)
    """
    def at_most(k: int) -> int:
        """至多 k 个不同字符的子串数量。"""
        char_count = defaultdict(int)
        left = 0
        count = 0
        for right in range(len(s)):
            char_count[s[right]] += 1
            while len(char_count) > k:
                char_count[s[left]] -= 1
                if char_count[s[left]] == 0:
                    del char_count[s[left]]
                left += 1
            # [left, right] 内所有以 right 结尾的子串均满足条件
            count += right - left + 1
        return count

    return at_most(k) - at_most(k - 1)


def lengthOfLongestSubstringNoRepeat(s: str) -> int:
    """
    特殊情况：k = 所有不同字符（#3 最长不含重复字符子串）。
    等价于 k = len(s)，或直接用 set 判断。
    """
    return lengthOfLongestSubstringKDistinct(s, len(set(s)) if s else 0)


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 至多 k 个不同字符最长子串
    assert lengthOfLongestSubstringKDistinct("eceba", 2) == 3     # "ece"
    assert lengthOfLongestSubstringKDistinct("aa", 1) == 2        # "aa"
    assert lengthOfLongestSubstringKDistinct("aabbcc", 2) == 4    # "aabb"/"bbcc"
    assert lengthOfLongestSubstringKDistinct("aabbcc", 3) == 6    # 整个字符串
    assert lengthOfLongestSubstringKDistinct("aabbcc", 1) == 2    # "aa"/"bb"/"cc"
    assert lengthOfLongestSubstringKDistinct("", 2) == 0
    assert lengthOfLongestSubstringKDistinct("abc", 0) == 0
    assert lengthOfLongestSubstringKDistinct("a", 1) == 1
    assert lengthOfLongestSubstringKDistinct("abaccc", 2) == 4    # "accc"

    # 恰好 k 个不同字符的子串数
    # "aab": 恰好1个=[a,a,b] 3个, 恰好2个=[aa,aab,ab] 3个
    assert countSubstringsExactlyK("aab", 1) == 3   # a, a, b
    assert countSubstringsExactlyK("aab", 2) == 3   # aa, aab, ab
    assert countSubstringsExactlyK("aba", 2) == 3   # ab, ba, aba

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"'eceba', k=2: {lengthOfLongestSubstringKDistinct('eceba', 2)}")    # 3
    print(f"'aa', k=1: {lengthOfLongestSubstringKDistinct('aa', 1)}")          # 2
    print(f"'aabbcc', k=2: {lengthOfLongestSubstringKDistinct('aabbcc', 2)}")  # 4

    print(f"\n恰好 k 个不同字符的子串数:")
    s = "aabbc"
    for k in range(1, 4):
        print(f"  '{s}', k={k}: {countSubstringsExactlyK(s, k)}")

    print(f"\nk 值对最长子串长度的影响 ('aabbccdd'):")
    s2 = "aabbccdd"
    for k in range(1, 5):
        print(f"  k={k}: {lengthOfLongestSubstringKDistinct(s2, k)}")
