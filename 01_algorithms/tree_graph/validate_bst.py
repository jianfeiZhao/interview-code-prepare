"""
题目：验证二叉搜索树
难度：Medium | 高频出现：字节/阿里
标签：DFS、中序遍历、树
LeetCode：#98

题目描述
---------
给定一棵二叉树的根节点 root，判断其是否是一棵有效的二叉搜索树（BST）。
有效 BST 的定义：左子树所有节点值严格小于根节点值，右子树所有节点值严格大于根节点值，
且左右子树本身也分别是有效 BST。返回布尔值表示是否合法。

示例
------
输入: root = [2, 1, 3]
输出: true

输入: root = [5, 1, 4, null, null, 3, 6]
输出: false（根节点 5 的右子节点为 4，违反 BST 性质）

约束
------
- 树中节点数量在 [1, 10^4] 范围内
- -2^31 <= Node.val <= 2^31 - 1

TL;DR（30秒速览）
- 思路：DFS 传入合法范围 (min_val, max_val)，每个节点都在范围内才合法
- 时间：O(n)  空间：O(h)
- 陷阱：不能只比较左右子节点，整个左子树必须 < root.val

详细解析
---------
方法1 - 范围法（推荐）：
  dfs(node, min_val, max_val)
  根节点初始范围(-∞, +∞)，往左子树传 max_val=node.val，往右传 min_val=node.val

方法2 - 中序遍历：
  BST 的中序遍历是严格递增序列
  遍历时记录上一个值 prev，若 cur <= prev 则非法
"""

from typing import Optional
import math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    def dfs(node, min_val, max_val):
        if not node:
            return True
        if not (min_val < node.val < max_val):
            return False
        return dfs(node.left, min_val, node.val) and dfs(node.right, node.val, max_val)
    return dfs(root, -math.inf, math.inf)


def is_valid_bst_inorder(root: Optional[TreeNode]) -> bool:
    """中序遍历法：BST 中序是严格递增的"""
    prev = -math.inf
    def inorder(node):
        nonlocal prev
        if not node:
            return True
        if not inorder(node.left):
            return False
        if node.val <= prev:
            return False
        prev = node.val
        return inorder(node.right)
    return inorder(root)


if __name__ == "__main__":
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(root) == True

    root = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(root) == False
    assert is_valid_bst_inorder(root) == False
    print("All tests passed.")
