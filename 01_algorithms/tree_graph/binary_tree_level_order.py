"""
题目：二叉树层序遍历
难度：Medium | 高频出现：字节/阿里/腾讯
标签：BFS、队列、树
LeetCode：#102

题目描述
---------
给定一棵二叉树的根节点 root，返回其节点值的层序遍历结果。即按从左到右的顺序，
逐层遍历所有节点，每一层的节点值放入一个列表，最终返回由各层列表构成的二维列表。

示例
------
输入: root = [3, 9, 20, null, null, 15, 7]
输出: [[3], [9, 20], [15, 7]]

输入: root = []
输出: []

约束
------
- 树中节点数量在 [0, 2000] 范围内
- -1000 <= Node.val <= 1000

TL;DR（30秒速览）
- 思路：BFS，用队列按层处理；每层开始时记录当前队列长度 size，循环 size 次
- 时间：O(n)  空间：O(n)（队列最多存一层节点）
- 陷阱：用 len(queue) 快照控制每层边界，否则会跨层

详细解析
---------
核心：deque 队列，初始放入根节点
每轮循环处理一整层：
  1. size = len(queue)（当层节点数）
  2. 循环 size 次，弹出节点，收集值，把左右子节点入队
  3. 当层收集完后 append 到结果

变种题：
  - 从底部开始的层序遍历 (LeetCode #107) → 结果 reverse
  - 锯齿形层序遍历 (LeetCode #103) → 偶数层 reverse
  - 每层最大值 (LeetCode #515)
"""

from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result


def build_tree(values):
    """按层序列表构建二叉树，None 表示空节点"""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    root = build_tree([3, 9, 20, None, None, 15, 7])
    assert level_order(root) == [[3], [9, 20], [15, 7]]

    root = build_tree([1])
    assert level_order(root) == [[1]]

    assert level_order(None) == []
    print("All tests passed.")
