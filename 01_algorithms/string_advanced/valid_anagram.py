"""
LeetCode #242 - 有效的字母异位词 (Valid Anagram)
难度: Easy | 频率: 全系必考

=== 题目描述 ===
给定两个字符串 s 和 t，编写一个函数来判断 t 是否是 s 的字母异位词。
注意：若 s 和 t 中每个字符出现的次数都相同，则称 s 和 t 互为字母异位词。

示例 1:
  输入: s = "anagram", t = "nagaram"
  输出: true

示例 2:
  输入: s = "rat", t = "car"
  输出: false

进阶: 如果输入字符串包含 unicode 字符怎么办？

=== TL;DR ===
核心思路: 统计两个字符串中每个字符的频次，判断频次是否完全相同。
  方法1（哈希表/Counter）: 用字典统计字符频次后对比 — O(n) 时间，O(1)/O(k) 空间
  方法2（排序）: 对两个字符串排序后直接比较 — O(n log n) 时间，O(n) 空间
  方法3（数组）: 仅限小写字母，用长度26的数组代替哈希表 — O(n) 时间，O(1) 空间

时间复杂度: O(n)，n 为字符串长度
空间复杂度: O(1)（字符集固定为26个小写字母时）；O(k) 处理 unicode 时，k 为字符种数

=== 详细解析 ===
关键技巧:
1. 若 len(s) != len(t)，直接返回 False（剪枝）
2. 方法1: collections.Counter(s) == collections.Counter(t) 一行搞定
3. 方法2: sorted(s) == sorted(t)，最简洁但不是最优
4. 方法3: 用 ord(c) - ord('a') 做下标，遍历s时+1，遍历t时-1，最后全零则是异位词
5. 进阶 unicode：改用通用 Counter/字典，空间变为 O(k)
"""

from collections import Counter


# ===== 方法1: Counter 对比（推荐，最简洁）=====
def is_anagram_counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


# ===== 方法2: 排序后对比 =====
def is_anagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)


# ===== 方法3: 26位数组（仅小写字母，最优）=====
def is_anagram_array(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    for c in t:
        count[ord(c) - ord('a')] -= 1
        if count[ord(c) - ord('a')] < 0:
            return False
    return True


# ===== 方法4: 单次遍历哈希（支持 unicode）=====
def is_anagram_unicode(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq: dict = {}
    for cs, ct in zip(s, t):
        freq[cs] = freq.get(cs, 0) + 1
        freq[ct] = freq.get(ct, 0) - 1
    return all(v == 0 for v in freq.values())


# ===== 测试 =====
if __name__ == "__main__":
    # 基础测试
    assert is_anagram_counter("anagram", "nagaram") == True
    assert is_anagram_counter("rat", "car") == False
    assert is_anagram_counter("", "") == True
    assert is_anagram_counter("a", "b") == False
    assert is_anagram_counter("ab", "ba") == True

    assert is_anagram_sort("anagram", "nagaram") == True
    assert is_anagram_sort("rat", "car") == False

    assert is_anagram_array("anagram", "nagaram") == True
    assert is_anagram_array("rat", "car") == False
    assert is_anagram_array("ab", "a") == False

    assert is_anagram_unicode("anagram", "nagaram") == True
    assert is_anagram_unicode("rat", "car") == False

    # 边界测试
    assert is_anagram_array("aab", "baa") == True
    assert is_anagram_array("aaab", "aab") == False

    print("All tests passed!")
