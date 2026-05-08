"""
题目：平衡二叉树
难度：Easy | 高频出现：字节/阿里
标签：二叉树、DFS、后序遍历
LeetCode：#110


题目描述
---------
给定一个二叉树，判断它是否是高度平衡的二叉树。
高度平衡的二叉树定义：一个二叉树每个节点的左右两个子树的高度差的绝对值不超过 1。

示例
------
输入: root = [3,9,20,null,null,15,7]
输出: True

输入: root = [1,2,2,3,3,null,null,4,4]
输出: False

约束
------
- 树中的节点数在范围 [0, 5000] 内
- -10^4 <= Node.val <= 10^4

TL;DR（30秒速览）
- 核心思路：后序DFS，返回高度；若子树不平衡则向上传递 -1 标记，提前终止
- 时间 O(n)，空间 O(H)
- 关键陷阱：暴力法对每节点分别算高度是 O(n^2)，面试应给出 O(n) 解法

详细解析
---------
后序DFS（一次遍历）：
  - dfs(node) 返回以 node 为根的子树高度
  - 若左或右子树返回 -1，说明已不平衡，直接返回 -1
  - 若 abs(left_h - right_h) > 1，返回 -1
  - 否则返回 max(left_h, right_h) + 1
  - 最终 dfs(root) != -1 即为平衡
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isBalanced(root: Optional[TreeNode]) -> bool:
    def dfs(node) -> int:
        """返回高度，-1表示不平衡"""
        if not node:
            return 0
        left_h = dfs(node.left)
        if left_h == -1:
            return -1
        right_h = dfs(node.right)
        if right_h == -1:
            return -1
        if abs(left_h - right_h) > 1:
            return -1
        return max(left_h, right_h) + 1

    return dfs(root) != -1


def build(vals):
    from collections import deque
    if not vals:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    # 平衡：[3,9,20,None,None,15,7]
    assert isBalanced(build([3, 9, 20, None, None, 15, 7])) is True

    # 不平衡：[1,2,2,3,3,None,None,4,4]
    assert isBalanced(build([1, 2, 2, 3, 3, None, None, 4, 4])) is False

    # 空树
    assert isBalanced(None) is True

    # 单节点
    assert isBalanced(build([1])) is True

    # 右偏链状
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.right = TreeNode(3)
    assert isBalanced(root) is False

    print("All tests passed.")
