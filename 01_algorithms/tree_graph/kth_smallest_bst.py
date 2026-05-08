"""
题目：二叉搜索树中第K小的元素
难度：Medium | 高频出现：字节/阿里/腾讯
标签：BST、中序遍历、迭代
LeetCode：#230


题目描述
---------
给定一个二叉搜索树的根节点 root，和一个整数 k，请你设计一个算法查找其中第 k 个最小元素
（从 1 开始计数）。

示例
------
输入: root = [3,1,4,null,2], k = 1
输出: 1

输入: root = [5,3,6,2,4,null,null,1], k = 3
输出: 3

约束
------
- 树中的节点数为 n，1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4
- 进阶：如果二叉搜索树经常被修改（插入/删除），如何优化？

TL;DR（30秒速览）
- 核心思路：BST中序遍历结果天然有序，第K个弹出的节点即答案
- 时间 O(H+K)（H为树高），空间 O(H)
- 关键陷阱：K从1开始；迭代中序比递归更易提前终止

详细解析
---------
方法1（迭代中序，推荐）：
  - 维护显式栈，一路压左孩子，弹出时计数，到K时返回
  - 优势：找到即停，不必遍历完整树

方法2（递归中序）：
  - 用实例变量记录计数和答案，代码稍冗余
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ===== 方法1：迭代中序（推荐）=====
def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    stack = []
    cur = root
    count = 0
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        count += 1
        if count == k:
            return cur.val
        cur = cur.right
    return -1  # 不会到达


# ===== 方法2：递归中序 =====
def kthSmallestRecursive(root: Optional[TreeNode], k: int) -> int:
    res = []

    def inorder(node):
        if not node or len(res) == k:
            return
        inorder(node.left)
        if len(res) < k:
            res.append(node.val)
        inorder(node.right)

    inorder(root)
    return res[k - 1]


def build_bst(vals):
    """辅助：按 BST 插入顺序构建"""
    def insert(root, val):
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = insert(root.left, val)
        else:
            root.right = insert(root.right, val)
        return root

    root = None
    for v in vals:
        root = insert(root, v)
    return root


if __name__ == "__main__":
    # BST: 3,1,4,None,2  ->  中序: 1,2,3,4
    from collections import deque

    def build_from_level(vals):
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

    root = build_from_level([3, 1, 4, None, 2])
    assert kthSmallest(root, 1) == 1
    assert kthSmallest(root, 3) == 3
    assert kthSmallestRecursive(root, 1) == 1
    assert kthSmallestRecursive(root, 3) == 3

    root2 = build_from_level([5, 3, 6, 2, 4, None, None, 1])
    assert kthSmallest(root2, 3) == 3

    print("All tests passed.")
