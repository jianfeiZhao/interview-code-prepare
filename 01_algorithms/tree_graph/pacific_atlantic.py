"""
LeetCode #417 - Pacific Atlantic Water Flow
难度: Medium
高频公司: 字节跳动

题目描述:
有一个 m x n 的矩形岛屿，与太平洋和大西洋相邻：
    - 太平洋：矩阵的左边界和上边界
    - 大西洋：矩阵的右边界和下边界
雨水可以向上下左右四个方向流动（高处流向低处或同高处）。
返回所有能同时流入太平洋和大西洋的单元格坐标。

示例:
    输入: heights = [
        [1,2,2,3,5],
        [3,2,3,4,4],
        [2,4,5,3,1],
        [6,7,1,4,5],
        [5,1,1,2,4]
    ]
    输出: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

约束条件:
    - m == heights.length
    - n == heights[r].length
    - 1 <= m, n <= 200
    - 0 <= heights[r][c] <= 10^5

TL;DR:
    核心思路（逆向思维，多源 BFS/DFS）：
        正向思路（从每个格子出发看能否流到两边）复杂度 O(m*n)^2，太慢。

        逆向思路 ★：从海岸线反向「爬坡」，找出所有能「逆流」到达的格子：
        - 太平洋可达：从上边界+左边界出发，逆向 BFS（下一格 >= 当前格）
        - 大西洋可达：从下边界+右边界出发，逆向 BFS
        - 两个集合的交集即为答案

        方法1 BFS（多源，两次）★
        方法2 DFS（多源，两次）

    复杂度:
        Time O(m * n)，Space O(m * n)
"""

from typing import List
from collections import deque


# ──────────────────────────────────────────────
# 方法1：多源 BFS ★
# ──────────────────────────────────────────────

def pacific_atlantic_bfs(heights: List[List[int]]) -> List[List[int]]:
    """
    多源 BFS 逆向扩展：
    分别从太平洋边界和大西洋边界出发，找出各自可逆流到达的所有格子，取交集。
    """
    if not heights or not heights[0]:
        return []

    m, n = len(heights), len(heights[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def bfs(starts) -> set:
        visited = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n
                        and (nr, nc) not in visited
                        and heights[nr][nc] >= heights[r][c]):  # 逆向：只能爬坡
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return visited

    pacific_starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
    atlantic_starts = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]

    pacific = bfs(pacific_starts)
    atlantic = bfs(atlantic_starts)

    return sorted([r, c] for r, c in pacific & atlantic)


# ──────────────────────────────────────────────
# 方法2：多源 DFS
# ──────────────────────────────────────────────

def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    多源 DFS 逆向扩展：逻辑与 BFS 相同，用递归 DFS 实现。
    """
    if not heights or not heights[0]:
        return []

    m, n = len(heights), len(heights[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r: int, c: int, visited: set) -> None:
        visited.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n
                    and (nr, nc) not in visited
                    and heights[nr][nc] >= heights[r][c]):
                dfs(nr, nc, visited)

    pacific = set()
    atlantic = set()

    for c in range(n):
        dfs(0, c, pacific)
        dfs(m - 1, c, atlantic)

    for r in range(m):
        dfs(r, 0, pacific)
        dfs(r, n - 1, atlantic)

    return sorted([r, c] for r, c in pacific & atlantic)


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: 标准示例
    heights1 = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4]
    ]
    expected1 = sorted([[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]])
    assert sorted(pacific_atlantic_bfs(heights1)) == expected1
    assert sorted(pacific_atlantic(heights1)) == expected1

    # 用例2: 单格子
    assert pacific_atlantic_bfs([[1]]) == [[0, 0]]
    assert pacific_atlantic([[1]]) == [[0, 0]]

    # 用例3: 全相等高度，所有格子都满足
    heights3 = [[1, 1], [1, 1]]
    result3 = sorted(pacific_atlantic(heights3))
    assert result3 == [[0, 0], [0, 1], [1, 0], [1, 1]]

    # 用例4: 1行多列，所有格子同时毗邻两大洋
    heights4 = [[1, 2, 3]]
    result4_bfs = sorted(pacific_atlantic_bfs(heights4))
    result4_dfs = sorted(pacific_atlantic(heights4))
    assert result4_bfs == result4_dfs
    assert [0, 0] in result4_bfs and [0, 2] in result4_bfs

    print("All tests passed!")


if __name__ == "__main__":
    test()
