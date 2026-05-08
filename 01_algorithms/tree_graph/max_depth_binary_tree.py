"""
题目：二叉树的最大深度
难度：Easy | 高频出现：字节/腾讯
标签：DFS、递归、树
LeetCode：#104


题目描述
---------
给定一个二叉树 root，返回其最大深度。
二叉树的最大深度是指从根节点到最远叶子节点的最长路径上的节点数。

示例
------
输入: root = [3,9,20,null,null,15,7]
输出: 3

输入: root = [1,null,2]
输出: 2

约束
------
- 树中节点的数量在 [0, 10^4] 范围内
- -100 <= Node.val <= 100

TL;DR（30秒速览）
- 思路：递归，max(左子树深度, 右子树深度) + 1
- 时间：O(n)  空间：O(h)，h为树高（最坏O(n)）

详细解析
---------
递归（自顶向下）：
  max_depth = 1 + max(max_depth(left), max_depth(right))

迭代（BFS 层序）：
  按层遍历，层数即为深度

进阶：
  - 最小深度 (LeetCode #111)：注意单子节点情况，不能直接 min
  - 平衡二叉树 (LeetCode #110)：DFS 同时返回高度+是否平衡
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def max_depth_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    depth = 0
    queue = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return depth


if __name__ == "__main__":
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_depth(root) == 3
    assert max_depth_iterative(root) == 3
    assert max_depth(None) == 0
    print("All tests passed.")
