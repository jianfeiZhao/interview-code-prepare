"""
题目：拓扑排序通用模板
难度：Medium | 高频出现：字节/阿里/腾讯
标签：图、拓扑排序、BFS、DFS、DAG
LeetCode：#210 课程表 II


题目描述
---------
给你一个有向图（可能含有环），请对其进行拓扑排序。
如果图中存在环（有向无环图 DAG 的前提被违反），则无法完成拓扑排序。

LeetCode #210 课程表 II：共有 numCourses 门课，prerequisites[i]=[ai,bi] 表示
学习课程 ai 之前必须先学课程 bi，返回完成所有课程所需学习顺序；若不可能完成，返回空数组。

示例
------
输入: numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]
输出: [0,2,1,3] 或 [0,1,2,3]（任意合法顺序）

约束
------
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses*(numCourses-1)

TL;DR（30秒速览）
- 核心思路：Kahn BFS（入度表+队列）或 DFS（后序入栈）均可；检测环时Kahn更直观
- 时间 O(V+E)，空间 O(V+E)
- 关键陷阱：若存在环则无法完成拓扑排序，Kahn法通过结果长度检测；DFS法用颜色标记(0/1/2)

详细解析
---------
Kahn BFS算法：
  1. 统计所有节点入度
  2. 将所有入度为0的节点入队
  3. 弹出节点加入结果，将其邻居入度-1，若入度变为0则入队
  4. 若最终结果长度 < V，则存在环

DFS算法：
  - 颜色标记：0=未访问，1=访问中（检测环），2=已完成
  - 后序顺序入栈，最终翻转得到拓扑序
  - 若访问中遇到颜色1则存在环
"""

from typing import List
from collections import deque, defaultdict


# ===== Kahn BFS 拓扑排序 =====
def findOrderKahn(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    in_degree = [0] * numCourses
    graph = defaultdict(list)

    for course, pre in prerequisites:
        graph[pre].append(course)
        in_degree[course] += 1

    q = deque(i for i in range(numCourses) if in_degree[i] == 0)
    result = []

    while q:
        node = q.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)

    return result if len(result) == numCourses else []


# ===== DFS 拓扑排序 =====
def findOrderDFS(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    for course, pre in prerequisites:
        graph[pre].append(course)

    # 0=未访问, 1=访问中, 2=已完成
    color = [0] * numCourses
    result = []
    has_cycle = [False]

    def dfs(node):
        if has_cycle[0]:
            return
        color[node] = 1
        for neighbor in graph[node]:
            if color[neighbor] == 1:
                has_cycle[0] = True
                return
            if color[neighbor] == 0:
                dfs(neighbor)
        color[node] = 2
        result.append(node)  # 后序

    for i in range(numCourses):
        if color[i] == 0:
            dfs(i)

    if has_cycle[0]:
        return []
    return result[::-1]  # 翻转得到拓扑序


# ===== 通用模板：仅判断是否能完成（#207 课程表）=====
def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    return len(findOrderKahn(numCourses, prerequisites)) == numCourses


if __name__ == "__main__":
    # #210 示例1: numCourses=2, prerequisites=[[1,0]] -> [0,1]
    r = findOrderKahn(2, [[1, 0]])
    assert r == [0, 1], f"Kahn: {r}"

    # 示例2: numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]] -> [0,1,2,3] or [0,2,1,3]
    r2 = findOrderKahn(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert r2[0] == 0 and r2[-1] == 3, f"Kahn: {r2}"

    # 有环: numCourses=2, prerequisites=[[1,0],[0,1]] -> []
    assert findOrderKahn(2, [[1, 0], [0, 1]]) == []
    assert findOrderDFS(2, [[1, 0], [0, 1]]) == []

    # DFS版本
    r3 = findOrderDFS(2, [[1, 0]])
    assert r3 == [0, 1], f"DFS: {r3}"

    r4 = findOrderDFS(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert r4[0] == 0 and r4[-1] == 3, f"DFS: {r4}"

    # canFinish
    assert canFinish(2, [[1, 0]]) is True
    assert canFinish(2, [[1, 0], [0, 1]]) is False

    print("All tests passed.")
