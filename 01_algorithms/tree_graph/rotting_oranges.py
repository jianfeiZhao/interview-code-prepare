"""
题目：腐烂的橘子
难度：Medium | 高频出现：字节/阿里/腾讯
标签：多源BFS、图
LeetCode：#994


题目描述
---------
给你一个 m x n 的网格 grid，每个单元格有三种可能的值：
  0：代表空单元格，1：代表新鲜橘子，2：代表腐烂的橘子。
每分钟，腐烂的橘子周围（上下左右）每个新鲜橘子都会变成腐烂橘子。
返回让所有橘子腐烂所必须经过的最小分钟数。如果不可能使所有橘子腐烂，返回 -1。

示例
------
输入: grid = [[2,1,1],[1,1,0],[0,1,1]]
输出: 4

输入: grid = [[2,1,1],[0,1,1],[1,0,1]]
输出: -1

约束
------
- m == grid.length，n == grid[i].length
- 1 <= m, n <= 10，grid[i][j] ∈ {0, 1, 2}

TL;DR（30秒速览）
- 多源BFS：将所有初始腐烂橘子同时入队，BFS层序扩散
- 最后检查是否还有新鲜橘子
- 时间 O(m*n)，空间 O(m*n)

详细解析
---------
将所有腐烂橘子(值为2)加入初始队列，BFS每轮（每分钟）向四周扩散。
扩散完后若还有值为1的橘子则返回-1，否则返回分钟数。
注意：初始没有新鲜橘子时返回0。
"""

from typing import List
from collections import deque


def oranges_rotting(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                queue.append((nr, nc, t+1))

    return minutes if fresh == 0 else -1


if __name__ == "__main__":
    assert oranges_rotting([[2,1,1],[1,1,0],[0,1,1]]) == 4
    assert oranges_rotting([[2,1,1],[0,1,1],[1,0,1]]) == -1
    assert oranges_rotting([[0,2]]) == 0
    assert oranges_rotting([[1]]) == -1
    assert oranges_rotting([[0]]) == 0
    print("All tests passed.")
