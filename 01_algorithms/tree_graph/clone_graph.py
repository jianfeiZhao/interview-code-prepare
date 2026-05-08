"""
LeetCode #133 - Clone Graph
难度: Medium
高频公司: 字节跳动 / 阿里巴巴

题目描述:
给你无向连通图中一个节点的引用，请你返回该图的深拷贝（克隆）。
图中的每个节点都包含它的值 val（int）和其邻居的列表（list[Node]）。

测试用例格式：
    简单起见，每个节点的值都和它的索引相同（从 1 开始）。
    给定节点将始终是图中第一个节点（值为 1）。
    以 邻接表 形式给出整个图。

示例:
    输入: adjList = [[2,4],[1,3],[2,4],[1,3]]
    输出: [[2,4],[1,3],[2,4],[1,3]]
    解释: 图中有 4 个节点，节点1的邻居是[2,4]，以此类推

约束条件:
    - 节点数不超过 100
    - 每个节点值 Node.val 都是唯一的 [1, 100]
    - 无重复边，无自环
    - 图是连通的（可从任意节点到达所有节点）

TL;DR:
    核心思路：
        DFS / BFS + 哈希表（visited）：
        用哈希表 {原节点: 克隆节点} 避免重复克隆（处理图中的环）。

        方法1 DFS（递归）：
            若节点已在 visited 中，直接返回对应克隆节点（处理环）。
            否则创建克隆节点，加入 visited，递归克隆所有邻居。

        方法2 BFS（迭代）：
            用队列按层遍历，每遇到未克隆的邻居就创建克隆并入队。

    复杂度:
        Time O(V + E)，Space O(V)  [V 节点数, E 边数]
"""

from typing import Optional, List
from collections import deque


# ──────────────────────────────────────────────
# 节点定义
# ──────────────────────────────────────────────

class Node:
    def __init__(self, val: int = 0, neighbors: List['Node'] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


# ──────────────────────────────────────────────
# 辅助：从邻接表构建图 / 图转邻接表（用于测试）
# ──────────────────────────────────────────────

def build_graph(adj_list: List[List[int]]) -> Optional[Node]:
    """
    从邻接表构建图，返回节点1的引用。
    adj_list[i] 表示值为 i+1 的节点的邻居列表（值从1开始）。
    """
    if not adj_list:
        return None
    n = len(adj_list)
    nodes = [Node(i + 1) for i in range(n)]
    for i, neighbors in enumerate(adj_list):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
    return nodes[0]


def graph_to_adj_list(node: Optional[Node]) -> List[List[int]]:
    """
    将图转换为邻接表，按节点值排序后输出。
    """
    if node is None:
        return []
    visited = {}
    queue = deque([node])
    visited[node.val] = node

    while queue:
        cur = queue.popleft()
        for neighbor in cur.neighbors:
            if neighbor.val not in visited:
                visited[neighbor.val] = neighbor
                queue.append(neighbor)

    result = []
    for val in sorted(visited.keys()):
        result.append(sorted([n.val for n in visited[val].neighbors]))
    return result


# ──────────────────────────────────────────────
# 方法1：DFS 递归 + 哈希表 ★
# ──────────────────────────────────────────────

def clone_graph_dfs(node: Optional[Node]) -> Optional[Node]:
    """
    DFS 深拷贝图。
    visited 字典将原节点映射到对应的克隆节点，防止重复克隆和无限循环。
    """
    if node is None:
        return None

    visited = {}  # {原节点: 克隆节点}

    def dfs(original: Node) -> Node:
        if original in visited:
            return visited[original]
        clone = Node(original.val)
        visited[original] = clone
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))
        return clone

    return dfs(node)


# ──────────────────────────────────────────────
# 方法2：BFS 迭代 + 哈希表
# ──────────────────────────────────────────────

def clone_graph(node: Optional[Node]) -> Optional[Node]:
    """
    BFS 深拷贝图。
    先为根节点创建克隆，然后 BFS 遍历所有邻居，
    每遇到未克隆的邻居则创建克隆并入队。
    """
    if node is None:
        return None

    visited = {node: Node(node.val)}  # {原节点: 克隆节点}
    queue = deque([node])

    while queue:
        cur = queue.popleft()
        for neighbor in cur.neighbors:
            if neighbor not in visited:
                visited[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            # 将克隆的邻居加入当前节点的克隆邻居列表
            visited[cur].neighbors.append(visited[neighbor])

    return visited[node]


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def is_deep_copy(original: Optional[Node], clone: Optional[Node]) -> bool:
    """验证克隆是深拷贝：结构相同，但是不同的对象引用。"""
    if original is None and clone is None:
        return True
    if original is None or clone is None:
        return False
    # BFS 同时遍历两个图
    visited_orig = {}
    queue = deque([(original, clone)])
    while queue:
        orig, cln = queue.popleft()
        if orig.val in visited_orig:
            continue
        if orig is cln:  # 必须是不同对象
            return False
        if orig.val != cln.val:
            return False
        if len(orig.neighbors) != len(cln.neighbors):
            return False
        visited_orig[orig.val] = cln
        orig_neighbors_vals = sorted(n.val for n in orig.neighbors)
        cln_neighbors_vals = sorted(n.val for n in cln.neighbors)
        if orig_neighbors_vals != cln_neighbors_vals:
            return False
        for on, cn in zip(
            sorted(orig.neighbors, key=lambda x: x.val),
            sorted(cln.neighbors, key=lambda x: x.val)
        ):
            queue.append((on, cn))
    return True


def test():
    # 用例1: [[2,4],[1,3],[2,4],[1,3]] (4节点环形图)
    adj1 = [[2, 4], [1, 3], [2, 4], [1, 3]]
    g1 = build_graph(adj1)
    clone_dfs = clone_graph_dfs(g1)
    clone_bfs = clone_graph(g1)

    assert graph_to_adj_list(clone_dfs) == [[2, 4], [1, 3], [2, 4], [1, 3]]
    assert graph_to_adj_list(clone_bfs) == [[2, 4], [1, 3], [2, 4], [1, 3]]
    assert is_deep_copy(g1, clone_dfs)
    assert is_deep_copy(g1, clone_bfs)

    # 用例2: 空图 -> None
    assert clone_graph_dfs(None) is None
    assert clone_graph(None) is None

    # 用例3: 单节点无边 [[]]
    g3 = build_graph([[]])
    clone3_dfs = clone_graph_dfs(g3)
    clone3_bfs = clone_graph(g3)
    assert clone3_dfs is not g3
    assert clone3_dfs.val == 1
    assert clone3_dfs.neighbors == []
    assert clone3_bfs is not g3
    assert clone3_bfs.val == 1

    # 用例4: 两节点互相连接 [[2],[1]]
    g4 = build_graph([[2], [1]])
    clone4_dfs = clone_graph_dfs(g4)
    clone4_bfs = clone_graph(g4)
    assert graph_to_adj_list(clone4_dfs) == [[2], [1]]
    assert graph_to_adj_list(clone4_bfs) == [[2], [1]]

    print("All tests passed!")


if __name__ == "__main__":
    test()
