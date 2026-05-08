"""
题目：统计元音子字符串的数目
难度：Easy | 高频出现：字节
标签：滑动窗口、哈希表、字符串
LeetCode：#2062

题目描述
---------
给定字符串 word，统计其中"元音子字符串"的数目。
元音子字符串是指：仅由元音字母（a, e, i, o, u）组成，且同时包含全部 5 种元音的子字符串。
字符串中若含有辅音字母则会打断有效子串。

示例
------
输入: word = "aeiouu"
输出: 2  # "aeiou"（下标0-4）和 "aeiouu"（下标0-5）均包含全部5种元音

输入: word = "cuaieuouac"
输出: 7

约束
------
- 1 <= len(word) <= 100
- word 仅由小写英文字母组成

TL;DR（30秒速览）
- 子字符串：仅由元音且包含全部5种元音（a,e,i,o,u）
- 暴力 O(n^2)；滑动窗口用 at_most 模板 O(n)
- 时间 O(n)，空间 O(1)
- 关键陷阱：子串中不能含非元音字母（遇到辅音直接断开/重置）

详细解析
---------
方法一（暴力 O(n^2)）：
  枚举所有子串，判断是否只含元音且包含全部5种。

方法二（滑动窗口 O(n)）：
  等价于：恰好包含5种元音 = at_most(5) - at_most(4)
  但"不含辅音"的限制使得遇到辅音要重置窗口。

  改进：对每段连续元音序列单独处理。
  at_most_k(vowels_only_segment, k)：至多 k 种元音的子数组数。
  答案 = sum(at_most(5) - at_most(4)) for each consecutive vowels segment

方法三（双指针 at_most 直接处理全串）：
  遇到辅音时 left 跳到辅音后一位，清空频率字典。
  其余与 #992 的 at_most 相同。
"""

from collections import defaultdict

VOWELS = set('aeiou')


# 方法一：暴力 O(n^2)
def count_vowel_substrings_brute(word: str) -> int:
    n = len(word)
    count = 0
    for i in range(n):
        freq: dict = defaultdict(int)
        for j in range(i, n):
            if word[j] not in VOWELS:
                break
            freq[word[j]] += 1
            if len(freq) == 5:
                count += 1
    return count


# 方法二：at_most 模板 O(n)
def count_vowel_substrings(word: str) -> int:
    def at_most(limit: int) -> int:
        """仅由元音组成且至多 limit 种元音的子串数"""
        freq: dict = defaultdict(int)
        distinct = 0
        left = 0
        count = 0

        for right, ch in enumerate(word):
            if ch not in VOWELS:
                # 辅音：清空窗口，left 跳到 right+1
                freq.clear()
                distinct = 0
                left = right + 1
                continue

            if freq[ch] == 0:
                distinct += 1
            freq[ch] += 1

            # 收缩左端到 distinct <= limit
            while distinct > limit:
                freq[word[left]] -= 1
                if freq[word[left]] == 0:
                    distinct -= 1
                left += 1

            count += right - left + 1

        return count

    return at_most(5) - at_most(4)


if __name__ == "__main__":
    assert count_vowel_substrings("aeiouu") == 2     # "aeiou", "aeiouu" 不对... 只有 "aeiou"?
    # 实际："aeiou"(0-4) 和 "aeiouu"? 不，"aeiouu"含u出现2次，所有5种元音都有 -> 也算
    # 重新验证：word="aeiouu" -> 子串"aeiou"(5种) "aeiouu"(5种) "eiouu"(5种? e,i,o,u 4种) 不含a -> 不算
    # 所以："aeiou"(0,1,2,3,4) 和 "aeiouu"(0,1,2,3,4,5)
    # LeetCode 答案是 2

    assert count_vowel_substrings("unicornarihan") == 0
    assert count_vowel_substrings("cuaieuouac") == 7

    # 验证两种方法一致
    tests = ["aeiouu", "unicornarihan", "cuaieuouac", "aeiou", "a", "aeiouaeiou"]
    for w in tests:
        assert count_vowel_substrings(w) == count_vowel_substrings_brute(w), \
            f"mismatch for {w}: {count_vowel_substrings(w)} vs {count_vowel_substrings_brute(w)}"

    print("All tests passed.")
