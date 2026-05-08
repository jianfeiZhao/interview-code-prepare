"""
LeetCode #101 - Symmetric Tree
难度: Easy
高频公司: 字节跳动 / 腾讯

题目描述:
给定一个二叉树的根节点 root，检查它是否轴对称（关于中心对称）。

示例:
    输入: root = [1, 2, 2, 3, 4, 4, 3]
    输出: True

    输入: root = [1, 2, 2, null, 3, null, 3]
    输出: False

约束条件:
    - 树中节点数目在 [1, 1000] 内
    - -100 <= Node.val <= 100

TL;DR:
    核心思路：
        对称 <=> 左子树和右子树互为镜像。
        方法1 递归：定义 is_mirror(L, R)：
            - L 和 R 同时为 None -> True
            - 其中一个为 None   -> False
            - L.val != R.val    -> False
            - 否则递归比较 (L.left, R.right) 和 (L.right, R.left)
        方法2 迭代（队列）：每次从队列取出两个节点做比较，
            把 (L.left, R.right) 和 (L.right, R.left) 成对入队

    复杂度:
        Time O(n)，Space O(h) 递归 / O(n) 迭代
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

def is_symmetric_recursive(root: Optional[TreeNode]) -> bool:
    """递归判断是否对称。"""
    def is_mirror(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (left.val == right.val
                and is_mirror(left.left, right.right)
                and is_mirror(left.right, right.left))

    if root is None:
        return True
    return is_mirror(root.left, root.right)


# ──────────────────────────────────────────────
# 方法2：迭代（队列）
# ──────────────────────────────────────────────

def is_symmetric_iterative(root: Optional[TreeNode]) -> bool:
    """
    迭代判断是否对称。
    用队列每次取出一对节点进行比较，
    然后将它们的子节点按镜像顺序成对入队。
    """
    if root is None:
        return True

    queue = deque()
    queue.append(root.left)
    queue.append(root.right)

    while queue:
        left = queue.popleft()
        right = queue.popleft()

        if left is None and right is None:
            continue
        if left is None or right is None:
            return False
        if left.val != right.val:
            return False

        # 镜像入队：外侧一对 + 内侧一对
        queue.append(left.left)
        queue.append(right.right)
        queue.append(left.right)
        queue.append(right.left)

    return True


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: 对称树 [1, 2, 2, 3, 4, 4, 3] -> True
    root1 = build_tree([1, 2, 2, 3, 4, 4, 3])
    assert is_symmetric_recursive(root1) is True
    assert is_symmetric_iterative(root1) is True

    # 用例2: 非对称树 [1, 2, 2, null, 3, null, 3] -> False
    root2 = build_tree([1, 2, 2, None, 3, None, 3])
    assert is_symmetric_recursive(root2) is False
    assert is_symmetric_iterative(root2) is False

    # 用例3: 单节点 -> True
    root3 = build_tree([1])
    assert is_symmetric_recursive(root3) is True
    assert is_symmetric_iterative(root3) is True

    # 用例4: 只有左子树 [1, 2] -> False
    root4 = build_tree([1, 2])
    assert is_symmetric_recursive(root4) is False
    assert is_symmetric_iterative(root4) is False

    # 用例5: 值相同但结构不对称 [1, 2, 2, 2, None, 2] -> False
    root5 = build_tree([1, 2, 2, 2, None, 2, None])
    assert is_symmetric_recursive(root5) is False
    assert is_symmetric_iterative(root5) is False

    print("All tests passed!")


if __name__ == "__main__":
    test()
