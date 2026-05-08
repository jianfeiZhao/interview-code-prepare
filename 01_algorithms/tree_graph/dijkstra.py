"""
题目：Dijkstra 最短路径算法（堆优化）
难度：Medium | 高频出现：字节/阿里/腾讯
标签：图、最短路、堆、贪心
LeetCode：#743 网络延迟时间


题目描述
---------
给定一个带权有向图，从源节点 src 出发，求到所有其他节点的最短路径（Dijkstra 算法）。
Dijkstra 适用于非负权重图，时间复杂度 O((V+E) log V)（堆优化版本）。
常见题型：LeetCode #743 网络延迟时间、#787 K 站中转内最便宜的航班。

示例
------
输入: n=5, edges=[(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)], src=0
输出: {0:0, 1:3, 2:1, 3:4, 4:inf}  （各节点最短距离）

约束
------
- 1 <= n <= 100，边权非负

TL;DR（30秒速览）
- 核心思路：小根堆贪心选当前最短距离的节点，松弛其邻居，直到堆空
- 时间 O((V+E) log V)，空间 O(V+E)
- 关键陷阱：弹出堆时须检查是否已访问（可能存在过期的更大距离）；不适用负权边

详细解析
---------
Dijkstra（堆优化）：
  1. dist[src] = 0，其余 inf，加入堆 (0, src)
  2. 弹出堆顶 (d, u)，若 d > dist[u] 则跳过（过期）
  3. 遍历 u 的邻居 v，若 dist[u] + w < dist[v] 则更新并入堆
  4. 重复直到堆空

#743 应用：
  - 网络有 n 个节点，times[i]=(u,v,w) 表示有向边
  - 从 k 出发，求所有节点收到信号的最小时间
  - 若有节点不可达返回 -1，否则返回 max(dist)
"""

from typing import List
import heapq
from collections import defaultdict


def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    # 建图
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # Dijkstra
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # 过期条目
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1


# ===== 通用 Dijkstra 模板 =====
def dijkstra(graph: dict, src: int) -> dict:
    """
    graph: {node: [(neighbor, weight), ...]}
    返回从 src 到所有节点的最短距离字典
    """
    dist = defaultdict(lambda: float('inf'))
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    return dict(dist)


if __name__ == "__main__":
    # #743 示例1: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2 -> 2
    assert networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2

    # 不可达: n=2, k=1 无出边 -> -1
    assert networkDelayTime([[2, 1, 1]], 2, 2) == 1
    assert networkDelayTime([[1, 2, 1]], 2, 2) == -1

    # 通用模板测试
    g = {1: [(2, 4), (3, 1)], 2: [(4, 1)], 3: [(2, 2), (4, 5)], 4: []}
    d = dijkstra(g, 1)
    assert d[1] == 0
    assert d[2] == 3  # 1->3->2
    assert d[3] == 1
    assert d[4] == 4  # 1->3->2->4

    print("All tests passed.")
