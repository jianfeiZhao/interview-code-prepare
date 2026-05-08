"""
题目: 单词搜索（矩阵中的 DFS）
LeetCode: #79 (Medium)
高频公司: 字节跳动、腾讯

题目描述:
给定一个 m x n 二维字符网格 board 和一个字符串单词 word。
如果 word 存在于网格中，返回 true；否则，返回 false。
单词必须按照字母顺序，通过相邻的单元格内的字母构成，
其中"相邻"单元格是那些水平相邻或垂直相邻的单元格。
同一个单元格内的字母不允许被重复使用。

示例 1: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED" -> True
示例 2: word = "SEE" -> True
示例 3: word = "ABCB" -> False（不能重复使用B）

================================================================================
TL;DR（核心思路）:
- DFS 回溯：从每个匹配首字母的位置出发，向四个方向递归匹配
- 原地标记：将已访问格子临时改为 '#'，回溯时恢复
- 剪枝：越界 / 字母不匹配 / 已访问 时直接返回 False
- 关键优化：若 word 的后缀在 board 中出现次数更少，可翻转 word 提升效率

时间复杂度: O(M * N * 4^L)，L 为 word 长度，实际因剪枝远小于此
空间复杂度: O(L)，递归栈深度
================================================================================
"""

from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """
    DFS + 回溯：从所有可能的起点出发深度搜索。
    原地修改 visited 状态（'#' 标记），回溯时恢复。
    """
    m, n = len(board), len(board[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r: int, c: int, idx: int) -> bool:
        """
        从 (r, c) 出发，尝试匹配 word[idx:]。
        """
        if idx == len(word):
            return True  # 所有字母匹配完毕

        if r < 0 or r >= m or c < 0 or c >= n:
            return False  # 越界

        if board[r][c] != word[idx]:
            return False  # 当前字母不匹配

        # 标记已访问（原地修改，避免额外 visited 集合）
        tmp, board[r][c] = board[r][c], '#'

        # 向四个方向递归
        for dr, dc in directions:
            if dfs(r + dr, c + dc, idx + 1):
                board[r][c] = tmp  # 恢复后再返回（实际上已成功，可不恢复，但好习惯）
                return True

        # 回溯：恢复当前格子
        board[r][c] = tmp
        return False

    # 枚举所有起点
    for r in range(m):
        for c in range(n):
            if dfs(r, c, 0):
                return True

    return False


def exist_with_count_prune(board: List[List[str]], word: str) -> bool:
    """
    优化版：增加频率剪枝。
    - 若 board 中某字母出现次数少于 word 中的次数，直接返回 False
    - 若 word 尾部字母更稀有，可翻转 word 减少搜索空间
    """
    from collections import Counter

    board_count = Counter(c for row in board for c in row)
    word_count = Counter(word)

    # 频率剪枝：board 中字母数量不够
    for ch, cnt in word_count.items():
        if board_count[ch] < cnt:
            return False

    # 若 word 最后一个字母比第一个字母更稀有，翻转 word（减少搜索分支）
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]

    return exist(board, word)


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    board1 = [
        ["A","B","C","E"],
        ["S","F","C","S"],
        ["A","D","E","E"]
    ]

    assert exist([row[:] for row in board1], "ABCCED") == True
    assert exist([row[:] for row in board1], "SEE") == True
    assert exist([row[:] for row in board1], "ABCB") == False  # 不能重复
    assert exist([row[:] for row in board1], "ABCCED") == True

    # 单格
    assert exist([["a"]], "a") == True
    assert exist([["a"]], "b") == False

    # 蛇形路径
    board2 = [
        ["A","B","C","D"],
        ["E","F","G","H"],
        ["I","J","K","L"]
    ]
    assert exist([row[:] for row in board2], "ABCDHGFELKJI") == True  # 蛇形
    assert exist([row[:] for row in board2], "ABCDEFGHIJKL") == False

    # 全相同字符
    board3 = [["a","a"],["a","a"]]
    assert exist([row[:] for row in board3], "aaa") == True
    assert exist([row[:] for row in board3], "aaaaa") == False  # 只有4个a

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"ABCCED: {exist([row[:] for row in board1], 'ABCCED')}")  # True
    print(f"SEE:    {exist([row[:] for row in board1], 'SEE')}")     # True
    print(f"ABCB:   {exist([row[:] for row in board1], 'ABCB')}")    # False
