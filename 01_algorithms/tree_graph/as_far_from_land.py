"""
题目：地图分析（离陆地最远的海洋）
难度：Medium | 高频出现：字节/阿里
标签：多源BFS、图
LeetCode：#1162

题目描述
---------
给定一个 n×n 的整数矩阵 grid，其中 0 表示海洋，1 表示陆地。
找到一个海洋格子，使其到距离最近陆地格子的曼哈顿距离最大，返回这个最大距离。
如果矩阵中全是陆地或全是海洋，则返回 -1。曼哈顿距离定义为 |x1-x2| + |y1-y2|。

示例
------
输入: grid = [[1,0,1],[0,0,0],[1,0,1]]
输出: 2（中心格子 (1,1) 到最近陆地距离为 2）

输入: grid = [[1,0,0],[0,0,0],[0,0,0]]
输出: 4（右下角 (2,2) 到最近陆地距离为 4）

约束
------
- n == grid.length == grid[i].length
- 1 <= n <= 100
- grid[i][j] 只为 0 或 1

TL;DR（30秒速览）
- 多源BFS：从所有陆地同时出发，BFS每步扩展，最后一个到达的海洋距离即为答案
- 时间 O(m*n)，空间 O(m*n)

详细解析
---------
与腐烂橘子类似的多源BFS模式：
  从所有1出发BFS，每到一个0格子更新其到最近陆地的距离
  最大距离即为答案
"""

from typing import List
from collections import deque


def max_distance(grid: List[List[int]]) -> int:
    n = len(grid)
    queue = deque()
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                queue.append((r, c))

    if len(queue) == 0 or len(queue) == n * n:
        return -1  # 全陆地或全海洋

    dist = -1
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = grid[r][c] + 1
                dist = max(dist, grid[nr][nc] - 1)
                queue.append((nr, nc))
    return dist


if __name__ == "__main__":
    assert max_distance([[1,0,1],[0,0,0],[1,0,1]]) == 2
    assert max_distance([[1,0,0],[0,0,0],[0,0,0]]) == 4
    assert max_distance([[1,1],[1,1]]) == -1
    assert max_distance([[0,0],[0,0]]) == -1
    print("All tests passed.")
