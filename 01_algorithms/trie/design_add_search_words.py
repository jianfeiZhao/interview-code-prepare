"""
题目：添加与搜索单词 - 数据结构设计
难度：Medium | 高频出现：字节/阿里
标签：Trie、DFS、通配符
LeetCode：#211


题目描述
---------
设计一个数据结构，支持向数据结构中添加新单词和查找字符串是否与之前添加的任何字符串匹配。
  - addWord(word)：将 word 添加到数据结构中
  - search(word)：如果数据结构中存在字符串与 word 匹配，则返回 True；否则返回 False
  - word 中可能包含 '.'，'.' 可以匹配任何字母

示例
------
输入: ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
      [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
输出: [null,null,null,null,False,True,True,True]

约束
------
- 1 <= word.length <= 25，addWord 中 word 仅含小写英文字母
- search 中 word 仅含 '.' 或小写英文字母，最多包含 2 个 '.'

TL;DR（30秒速览）
- 核心思路：Trie存储单词，search时遇到'.'则递归遍历当前节点所有子节点
- 时间 insert O(L)，search O(L) 最好 / O(26^L) 最坏（全'.'），空间 O(总字符数)
- 关键陷阱：'.'通配符需要遍历所有子节点；DFS搜索时提前返回True可剪枝

详细解析
---------
- 普通字符：正常 Trie 遍历
- '.' 通配符：遍历当前节点所有子节点，对每个子节点递归搜索剩余模式
- 实现中用递归DFS更清晰
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        return self._dfs(word, 0, self.root)

    def _dfs(self, word: str, idx: int, node: TrieNode) -> bool:
        if idx == len(word):
            return node.is_end

        ch = word[idx]
        if ch == '.':
            # 通配符：尝试所有子节点
            for child in node.children.values():
                if self._dfs(word, idx + 1, child):
                    return True
            return False
        else:
            if ch not in node.children:
                return False
            return self._dfs(word, idx + 1, node.children[ch])


if __name__ == "__main__":
    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")

    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True
    assert wd.search("...") is True
    assert wd.search("b.d") is True
    assert wd.search("b.x") is False

    # 长度不匹配
    assert wd.search("ba") is False
    assert wd.search("badd") is False

    # 只有通配符
    wd2 = WordDictionary()
    wd2.addWord("a")
    assert wd2.search(".") is True
    assert wd2.search("..") is False

    print("All tests passed.")
