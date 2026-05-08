"""
题目：实现 Trie（前缀树）
难度：Medium | 高频出现：字节/阿里/腾讯
标签：Trie、字典树、设计
LeetCode：#208


题目描述
---------
实现一个 Trie（前缀树），包含 insert、search 和 startsWith 三个操作。
  - insert(word)：向前缀树中插入字符串 word
  - search(word)：如果字符串 word 在前缀树中，返回 True；否则返回 False
  - startsWith(prefix)：如果之前插入的字符串 word 的前缀之一为 prefix，返回 True

示例
------
输入: ["Trie","insert","search","search","startsWith","insert","search"]
      [[],["apple"],["apple"],["app"],["app"],["app"],["app"]]
输出: [null,null,True,False,True,null,True]

约束
------
- 1 <= word.length, prefix.length <= 2000
- word 和 prefix 仅由小写英文字母组成

TL;DR（30秒速览）
- 核心思路：每个节点包含26个子节点指针 + is_end 标志；insert/search/startsWith 均沿路径遍历
- 时间 O(L)（L为单词长度），空间 O(L*26) 最坏
- 关键陷阱：search 需要 is_end 标志；startsWith 只需路径存在

详细解析
---------
TrieNode 结构：
  - children: dict 或 [None]*26
  - is_end: bool

三个操作：
  - insert: 逐字符创建节点，最后设 is_end=True
  - search: 逐字符遍历，路径存在且最后节点 is_end=True
  - startsWith: 逐字符遍历，路径存在即可（不需要 is_end）
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def _get_node(self, prefix: str):
        """辅助：返回 prefix 末尾节点，不存在返回 None"""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


# ===== 数组实现版（固定26字母，更快）=====
class TrieNodeArray:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False


class TrieArray:
    def __init__(self):
        self.root = TrieNodeArray()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            idx = ord(ch) - ord('a')
            if not node.children[idx]:
                node.children[idx] = TrieNodeArray()
            node = node.children[idx]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            idx = ord(ch) - ord('a')
            if not node.children[idx]:
                return False
            node = node.children[idx]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            idx = ord(ch) - ord('a')
            if not node.children[idx]:
                return False
            node = node.children[idx]
        return True


if __name__ == "__main__":
    # 字典版
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    assert trie.startsWith("b") is False

    # 数组版
    trie2 = TrieArray()
    trie2.insert("apple")
    assert trie2.search("apple") is True
    assert trie2.search("app") is False
    assert trie2.startsWith("app") is True
    trie2.insert("app")
    assert trie2.search("app") is True

    print("All tests passed.")
