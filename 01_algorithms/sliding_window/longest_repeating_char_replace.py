"""
题目: 替换后的最长重复字符
LeetCode: #424 (Medium)
高频公司: 字节跳动、腾讯

题目描述:
给你一个字符串 s 和一个整数 k 。你可以选择字符串中的任一字符，并将其更改为任何其他大写英文字符。
该操作最多可执行 k 次。
在执行上述操作后，返回包含相同字母的最长子字符串的长度。

示例 1: s = "ABAB", k = 2 -> 4   (将两个 A 或两个 B 替换，得到 "AAAA" 或 "BBBB")
示例 2: s = "AABABBA", k = 1 -> 4 (将 index=5 的 B 替换，得到 "AABAB" -> "AAABA" 长4... 实际是 "AABA")

================================================================================
TL;DR（核心思路）:
- 滑动窗口：维护最长子串，使得其中出现最多的字符频次 + k >= 窗口长度
- 关键不等式：(窗口长度 - 窗口内最高频字符数) <= k  => 需要替换的字符数 <= k
- max_count 跟踪历史最大频次（无需缩减，因为答案只增不减）
- 当不等式不满足时，left 右移（等价于窗口平移，不缩小）

核心公式：
  合法窗口条件: (right - left + 1) - max_count <= k
  即: 窗口大小 - 最高频字符数 <= 可替换次数

时间复杂度: O(n)
空间复杂度: O(1)（最多 26 个字母）
================================================================================
"""


def characterReplacement(s: str, k: int) -> int:
    """
    滑动窗口 + 最高频字符数维护。

    关键洞察：
    若窗口 [left, right] 内最多的字符出现了 max_count 次，
    则需要替换的字符数 = (right - left + 1) - max_count。
    若这个数量 <= k，窗口合法。

    max_count 的维护：
    我们只需要在 max_count 增大时扩展窗口，
    否则直接平移窗口（left 和 right 同时 +1），保证窗口大小不缩小。
    """
    count = [0] * 26  # 每个字母的频率
    left = 0
    max_count = 0   # 历史最大频次（用于保证窗口只增不减）

    for right in range(len(s)):
        count[ord(s[right]) - ord('A')] += 1
        # 更新当前窗口内最高频字符数
        max_count = max(max_count, count[ord(s[right]) - ord('A')])

        # 判断当前窗口是否合法
        window_size = right - left + 1
        if window_size - max_count > k:
            # 不合法：平移窗口（左边减一个，不扩大）
            count[ord(s[left]) - ord('A')] -= 1
            left += 1

    # 窗口大小 = right - left + 1，由于只增不减，最终窗口大小即为答案
    return len(s) - left


def characterReplacement_explicit(s: str, k: int) -> int:
    """
    更显式的写法：维护 max_len，便于理解为何不需要缩减 max_count。
    """
    count = [0] * 26
    left = 0
    max_count = 0
    max_len = 0

    for right in range(len(s)):
        idx = ord(s[right]) - ord('A')
        count[idx] += 1
        max_count = max(max_count, count[idx])

        # 若当前窗口需要替换的字符数 > k，收缩左边界
        while (right - left + 1) - max_count > k:
            count[ord(s[left]) - ord('A')] -= 1
            left += 1
            # 重新计算 max_count（注意：这里重新遍历26个字母，O(26)=O(1)）
            max_count = max(count)

        max_len = max(max_len, right - left + 1)

    return max_len


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    assert characterReplacement("ABAB", 2) == 4
    assert characterReplacement("AABABBA", 1) == 4
    assert characterReplacement("AAAA", 2) == 4    # 全相同，无需替换
    assert characterReplacement("ABCD", 0) == 1    # k=0，只能选相同字符
    assert characterReplacement("ABCD", 4) == 4    # k=4，可全替换
    assert characterReplacement("A", 0) == 1
    assert characterReplacement("AABA", 0) == 2    # "AA"

    # 两种实现结果一致
    test_cases = [
        ("ABAB", 2),
        ("AABABBA", 1),
        ("AAAA", 2),
        ("ABCDE", 2),
        ("ABABABABAB", 3),
    ]
    for s, k in test_cases:
        r1 = characterReplacement(s, k)
        r2 = characterReplacement_explicit(s, k)
        assert r1 == r2, f"两种实现不一致: s={s}, k={k}, r1={r1}, r2={r2}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"'ABAB', k=2:    {characterReplacement('ABAB', 2)}")    # 4
    print(f"'AABABBA', k=1: {characterReplacement('AABABBA', 1)}")  # 4

    print(f"\n解题过程演示 ('AABABBA', k=1):")
    s, k = "AABABBA", 1
    count = [0] * 26
    left = 0
    max_count = 0
    for right in range(len(s)):
        count[ord(s[right]) - ord('A')] += 1
        max_count = max(max_count, count[ord(s[right]) - ord('A')])
        window = s[left:right+1]
        need_replace = (right - left + 1) - max_count
        valid = need_replace <= k
        print(f"  right={right} '{s[right]}', window='{window}', "
              f"max_count={max_count}, need_replace={need_replace}, valid={valid}")
        if not valid:
            count[ord(s[left]) - ord('A')] -= 1
            left += 1
