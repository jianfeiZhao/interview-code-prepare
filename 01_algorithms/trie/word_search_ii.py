"""
题目：单词搜索 II
难度：Hard | 高频出现：字节/阿里/腾讯
标签：Trie、DFS、回溯、矩阵
LeetCode：#212


题目描述
---------
给定一个 m×n 二维字符网格 board 和一个单词（字符串）列表 words，
返回所有同时在二维网格和字典中出现的单词。
单词必须按照字母顺序，通过相邻的单元格内的字母构成；相邻单元格是上下左右，
同一单元格内的字母在一个单词中不允许被重复使用。

示例
------
输入: board=[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
      words=["oath","pea","eat","rain"]
输出: ["eat","oath"]

约束
------
- m == board.length，n == board[i].length，1 <= m, n <= 12
- 1 <= words.length <= 3 * 10^4，1 <= words[i].length <= 10

TL;DR（30秒速览）
- 核心思路：将 words 全部插入 Trie，然后对矩阵每个格子做 DFS+Trie 同步遍历
- 时间 O(M*N*4^L)（L为最长单词长度），空间 O(W*L)（Trie空间）
- 关键陷阱：找到单词后清除 Trie 节点的 word 标记防止重复；DFS 需 visited 标记（原地修改）

详细解析
---------
关键优化：
  1. 在 Trie 节点上直接存 word（到达该节点时说明找到完整单词）
  2. 找到后置 node.word = None，防止重复添加同一单词
  3. 剪枝：若当前 Trie 节点无子节点（叶子）且无 word，可删除节点
  4. 原地修改 board[r][c]='#' 作为 visited 标记，回溯时还原
"""

from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # 存完整单词


def findWords(board: List[List[str]], words: List[str]) -> List[str]:
    # 构建 Trie
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w

    m, n = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]

        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # 去重

        board[r][c] = '#'  # 标记已访问
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = ch  # 回溯

        # 剪枝：删除空叶子节点
        if not next_node.children and not next_node.word:
            del node.children[ch]

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)

    return result


if __name__ == "__main__":
    # 示例1
    board1 = [
        ['o', 'a', 'a', 'n'],
        ['e', 't', 'a', 'e'],
        ['i', 'h', 'k', 'r'],
        ['i', 'f', 'l', 'v'],
    ]
    words1 = ["oath", "pea", "eat", "rain"]
    result1 = findWords(board1, words1)
    assert sorted(result1) == ["eat", "oath"], f"Got {sorted(result1)}"

    # 示例2
    board2 = [['a', 'b'], ['c', 'd']]
    words2 = ["abcd"]
    assert findWords(board2, words2) == []

    # 重复单词
    board3 = [['a', 'a']]
    words3 = ["a"]
    assert findWords(board3, words3) == ['a']  # 只返回一次

    print("All tests passed.")
