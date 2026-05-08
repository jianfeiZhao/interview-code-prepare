"""
LeetCode #94 - Binary Tree Inorder Traversal
难度: Easy
高频公司: 全系（字节/腾讯/阿里/美团/百度）

题目描述:
给定一个二叉树的根节点 root，返回它的中序遍历结果。
中序遍历顺序：左 -> 根 -> 右

示例:
    输入: root = [1, null, 2, 3]
    输出: [1, 3, 2]

约束条件:
    - 树中节点数目在 [0, 100] 内
    - -100 <= Node.val <= 100

TL;DR:
    核心思路：
        方法1 递归：直接按左-根-右顺序递归，代码最简洁
        方法2 迭代（显式栈）：用栈模拟系统递归调用栈，一路向左压栈，
              弹出时记录，再转向右子树，时间/空间均 O(n)
        方法3 Morris 遍历：利用叶子节点的空指针存储回溯信息，将空间压到 O(1)，
              遍历完后恢复树结构

    复杂度:
        递归 / 迭代: Time O(n), Space O(h)  [h 为树高，最坏 O(n)]
        Morris:      Time O(n), Space O(1)
"""

from typing import Optional, List
from collections import deque


# ──────────────────────────────────────────────
# 公共工具：TreeNode 定义 + 辅助构建函数
# ──────────────────────────────────────────────

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


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

def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """递归中序遍历，代码最简洁。"""
    result = []

    def dfs(node):
        if node is None:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


# ──────────────────────────────────────────────
# 方法2：迭代（显式栈）
# ──────────────────────────────────────────────

def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    迭代中序遍历。
    关键思路：
        1. 当前节点不为空 -> 压栈，继续向左走
        2. 当前节点为空   -> 从栈顶弹出，记录值，转向右子树
    """
    result = []
    stack = []
    cur = root

    while cur or stack:
        # 一路向左，全部压栈
        while cur:
            stack.append(cur)
            cur = cur.left
        # 弹出栈顶，访问
        cur = stack.pop()
        result.append(cur.val)
        # 转向右子树
        cur = cur.right

    return result


# ──────────────────────────────────────────────
# 方法3：Morris 遍历（O(1) 空间）
# ──────────────────────────────────────────────

def inorder_morris(root: Optional[TreeNode]) -> List[int]:
    """
    Morris 中序遍历，空间 O(1)。
    核心思路：
        对每个节点 cur，找其中序前驱（左子树的最右节点 predecessor）。
        - 若 predecessor.right 为 None，说明首次到达：
          建立 predecessor.right = cur 的线索，cur 向左走
        - 若 predecessor.right 为 cur，说明左子树已访问完：
          恢复 predecessor.right = None，访问 cur，cur 向右走
        若 cur 无左子树，直接访问后向右走。
    """
    result = []
    cur = root

    while cur:
        if cur.left is None:
            # 无左子树，直接访问，向右走
            result.append(cur.val)
            cur = cur.right
        else:
            # 找中序前驱（左子树最右节点）
            predecessor = cur.left
            while predecessor.right and predecessor.right is not cur:
                predecessor = predecessor.right

            if predecessor.right is None:
                # 首次到达：建立线索，向左走
                predecessor.right = cur
                cur = cur.left
            else:
                # 线索已建立，左子树遍历完毕：恢复，访问 cur，向右走
                predecessor.right = None
                result.append(cur.val)
                cur = cur.right

    return result


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: [1, null, 2, 3]  ->  [1, 3, 2]
    root1 = build_tree([1, None, 2, 3])
    expected1 = [1, 3, 2]
    assert inorder_recursive(root1) == expected1, "递归 用例1 失败"
    assert inorder_iterative(root1) == expected1, "迭代 用例1 失败"
    assert inorder_morris(root1) == expected1, "Morris 用例1 失败"

    # 用例2: 空树 -> []
    assert inorder_recursive(None) == []
    assert inorder_iterative(None) == []
    assert inorder_morris(None) == []

    # 用例3: 单节点 [1] -> [1]
    root3 = build_tree([1])
    assert inorder_recursive(root3) == [1]
    assert inorder_iterative(root3) == [1]
    assert inorder_morris(root3) == [1]

    # 用例4: 完整树 [4, 2, 6, 1, 3, 5, 7] -> [1,2,3,4,5,6,7]
    root4 = build_tree([4, 2, 6, 1, 3, 5, 7])
    expected4 = [1, 2, 3, 4, 5, 6, 7]
    assert inorder_recursive(root4) == expected4
    assert inorder_iterative(root4) == expected4
    assert inorder_morris(root4) == expected4

    print("All tests passed!")


if __name__ == "__main__":
    test()
