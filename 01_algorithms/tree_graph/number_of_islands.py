"""
题目：岛屿数量
难度：Medium | 高频出现：字节/美团/阿里
标签：DFS、BFS、图、矩阵
LeetCode：#200


题目描述
---------
给你一个由 '1'（陆地）和 '0'（水）组成的二维网格，请你计算网格中岛屿的数量。
岛屿总是被水包围，并且每座岛屿只能由水平方向和/或垂直方向上相邻的陆地连接形成。
你可以假设该网格的四条边均被水包围。

示例
------
输入: grid = [["1","1","1","1","0"],["1","1","0","1","0"],
              ["1","1","0","0","0"],["0","0","0","0","0"]]
输出: 1

输入: grid = [["1","1","0","0","0"],["1","1","0","0","0"],
              ["0","0","1","0","0"],["0","0","0","1","1"]]
输出: 3

约束
------
- m == grid.length，n == grid[i].length
- 1 <= m, n <= 300，grid[i][j] 为 '0' 或 '1'

TL;DR（30秒速览）
- 思路：遍历矩阵，遇到'1'则 DFS 淹没整个岛（置为'0'），计数+1
- 时间：O(m×n)  空间：O(m×n)（递归栈最坏情况）
- 陷阱：原地修改 grid（或用 visited 集合），避免重复访问

详细解析
---------
DFS 法（推荐）：
  遍历每格，遇到 '1' → 触发 DFS，把四联通的所有 '1' 置为 '0'（沉岛）
  每次触发 DFS 即找到一个新岛屿，计数 +1

BFS 法：把 DFS 换成 BFS 队列，适合栈溢出场景（超大矩阵）

Union-Find 法：
  每个 '1' 初始化为独立集合，遍历时合并相邻 '1'
  最终集合数 = 岛屿数
"""

from typing import List
from collections import deque


def num_islands_dfs(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # 沉岛
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count


def num_islands_bfs(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                queue = deque([(r, c)])
                grid[r][c] = '0'
                while queue:
                    row, col = queue.popleft()
                    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr, nc = row+dr, col+dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
    return count


if __name__ == "__main__":
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert num_islands_dfs(grid1) == 1

    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert num_islands_bfs(grid2) == 3
    print("All tests passed.")
