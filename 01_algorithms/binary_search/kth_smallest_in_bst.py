"""
题目: 二叉搜索树中第K小的元素
LeetCode: #230 (Medium)
高频公司: 字节跳动

题目描述:
给定一个二叉搜索树的根节点 root，和一个整数 k，请你设计一个算法查找其中第 k 小的元素
（从 1 开始计数）。

示例 1: root = [3,1,4,null,2], k = 1 -> 1
示例 2: root = [5,3,6,2,4,null,null,1], k = 3 -> 3

进阶: 如果二叉搜索树经常被修改（插入/删除操作），并且你需要频繁地查找第 k 小的值，
     你将如何优化算法？

================================================================================
TL;DR (核心思路):
  - BST 中序遍历结果为升序序列，第 k 小 = 中序遍历的第 k 个节点
  - 方法1: 递归中序遍历，收集所有节点值后取第 k-1 个
  - 方法2: 迭代中序遍历（用栈），遍历到第 k 个时立即返回，避免完整遍历
  - 进阶优化: 在每个节点记录左子树节点数，可 O(log n) 定位

时间复杂度: O(H + k)，H 为树高，最坏 O(n)
空间复杂度: O(H)，H 为栈深度
================================================================================
"""

from typing import Optional, List


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


# ===================== 方法1: 递归中序遍历 =====================

def kthSmallest_recursive(root: Optional[TreeNode], k: int) -> int:
    """
    递归中序遍历收集所有节点，返回第 k 小。
    简洁但不能提前终止。
    """
    result = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        result.append(node.val)
        inorder(node.right)

    inorder(root)
    return result[k - 1]


# ===================== 方法2: 迭代中序遍历（推荐）=====================

def kthSmallest_iterative(root: Optional[TreeNode], k: int) -> int:
    """
    迭代中序遍历，遍历到第 k 个节点时立即返回。
    适合大 BST 且 k 较小的场景，无需遍历所有节点。

    迭代中序遍历模板：
    1. 当前节点不为空，一路向左压栈
    2. 弹出栈顶（最小未访问节点），处理
    3. 转向右子树
    """
    stack = []
    curr = root
    count = 0

    while curr or stack:
        # 一路向左，将所有左节点压栈
        while curr:
            stack.append(curr)
            curr = curr.left

        # 弹出栈顶，即当前中序序列中最小的未访问节点
        curr = stack.pop()
        count += 1

        if count == k:
            return curr.val

        # 转向右子树
        curr = curr.right

    return -1  # 不应到达此处（k 有效时）


# ===================== 方法3: 递归 + 提前终止 =====================

def kthSmallest_early_stop(root: Optional[TreeNode], k: int) -> int:
    """
    递归中序遍历，但通过计数器提前终止。
    面试中展示对优化的思考。
    """
    count = [0]
    result = [None]

    def inorder(node):
        if not node or result[0] is not None:
            return
        inorder(node.left)
        count[0] += 1
        if count[0] == k:
            result[0] = node.val
            return
        inorder(node.right)

    inorder(root)
    return result[0]


# ===================== 进阶: 带节点计数的 BST =====================

class TreeNodeWithCount:
    """
    进阶方案：每个节点记录左子树节点数，
    可以在 O(log n) 时间内找第 k 小。
    适合频繁插入/删除后频繁查询第 k 小的场景。
    """
    def __init__(self, val: int = 0):
        self.val = val
        self.left = None
        self.right = None
        self.left_count = 0  # 左子树节点数

    def kthSmallest(self, k: int) -> int:
        """
        根据 left_count 做二分决策，O(log n)。
        """
        node = self
        while node:
            left_size = node.left_count
            if k == left_size + 1:
                return node.val
            elif k <= left_size:
                node = node.left
            else:
                k -= left_size + 1
                node = node.right
        return -1


# ============================================================
# 辅助：从列表构建 BST
# ============================================================

def build_bst_from_list(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """按层序（BFS顺序）从列表构建二叉树（非BST插入，直接赋值）。"""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 示例 1: [3,1,4,null,2], k=1 -> 1
    #       3
    #      / \
    #     1   4
    #      \
    #       2
    root1 = build_bst_from_list([3, 1, 4, None, 2])
    assert kthSmallest_recursive(root1, 1) == 1
    assert kthSmallest_iterative(root1, 1) == 1
    assert kthSmallest_early_stop(root1, 1) == 1

    # 示例 2: [5,3,6,2,4,null,null,1], k=3 -> 3
    #         5
    #        / \
    #       3   6
    #      / \
    #     2   4
    #    /
    #   1
    root2 = build_bst_from_list([5, 3, 6, 2, 4, None, None, 1])
    assert kthSmallest_recursive(root2, 3) == 3
    assert kthSmallest_iterative(root2, 3) == 3
    assert kthSmallest_early_stop(root2, 3) == 3

    # 单节点
    root3 = TreeNode(1)
    assert kthSmallest_iterative(root3, 1) == 1

    # 手工构建有序 BST: 1,2,3,4,5
    #     3
    #    / \
    #   2   4
    #  /     \
    # 1       5
    root4 = TreeNode(3)
    root4.left = TreeNode(2)
    root4.right = TreeNode(4)
    root4.left.left = TreeNode(1)
    root4.right.right = TreeNode(5)
    for k_val, expected in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]:
        assert kthSmallest_iterative(root4, k_val) == expected, f"k={k_val}"
        assert kthSmallest_recursive(root4, k_val) == expected, f"k={k_val}"

    print("所有测试通过!")

    print(f"\n[3,1,4,null,2], k=1: {kthSmallest_iterative(root1, 1)}")  # 1
    print(f"[5,3,6,2,4,null,null,1], k=3: {kthSmallest_iterative(root2, 3)}")  # 3
