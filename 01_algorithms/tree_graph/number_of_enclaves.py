"""
题目：飞地的数量 + 统计封闭岛屿的数目
难度：Medium | 高频出现：字节/阿里
标签：DFS/BFS、图
LeetCode：#1020 飞地的数量，#1254 统计封闭岛屿的数目

题目描述
---------
给定一个 m×n 的二进制矩阵 grid，其中 0 表示海洋，1 表示陆地。
"飞地"是指那些无法从矩阵边界出发、通过若干步上下左右移动到达的陆地格子。
请统计并返回矩阵中飞地（无法到达边界的陆地）的格子总数。

示例
------
输入: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
输出: 3（中间的3个陆地格子无法到达边界）

输入: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
输出: 0（所有陆地都与边界相连）

约束
------
- m == grid.length，n == grid[i].length
- 1 <= m, n <= 500
- grid[i][j] 只为 0 或 1

TL;DR（30秒速览）
- 从边界的1出发DFS标记，剩余的1即为飞地（无法到达边界的陆地）
- 时间 O(m*n)，空间 O(m*n)

详细解析
---------
方法：从四条边界的1开始DFS/BFS，标记所有与边界相连的陆地
最终统计未被标记的1的数量
"""

from typing import List
from collections import deque


def num_enclaves(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = 0
        while queue:
            x, y = queue.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = 0
                    queue.append((nx, ny))

    # 标记所有与边界相连的陆地
    for r in range(m):
        for c in range(n):
            if (r == 0 or r == m-1 or c == 0 or c == n-1) and grid[r][c] == 1:
                bfs(r, c)

    return sum(grid[r][c] for r in range(m) for c in range(n))


def closed_island(grid: List[List[int]]) -> int:
    """#1254 统计封闭岛屿（0=陆地，1=水）"""
    m, n = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n:
            return False
        if grid[r][c] == 1:
            return True
        grid[r][c] = 1
        # 4个方向全部为True才是封闭岛屿
        up = dfs(r-1, c)
        down = dfs(r+1, c)
        left = dfs(r, c-1)
        right = dfs(r, c+1)
        return up and down and left and right

    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0 and dfs(r, c):
                count += 1
    return count


if __name__ == "__main__":
    assert num_enclaves([[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]) == 3
    assert num_enclaves([[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]) == 0

    assert closed_island([[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]) == 2
    print("All tests passed.")
