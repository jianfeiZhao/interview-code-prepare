"""
题目：被围绕的区域
难度：Medium | 高频出现：字节/阿里
标签：DFS、BFS、并查集、矩阵
LeetCode：#130

题目描述
---------
给定一个 m×n 的字符矩阵 board，包含 'X' 和 'O' 两种字符。
找出所有被 'X' 围绕的区域，并将这些区域内所有的 'O' 替换为 'X'（原地修改）。
"被围绕"指该区域中的 'O' 不与矩阵边界上的 'O' 直接或间接相连（四方向连通）。

示例
------
输入: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
输出: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
（第4行的 'O' 与边界相连，保留；内部的 'O' 被围绕，替换为 'X'）

输入: board = [["X"]]
输出: [["X"]]

约束
------
- m == board.length，n == board[i].length
- 1 <= m, n <= 200
- board[i][j] 只为 'X' 或 'O'

TL;DR（30秒速览）
- 核心思路：从边界出发DFS/BFS标记所有与边界连通的'O'，最后把未标记的'O'翻转为'X'
- 时间 O(m*n)，空间 O(m*n)
- 关键陷阱：不能直接DFS标记内部'O'（难以判断是否与边界连通），逆向思维从边界入手更简单

详细解析
---------
步骤：
  1. 遍历4条边界，将所有'O'及其连通的'O'标记为临时字符'S'
  2. 遍历整个矩阵：'S'->'O'（恢复），'O'->'X'（填充），'X'不变
"""

from typing import List


def solve(board: List[List[str]]) -> None:
    if not board or not board[0]:
        return
    m, n = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != 'O':
            return
        board[r][c] = 'S'  # 标记为安全
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Step1: 从四条边界出发标记
    for r in range(m):
        dfs(r, 0)
        dfs(r, n - 1)
    for c in range(n):
        dfs(0, c)
        dfs(m - 1, c)

    # Step2: 翻转
    for r in range(m):
        for c in range(n):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O'


# BFS 版本（避免递归栈溢出）
def solve_bfs(board: List[List[str]]) -> None:
    if not board or not board[0]:
        return
    from collections import deque
    m, n = len(board), len(board[0])
    q = deque()

    # 收集边界'O'
    for r in range(m):
        for c in [0, n - 1]:
            if board[r][c] == 'O':
                q.append((r, c))
                board[r][c] = 'S'
    for c in range(1, n - 1):
        for r in [0, m - 1]:
            if board[r][c] == 'O':
                q.append((r, c))
                board[r][c] = 'S'

    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 'O':
                board[nr][nc] = 'S'
                q.append((nr, nc))

    for r in range(m):
        for c in range(n):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O'


if __name__ == "__main__":
    board1 = [
        ['X', 'X', 'X', 'X'],
        ['X', 'O', 'O', 'X'],
        ['X', 'X', 'O', 'X'],
        ['X', 'O', 'X', 'X'],
    ]
    solve(board1)
    expected1 = [
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['X', 'O', 'X', 'X'],
    ]
    assert board1 == expected1, f"Got {board1}"

    board2 = [['X']]
    solve(board2)
    assert board2 == [['X']]

    # BFS版本
    board3 = [
        ['X', 'X', 'X', 'X'],
        ['X', 'O', 'O', 'X'],
        ['X', 'X', 'O', 'X'],
        ['X', 'O', 'X', 'X'],
    ]
    solve_bfs(board3)
    assert board3 == expected1

    print("All tests passed.")
