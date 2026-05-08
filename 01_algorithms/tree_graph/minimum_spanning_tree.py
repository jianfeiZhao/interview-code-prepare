"""
题目：最小生成树（MST）
难度：Medium | 高频出现：字节/阿里
标签：图、并查集、贪心、堆
LeetCode：#1135 最低成本联通所有城市


题目描述
---------
给定一个连通无向带权图，找出一棵最小生成树（MST），使得所有节点连通且边权之和最小。
两种经典算法：
  - Kruskal 算法：按边权排序，用并查集判断是否成环，O(E log E)
  - Prim 算法：从一个顶点开始，每次选择到已选集合距离最小的节点，O((V+E) log V)

示例
------
输入: n=4, edges=[(0,1,1),(0,2,4),(1,2,2),(1,3,5),(2,3,1)]
输出: 最小生成树权重之和 = 4  （选边 0-1, 2-3, 1-2）

约束
------
- 连通无向图，边权非负

TL;DR（30秒速览）
- 核心思路：Kruskal（按边权排序+并查集）或 Prim（最小堆贪心选边）
- 时间 O(E log E)（Kruskal）/ O((V+E) log V)（Prim）
- 关键陷阱：Kruskal必须用并查集检测环；Prim需visited集合防重复访问

详细解析
---------
Kruskal：
  1. 所有边按权重排序
  2. 依次选边，若两端不连通（并查集查找）则加入MST，否则跳过
  3. 选够 V-1 条边结束

Prim（堆优化）：
  1. 任意节点出发，将其所有邻边加入最小堆
  2. 弹出最小边，若目标节点未访问则加入MST
  3. 将新节点的邻边加入堆，重复直到所有节点访问

#1135：无向带权图，返回连通所有城市的最低成本，不可连通返回-1
"""

from typing import List
import heapq


# ===== 并查集 =====
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


# ===== Kruskal =====
def minimumCostKruskal(n: int, connections: List[List[int]]) -> int:
    """
    n: 城市数量 (1-indexed)
    connections: [[u, v, cost], ...]
    """
    uf = UnionFind(n + 1)
    connections.sort(key=lambda x: x[2])
    total_cost = 0
    edges_used = 0

    for u, v, cost in connections:
        if uf.union(u, v):
            total_cost += cost
            edges_used += 1
            if edges_used == n - 1:
                return total_cost

    return -1  # 不可连通


# ===== Prim（堆优化）=====
def minimumCostPrim(n: int, connections: List[List[int]]) -> int:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v, cost in connections:
        graph[u].append((cost, v))
        graph[v].append((cost, u))

    visited = set()
    heap = [(0, 1)]  # (cost, node)，从节点1出发
    total_cost = 0

    while heap and len(visited) < n:
        cost, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total_cost += cost
        for w, v in graph[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v))

    return total_cost if len(visited) == n else -1


if __name__ == "__main__":
    # #1135 示例1: n=3, connections=[[1,2,5],[1,3,6],[2,3,1]] -> 6
    assert minimumCostKruskal(3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]) == 6
    assert minimumCostPrim(3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]) == 6

    # 不可连通: n=4, connections=[[1,2,3],[3,4,4]] -> -1
    assert minimumCostKruskal(4, [[1, 2, 3], [3, 4, 4]]) == -1
    assert minimumCostPrim(4, [[1, 2, 3], [3, 4, 4]]) == -1

    # 示例2: n=4, connections=[[1,2,3],[3,4,4],[2,3,1],[1,4,10]] -> 8
    assert minimumCostKruskal(4, [[1, 2, 3], [3, 4, 4], [2, 3, 1], [1, 4, 10]]) == 8
    assert minimumCostPrim(4, [[1, 2, 3], [3, 4, 4], [2, 3, 1], [1, 4, 10]]) == 8

    print("All tests passed.")
