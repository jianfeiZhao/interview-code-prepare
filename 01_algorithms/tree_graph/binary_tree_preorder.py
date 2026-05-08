"""
LeetCode #144 - Binary Tree Preorder Traversal
难度: Easy
高频公司: 全系（字节/腾讯/阿里/美团）

题目描述:
给定一个二叉树的根节点 root，返回它的前序遍历结果。
前序遍历顺序：根 -> 左 -> 右

示例:
    输入: root = [1, null, 2, 3]
    输出: [1, 2, 3]

约束条件:
    - 树中节点数目在 [0, 100] 内
    - -100 <= Node.val <= 100

TL;DR:
    核心思路：
        方法1 递归：先记录根，再递归左子树，再递归右子树
        方法2 迭代（显式栈）：根入栈 -> 弹出记录 -> 先压右子再压左子
              （先压右是因为栈 LIFO，保证左子先弹出）

    复杂度:
        递归 / 迭代: Time O(n), Space O(h)  [h 为树高]
"""

from typing import Optional, List
from collections import deque


# ──────────────────────────────────────────────
# 公共工具
# ──────────────────────────────────────────────

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: List) -> Optional[TreeNode]:
    """从层序数组构建二叉树，None 表示空节点。"""
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


# ──────────────────────────────────────────────
# 方法1：递归
# ──────────────────────────────────────────────

def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """递归前序遍历。"""
    result = []

    def dfs(node):
        if node is None:
            return
        result.append(node.val)  # 先访问根
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


# ──────────────────────────────────────────────
# 方法2：迭代（显式栈）
# ──────────────────────────────────────────────

def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    迭代前序遍历。
    关键：先压右子再压左子，保证左子先被弹出处理。
    """
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        # 注意：先压右，再压左（栈弹出顺序相反）
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


# ──────────────────────────────────────────────
# 方法3：迭代（统一模板，与中序/后序写法一致）
# ──────────────────────────────────────────────

def preorder_iterative_v2(root: Optional[TreeNode]) -> List[int]:
    """
    迭代前序遍历（统一模板写法）。
    与中序遍历迭代版对比：在压栈前（即向左走时）访问节点。
    """
    result = []
    stack = []
    cur = root

    while cur or stack:
        while cur:
            result.append(cur.val)  # 向左走时先访问根
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        cur = cur.right  # 转向右子树

    return result


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: [1, null, 2, 3] -> [1, 2, 3]
    root1 = build_tree([1, None, 2, 3])
    expected1 = [1, 2, 3]
    assert preorder_recursive(root1) == expected1, "递归 用例1 失败"
    assert preorder_iterative(root1) == expected1, "迭代 用例1 失败"
    assert preorder_iterative_v2(root1) == expected1, "迭代v2 用例1 失败"

    # 用例2: 空树 -> []
    assert preorder_recursive(None) == []
    assert preorder_iterative(None) == []
    assert preorder_iterative_v2(None) == []

    # 用例3: 单节点 -> [1]
    root3 = build_tree([1])
    assert preorder_recursive(root3) == [1]
    assert preorder_iterative(root3) == [1]
    assert preorder_iterative_v2(root3) == [1]

    # 用例4: [4, 2, 6, 1, 3, 5, 7] -> [4, 2, 1, 3, 6, 5, 7]
    root4 = build_tree([4, 2, 6, 1, 3, 5, 7])
    expected4 = [4, 2, 1, 3, 6, 5, 7]
    assert preorder_recursive(root4) == expected4
    assert preorder_iterative(root4) == expected4
    assert preorder_iterative_v2(root4) == expected4

    print("All tests passed!")


if __name__ == "__main__":
    test()
