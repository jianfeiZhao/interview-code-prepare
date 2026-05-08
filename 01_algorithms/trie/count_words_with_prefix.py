"""
题目：统计包含给定前缀的字符串数目
难度：Easy | 高频出现：字节
标签：Trie、字符串、计数
LeetCode：#2185


题目描述
---------
给你一个字符串数组 words 和一个字符串 pref，统计并返回数组 words 中以 pref 为前缀的字符串的数目。
一个字符串 word 的前缀是 word 的从首字符开始的连续子字符串。

示例
------
输入: words = ["pay","attention","practice","attend"], pref = "at"
输出: 2  （"attention" 和 "attend"）

输入: words = ["leetcode","win","loops","success"], pref = "code"
输出: 0

约束
------
- 1 <= words.length <= 100，1 <= words[i].length, pref.length <= 100
- words[i] 和 pref 由小写英文字母组成

TL;DR（30秒速览）
- 核心思路：直接遍历所有单词检查 startswith 最简单；Trie解法可批量查询多前缀
- 时间 O(n*L) 直接法 / O(总字符+查询) Trie法，空间 O(1) / O(总字符)
- 关键陷阱：本题为Easy，直接 str.startswith 即可；Trie适合多次不同前缀查询场景

详细解析
---------
方法1（直接法，推荐 Easy）：
  - [w for w in words if w.startswith(pref)] 一行解决

方法2（Trie，适合多次查询）：
  - 每个节点存 count（经过该节点的字符串数）
  - 查询时走到 prefix 末尾节点，直接返回 count
"""

from typing import List


# ===== 方法1：直接法 =====
def prefixCount(words: List[str], pref: str) -> int:
    return sum(1 for w in words if w.startswith(pref))


# ===== 方法2：Trie（适合批量查询）=====
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # 经过该节点的字符串数


class PrefixTrie:
    def __init__(self, words: List[str]):
        self.root = TrieNode()
        for w in words:
            self._insert(w)

    def _insert(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1

    def count_prefix(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count


if __name__ == "__main__":
    # 示例1: words=["pay","attention","practice","attend"], pref="at" -> 2
    assert prefixCount(["pay", "attention", "practice", "attend"], "at") == 2

    # 示例2: words=["leetcode","win","loops","success"], pref="code" -> 0
    assert prefixCount(["leetcode", "win", "loops", "success"], "code") == 0

    # Trie版本
    trie = PrefixTrie(["pay", "attention", "practice", "attend"])
    assert trie.count_prefix("at") == 2
    assert trie.count_prefix("pay") == 1
    assert trie.count_prefix("code") == 0
    assert trie.count_prefix("") == 0  # 空前缀（root无count）

    # 边界
    assert prefixCount([], "a") == 0
    assert prefixCount(["a"], "a") == 1
    assert prefixCount(["ab"], "abc") == 0  # prefix比单词长

    print("All tests passed.")
