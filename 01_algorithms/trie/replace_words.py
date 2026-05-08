"""
题目：单词替换
难度：Medium | 高频出现：字节/阿里
标签：Trie、哈希表、字符串
LeetCode：#648


题目描述
---------
在英语中，我们有一个叫做词根的概念，可以跟着其他一些词组合在一起，形成另一个较长的单词——
这个词被称为继承词（successor）。例如，词根 an 可以形成 another、annual 等。
给你一个字典（词根列表）dictionary 和一个句子 sentence（句子中含有若干个单词），
将句子中的所有继承词替换为词根（选择最短的词根），最后返回替换后的句子。

示例
------
输入: dictionary=["cat","bat","rat"], sentence="the cattle was rattled by the battery"
输出: "the cat was rat by the bat"

约束
------
- 1 <= dictionary.length <= 1000，1 <= dictionary[i].length <= 100
- 1 <= sentence.length <= 10^6，句子中单词由空格分隔

TL;DR（30秒速览）
- 核心思路：将所有词根插入 Trie，对句子每个单词做 Trie 前缀匹配，找到最短词根则替换
- 时间 O(sum_root_len + sum_word_len)，空间 O(sum_root_len)
- 关键陷阱：应找最短词根（最先到达 is_end 的节点）；哈希集合法更简单但略慢

详细解析
---------
方法1（Trie）：
  - 插入所有词根，搜索时遇到 is_end=True 立即返回该前缀

方法2（排序+哈希集合）：
  - 将词根按长度排序后存入集合，对每个单词逐步截断查找
  - 代码更简单，时间复杂度相同

面试推荐：先说 Trie 思路，实现时可选哈希集合简化代码
"""

from typing import List


# ===== 方法1：Trie =====
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


def replaceWordsTrie(dictionary: List[str], sentence: str) -> str:
    # 构建 Trie
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def find_root(word):
        node = root
        for i, ch in enumerate(word):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_end:
                return word[:i + 1]
        return word

    return ' '.join(find_root(w) for w in sentence.split())


# ===== 方法2：哈希集合 =====
def replaceWordsHash(dictionary: List[str], sentence: str) -> str:
    root_set = set(dictionary)

    def find_root(word):
        for i in range(1, len(word) + 1):
            if word[:i] in root_set:
                return word[:i]
        return word

    return ' '.join(find_root(w) for w in sentence.split())


if __name__ == "__main__":
    # 示例1: dictionary=["cat","bat","rat"], sentence="the cattle was rattled by the battery"
    # -> "the cat was rat by the bat"
    d1 = ["cat", "bat", "rat"]
    s1 = "the cattle was rattled by the battery"
    expected1 = "the cat was rat by the bat"
    assert replaceWordsTrie(d1, s1) == expected1
    assert replaceWordsHash(d1, s1) == expected1

    # 示例2: dictionary=["a","b","c"], sentence="aadsfasf absbs bbab cadsfafs"
    # -> "a a b c"
    d2 = ["a", "b", "c"]
    s2 = "aadsfasf absbs bbab cadsfafs"
    expected2 = "a a b c"
    assert replaceWordsTrie(d2, s2) == expected2
    assert replaceWordsHash(d2, s2) == expected2

    # 无词根匹配
    assert replaceWordsTrie(["abc"], "xyz def") == "xyz def"

    print("All tests passed.")
