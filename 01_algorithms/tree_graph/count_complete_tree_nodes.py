"""
LeetCode #222 - Count Complete Tree Nodes
难度: Medium
高频公司: 字节跳动

题目描述:
给你一棵完全二叉树的根节点 root，求出该树的节点个数。
完全二叉树：所有层（除最后一层）都被完全填满，最后一层的节点都靠左。

示例:
    输入: root = [1,2,3,4,5,6]
    输出: 6

约束条件:
    - 树中节点数目在 [0, 5 * 10^4] 内
    - 0 <= Node.val <= 5 * 10^4
    - 题目保证输入的树是完全二叉树

TL;DR:
    核心思路：
        方法1 暴力 O(n)：直接 DFS 遍历计数，不利用完全二叉树性质，面试不加分。

        方法2 利用完全二叉树性质 O(log^2 n)（★ 面试期望答案）：
            对于当前子树，分别计算「最左路径深度」left_depth 和
            「最右路径深度」right_depth：
            - 若 left_depth == right_depth：该子树是满二叉树，节点数 = 2^depth - 1
            - 否则：递归左右子树，节点数 = 1 + count(left) + count(right)

            每次递归层数降低一半，递归深度 O(log n)，每层需要 O(log n) 计算深度，
            总时间 O(log^2 n)。

    复杂度:
        方法1: Time O(n),       Space O(h)
        方法2: Time O(log^2 n), Space O(log n)
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
# 方法1：暴力 DFS（O(n)）
# ──────────────────────────────────────────────

def count_nodes_brute(root: Optional[TreeNode]) -> int:
    """暴力计数，不利用完全二叉树性质。"""
    if root is None:
        return 0
    return 1 + count_nodes_brute(root.left) + count_nodes_brute(root.right)


# ──────────────────────────────────────────────
# 方法2：利用完全二叉树性质（O(log^2 n)） ★
# ──────────────────────────────────────────────

def count_nodes(root: Optional[TreeNode]) -> int:
    """
    利用完全二叉树性质，O(log^2 n) 时间。
    对每棵子树判断是否为满二叉树：
    - 是满二叉树（left_depth == right_depth）-> 直接返回 2^depth - 1
    - 否则 -> 递归左右子树
    """
    if root is None:
        return 0

    # 计算左路径深度（一直向左走）
    left_depth = 0
    node = root
    while node:
        left_depth += 1
        node = node.left

    # 计算右路径深度（一直向右走）
    right_depth = 0
    node = root
    while node:
        right_depth += 1
        node = node.right

    # 满二叉树：左深度 == 右深度
    if left_depth == right_depth:
        return (1 << left_depth) - 1  # 2^depth - 1

    # 非满二叉树：递归处理
    return 1 + count_nodes(root.left) + count_nodes(root.right)


# ──────────────────────────────────────────────
# 扩展：二分查找最后一层节点位置（另一种 O(log^2 n) 思路）
# ──────────────────────────────────────────────

def count_nodes_binary_search(root: Optional[TreeNode]) -> int:
    """
    二分查找法：O(log^2 n)。
    先确定树的高度 h（节点数在 [2^(h-1), 2^h - 1] 之间）。
    在最后一层用二分查找找到最后一个节点的位置。
    """
    if root is None:
        return 0

    # 计算树高（一路向左）
    h = 0
    node = root
    while node:
        h += 1
        node = node.left

    if h == 1:
        return 1

    # 最后一层节点数范围 [1, 2^(h-1)]
    # 用二分确定最后一层最右节点的位置（1-indexed）
    lo, hi = 1, 1 << (h - 1)  # 2^(h-1)

    while lo < hi:
        mid = (lo + hi + 1) // 2
        # 检查位置 mid 的节点是否存在
        if node_exists(root, h, mid):
            lo = mid
        else:
            hi = mid - 1

    return (1 << (h - 1)) - 1 + lo  # 前 h-1 层节点数 + 最后一层节点数


def node_exists(root: Optional[TreeNode], h: int, pos: int) -> bool:
    """
    检查最后一层第 pos 个位置是否存在节点。
    使用二进制位引导路径：h-1 位中，0 表示向左，1 表示向右。
    """
    lo, hi = 1, 1 << (h - 1)
    node = root
    for _ in range(h - 1):
        mid = (lo + hi) // 2
        if pos <= mid:
            node = node.left
            hi = mid
        else:
            node = node.right
            lo = mid + 1
        if node is None:
            return False
    return node is not None


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: [1,2,3,4,5,6] -> 6
    root1 = build_tree([1, 2, 3, 4, 5, 6])
    assert count_nodes_brute(root1) == 6
    assert count_nodes(root1) == 6

    # 用例2: 空树 -> 0
    assert count_nodes_brute(None) == 0
    assert count_nodes(None) == 0

    # 用例3: 单节点 -> 1
    root3 = build_tree([1])
    assert count_nodes_brute(root3) == 1
    assert count_nodes(root3) == 1

    # 用例4: 满二叉树 [1,2,3,4,5,6,7] -> 7
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert count_nodes_brute(root4) == 7
    assert count_nodes(root4) == 7

    # 用例5: 较大完全二叉树 [1..10] -> 10
    root5 = build_tree(list(range(1, 11)))
    assert count_nodes_brute(root5) == 10
    assert count_nodes(root5) == 10

    # 用例6: 完全二叉树，最后一层只有左子节点
    root6 = build_tree([1, 2, 3, 4, 5, 6, 7, 8])
    assert count_nodes(root6) == 8

    print("All tests passed!")


if __name__ == "__main__":
    test()
