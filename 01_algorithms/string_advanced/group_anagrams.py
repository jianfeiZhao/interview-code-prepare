"""
LeetCode #49 - 字母异位词分组 (Group Anagrams)
难度: Medium | 频率: 字节/腾讯/阿里

=== 题目描述 ===
给你一个字符串数组，请你将字母异位词组合在一起。可以按任意顺序返回结果列表。
字母异位词是由重新排列源单词的所有字母得到的一个新单词。

示例 1:
  输入: strs = ["eat","tea","tan","ate","nat","bat"]
  输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

示例 2:
  输入: strs = [""]
  输出: [[""]]

示例 3:
  输入: strs = ["a"]
  输出: [["a"]]

=== TL;DR ===
核心思路: 为每个字符串找到一个"规范形式"作为哈希Key，相同Key的字符串归为一组。
  方法1（排序Key）: 对每个字符串排序得到Key，如 "eat"->"aet"，用字典分组
  方法2（计数Key）: 用长度26的字符计数元组做Key，避免排序的 O(k log k) 开销

时间复杂度: O(n * k log k)，n 为字符串数量，k 为最长字符串长度
  方法2: O(n * k)，k 为最长字符串长度
空间复杂度: O(n * k)，存储所有字符串

=== 详细解析 ===
关键技巧:
1. 排序Key: tuple(sorted(s)) 或 "".join(sorted(s)) 都可作为字典key
2. 计数Key: tuple([count[i] for i in range(26)])，用tuple而非list（list不可哈希）
3. defaultdict(list) 自动初始化，避免手动判断key是否存在
4. 返回 list(groups.values()) 即可
5. 面试中方法1（排序）代码更简洁，是首选答案；方法2是优化版
"""

from collections import defaultdict


# ===== 方法1: 排序作为Key（推荐，代码简洁）=====
def group_anagrams_sort(strs: list) -> list:
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))   # "eat" -> ('a','e','t')
        groups[key].append(s)
    return list(groups.values())


# ===== 方法2: 字符计数元组作为Key（O(n*k) 时间）=====
def group_anagrams_count(strs: list) -> list:
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)       # 26个整数组成的不可变元组
        groups[key].append(s)
    return list(groups.values())


# ===== 辅助：结果规范化（用于断言比较）=====
def normalize(result: list) -> list:
    return sorted([sorted(group) for group in result])


# ===== 测试 =====
if __name__ == "__main__":
    # 示例1
    strs1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected1 = [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert normalize(group_anagrams_sort(strs1)) == normalize(expected1)
    assert normalize(group_anagrams_count(strs1)) == normalize(expected1)

    # 示例2: 空字符串
    strs2 = [""]
    assert normalize(group_anagrams_sort(strs2)) == [[""]]
    assert normalize(group_anagrams_count(strs2)) == [[""]]

    # 示例3: 单字符
    strs3 = ["a"]
    assert normalize(group_anagrams_sort(strs3)) == [["a"]]

    # 边界: 全部相同
    strs4 = ["abc", "bca", "cab"]
    assert len(group_anagrams_sort(strs4)) == 1

    # 边界: 全部不同
    strs5 = ["abc", "def", "ghi"]
    assert len(group_anagrams_sort(strs5)) == 3

    print("All tests passed!")
