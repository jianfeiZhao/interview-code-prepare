"""
LeetCode #547 - Number of Provinces
难度: Medium
高频公司: 字节跳动 / 腾讯

题目描述:
有 n 个城市，其中一些彼此相连，另一些没有相连。如果城市 a 与城市 b 直接相连，
且城市 b 与城市 c 直接相连，那么城市 a 与城市 c 间接相连。
省份是一组直接或间接相连的城市，组内不含其他没有相连的城市。
给你一个 n x n 的矩阵 isConnected，其中 isConnected[i][j] = 1 表示第 i 个城市和
第 j 个城市直接相连，而 isConnected[i][j] = 0 表示二者不直接相连。
返回矩阵中省份的数量。

示例:
    输入: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
    输出: 2

    输入: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
    输出: 3

约束条件:
    - 1 <= n <= 200
    - n == isConnected.length
    - n == isConnected[i].length
    - isConnected[i][j] 为 1 或 0
    - isConnected[i][i] == 1
    - isConnected[i][j] == isConnected[j][i]

TL;DR:
    核心思路（三种方法，本质都是连通分量计数）：
        方法1 DFS：从未访问节点出发 DFS，每次 DFS 标记一个连通分量，计数+1
        方法2 BFS：同 DFS，用队列实现
        方法3 并查集（Union-Find） ★ 面试加分项：
            初始化 n 个独立集合，根据矩阵合并相连城市，
            最终统计不同根节点的数量即为省份数。
            路径压缩 + 按秩合并使近似 O(n*alpha(n)) ~ O(n)

    复杂度:
        DFS/BFS: Time O(n^2), Space O(n)
        并查集:   Time O(n^2 * alpha(n)), Space O(n)
"""

from typing import List
from collections import deque


# ──────────────────────────────────────────────
# 方法1：DFS
# ──────────────────────────────────────────────

def find_circle_num_dfs(isConnected: List[List[int]]) -> int:
    """DFS 遍历，每次从未访问节点出发遍历整个连通分量。"""
    n = len(isConnected)
    visited = [False] * n

    def dfs(city: int) -> None:
        visited[city] = True
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    provinces = 0
    for i in range(n):
        if not visited[i]:
            dfs(i)
            provinces += 1
    return provinces


# ──────────────────────────────────────────────
# 方法2：BFS
# ──────────────────────────────────────────────

def find_circle_num_bfs(isConnected: List[List[int]]) -> int:
    """BFS 遍历，每次从未访问节点出发遍历整个连通分量。"""
    n = len(isConnected)
    visited = [False] * n
    provinces = 0

    for i in range(n):
        if not visited[i]:
            queue = deque([i])
            visited[i] = True
            while queue:
                city = queue.popleft()
                for neighbor in range(n):
                    if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            provinces += 1

    return provinces


# ──────────────────────────────────────────────
# 方法3：并查集（Union-Find） ★
# ──────────────────────────────────────────────

class UnionFind:
    """
    带路径压缩和按秩合并的并查集。
    - find：路径压缩，将所有节点直接连到根
    - union：按秩合并，将矮树挂到高树上
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # 连通分量数

    def find(self, x: int) -> int:
        """路径压缩（递归版）。"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """按秩合并。"""
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1

    def get_count(self) -> int:
        return self.count


def find_circle_num(isConnected: List[List[int]]) -> int:
    """并查集解法，统计连通分量数。"""
    n = len(isConnected)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):  # 只遍历上三角，避免重复
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.get_count()


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: [[1,1,0],[1,1,0],[0,0,1]] -> 2
    conn1 = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    assert find_circle_num_dfs(conn1) == 2
    assert find_circle_num_bfs(conn1) == 2
    assert find_circle_num(conn1) == 2

    # 用例2: [[1,0,0],[0,1,0],[0,0,1]] -> 3 (全部独立)
    conn2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert find_circle_num_dfs(conn2) == 3
    assert find_circle_num_bfs(conn2) == 3
    assert find_circle_num(conn2) == 3

    # 用例3: 全部相连 [[1,1,1],[1,1,1],[1,1,1]] -> 1
    conn3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert find_circle_num_dfs(conn3) == 1
    assert find_circle_num_bfs(conn3) == 1
    assert find_circle_num(conn3) == 1

    # 用例4: 单个城市 [[1]] -> 1
    conn4 = [[1]]
    assert find_circle_num_dfs(conn4) == 1
    assert find_circle_num_bfs(conn4) == 1
    assert find_circle_num(conn4) == 1

    # 用例5: 链式连接 0-1-2 -> 1
    conn5 = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
    assert find_circle_num_dfs(conn5) == 1
    assert find_circle_num_bfs(conn5) == 1
    assert find_circle_num(conn5) == 1

    print("All tests passed!")


if __name__ == "__main__":
    test()
