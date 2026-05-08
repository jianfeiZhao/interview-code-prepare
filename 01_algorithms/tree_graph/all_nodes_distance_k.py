"""
题目：距离目标节点 K 步的所有节点
难度：Medium | 高频出现：字节/阿里
标签：二叉树、BFS、DFS、建图
LeetCode：#863


题目描述
---------
给定一个二叉树（根节点 root）、一个目标节点 target，和一个整数值 k，
返回到目标节点 target 距离为 k 的所有节点的值组成的列表（返回顺序不限）。

示例
------
输入: root=[3,5,1,6,2,0,8,null,null,7,4], target=5, k=2
输出: [7,4,1]

约束
------
- 树中节点的数量在 [1, 500] 范围内
- 0 <= Node.val <= 500，树中所有节点的值各不相同
- 目标节点 target 是树中的某个节点（已保证存在）

TL;DR（30秒速览）
- 核心思路：建立父节点映射，把树变成无向图，从 target 出发 BFS K步
- 时间 O(n)，空间 O(n)
- 关键陷阱：BFS需要visited集合防止回头；K=0时直接返回target

详细解析
---------
步骤：
  1. DFS建立每个节点的父节点映射 parent[node] = parent
  2. 从 target 出发 BFS，同时走 left/right/parent 三个方向
  3. 走满 K 步后收集所有节点的值
"""

from typing import Optional, List
from collections import deque, defaultdict


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def distanceK(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    # Step1: 建立父节点映射
    parent = {}

    def build_parent(node, par):
        if not node:
            return
        parent[node] = par
        build_parent(node.left, node)
        build_parent(node.right, node)

    build_parent(root, None)

    # Step2: BFS from target
    visited = {target}
    q = deque([target])
    dist = 0

    while q and dist < k:
        dist += 1
        for _ in range(len(q)):
            node = q.popleft()
            for neighbor in (node.left, node.right, parent[node]):
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)

    return [node.val for node in q]


def build(vals):
    if not vals:
        return None, {}
    nodes = {}
    root = TreeNode(vals[0])
    nodes[vals[0]] = root
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            nodes[vals[i]] = node.left
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            nodes[vals[i]] = node.right
            q.append(node.right)
        i += 1
    return root, nodes


if __name__ == "__main__":
    # [3,5,1,6,2,0,8,None,None,7,4], target=5, k=2 -> [7,4,1]
    root, nodes = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    result = distanceK(root, nodes[5], 2)
    assert sorted(result) == [1, 4, 7], f"Got {sorted(result)}"

    # target=5, k=0 -> [5]
    result2 = distanceK(root, nodes[5], 0)
    assert result2 == [5]

    # 单节点 k=0
    root2, nodes2 = build([1])
    assert distanceK(root2, nodes2[1], 0) == [1]

    print("All tests passed.")
