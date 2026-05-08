"""
LeetCode #207 - Course Schedule
难度: Medium
高频公司: 字节跳动 / 阿里巴巴

题目描述:
你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses-1。
在选修某些课程之前需要完成一些其他课程的学习，先修课程关系以
prerequisites[i] = [a_i, b_i] 给出，意味着必须先修完课程 b_i 才能修 a_i。
请你判断是否可能完成所有课程的学习（即图中是否有环）。

示例:
    输入: numCourses = 2, prerequisites = [[1,0]]
    输出: True  (先学0，再学1)

    输入: numCourses = 2, prerequisites = [[1,0],[0,1]]
    输出: False  (循环依赖)

约束条件:
    - 1 <= numCourses <= 2000
    - 0 <= prerequisites.length <= 5000
    - prerequisites[i].length == 2
    - 0 <= a_i, b_i < numCourses
    - 所有先决条件对互不相同

TL;DR:
    核心思路（本质：有向图判环）：
        方法1 拓扑排序（BFS / Kahn's 算法） ★：
            计算每个节点的入度，将所有入度为 0 的节点入队。
            BFS：弹出节点，减少其后继节点的入度；若后继入度变为 0 则入队。
            最终若所有节点都被处理（count == numCourses），说明无环。

        方法2 DFS 染色判环：
            维护节点状态：0=未访问，1=访问中（在当前 DFS 路径上），2=已完成。
            DFS 过程中若遇到状态为 1 的节点，说明存在环。

    复杂度:
        Time O(V + E)，Space O(V + E)
        V = numCourses, E = prerequisites.length
"""

from typing import List
from collections import deque, defaultdict


# ──────────────────────────────────────────────
# 方法1：拓扑排序 BFS（Kahn's 算法） ★
# ──────────────────────────────────────────────

def can_finish_bfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Kahn's 算法拓扑排序。
    若能完成拓扑排序（处理了所有节点），则无环，可以完成所有课程。
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0

    while queue:
        course = queue.popleft()
        count += 1
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return count == numCourses


# 保留原始接口名，兼容旧测试
def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    return can_finish_bfs(num_courses, prerequisites)


# ──────────────────────────────────────────────
# 方法2：DFS 染色判环
# ──────────────────────────────────────────────

def can_finish_dfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    DFS 三色标记判环：
        0 = 未访问（白色）
        1 = 访问中（灰色，在当前 DFS 路径上）
        2 = 已完成（黑色，无环确认）
    遇到灰色节点说明有环。
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    state = [0] * numCourses

    def has_cycle(node: int) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        state[node] = 2
        return False

    for i in range(numCourses):
        if has_cycle(i):
            return False
    return True


# ──────────────────────────────────────────────
# 扩展：#210 Course Schedule II（返回具体的拓扑顺序）
# ──────────────────────────────────────────────

def find_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    LeetCode #210：返回学习课程的拓扑顺序，若有环则返回空列表。
    在 Kahn's 算法基础上，记录出队顺序即为拓扑序。
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return order if len(order) == numCourses else []


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: 无环 [[1,0]] -> True
    assert can_finish_bfs(2, [[1, 0]]) is True
    assert can_finish_dfs(2, [[1, 0]]) is True

    # 用例2: 有环 [[1,0],[0,1]] -> False
    assert can_finish_bfs(2, [[1, 0], [0, 1]]) is False
    assert can_finish_dfs(2, [[1, 0], [0, 1]]) is False

    # 用例3: 单门课程，无依赖 -> True
    assert can_finish_bfs(1, []) is True
    assert can_finish_dfs(1, []) is True

    # 用例4: 复杂有环 [[1,0],[2,1],[0,2]] -> False
    assert can_finish_bfs(3, [[1, 0], [2, 1], [0, 2]]) is False
    assert can_finish_dfs(3, [[1, 0], [2, 1], [0, 2]]) is False

    # 用例5: 复杂无环 [[1,0],[2,0],[3,1],[3,2]] -> True
    assert can_finish_bfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
    assert can_finish_dfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True

    # 用例6: find_order 验证拓扑序合法性
    order = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert len(order) == 4
    pos = {v: i for i, v in enumerate(order)}
    for a, b in [[1, 0], [2, 0], [3, 1], [3, 2]]:
        assert pos[b] < pos[a], f"Invalid order: {order}"

    # 用例7: 有环 -> []
    assert find_order(2, [[1, 0], [0, 1]]) == []

    print("All tests passed!")


if __name__ == "__main__":
    test()
