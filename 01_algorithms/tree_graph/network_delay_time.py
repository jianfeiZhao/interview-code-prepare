"""
题目：网络延迟时间
难度：Medium | 高频出现：字节/阿里
标签：Dijkstra、图
LeetCode：#743


题目描述
---------
有 n 个网络节点，标记为 1 到 n。给你一个列表 times，表示信号经过有向边的传递时间。
times[i] = (ui, vi, wi)，其中 ui 是源节点，vi 是目标节点，wi 是信号传递的时间。
现在从节点 k 发出一个信号，需要多久才能使所有节点都收到信号？
如果不能使所有节点收到信号，返回 -1。

示例
------
输入: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2
输出: 2

约束
------
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- 0 <= wi <= 100，图中可能有重边

TL;DR（30秒速览）
- Dijkstra最短路：从源节点k出发，找到所有节点的最短路径
- 答案为最短路中的最大值（等待所有节点收到信号的时间）
- 时间 O((V+E) log V)，空间 O(V+E)

详细解析
---------
Dijkstra堆优化模板：
  dist[k]=0，其他=inf
  小顶堆按距离排序，每次取出最近节点更新邻居
  最终 max(dist.values()) 即为答案
"""

from typing import List
import heapq
from collections import defaultdict


def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n+1)}
    dist[k] = 0
    heap = [(0, k)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    ans = max(dist.values())
    return ans if ans < float('inf') else -1


if __name__ == "__main__":
    assert network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2) == 2
    assert network_delay_time([[1,2,1]], 2, 1) == 1
    assert network_delay_time([[1,2,1]], 2, 2) == -1
    print("All tests passed.")
