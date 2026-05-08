"""
LeetCode #236 - Lowest Common Ancestor of a Binary Tree
难度: Medium
高频公司: 字节跳动 / 阿里巴巴 / 腾讯  ★ 必考

题目描述:
给定一个二叉树，找出两个指定节点 p 和 q 的最近公共祖先（LCA）。
LCA 定义：节点 v 是 p 和 q 的最近公共祖先，v 是 p、q 的祖先，
且 v 尽可能深（v 本身可以是其自己的祖先）。

示例:
    输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
    输出: 3
    解释: 节点 5 和节点 1 的最近公共祖先是节点 3

    输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
    输出: 5
    解释: 节点 5 是节点 4 的祖先，所以 LCA 是 5

约束条件:
    - 树中节点数目在 [2, 10^5] 内
    - -10^9 <= Node.val <= 10^9
    - p 和 q 均存在于给定树中，且各不相同

TL;DR:
    核心思路（递归后序遍历）：
        对每个节点，先递归左右子树取结果 left, right：
        1. 当前节点就是 p 或 q -> 直接返回当前节点
           （不管另一个在不在子树里，LCA 一定是当前节点或其祖先）
        2. left 和 right 都非空 -> p、q 分列两侧，当前节点即为 LCA
        3. 只有 left 非空 -> 两个节点都在左子树，LCA 在左边返回
        4. 只有 right 非空 -> 两个节点都在右子树，LCA 在右边返回
        5. 两者都为空 -> 返回 None

    复杂度:
        Time O(n)，Space O(h) [递归栈深度]

    扩展变体（面试常考）：
        - 节点可能不存在于树中 -> 需要用返回元组 (found_p, found_q, lca) 的方式
        - BST 的 LCA（#235）-> 利用 BST 性质，每次只走一侧，O(h) 时间
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


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """在树中查找值为 val 的节点，用于测试辅助。"""
    if root is None:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


# ──────────────────────────────────────────────
# 方法1：递归（后序 DFS）★ 最优写法
# ──────────────────────────────────────────────

def lowest_common_ancestor(
    root: Optional[TreeNode],
    p: TreeNode,
    q: TreeNode
) -> Optional[TreeNode]:
    """
    经典递归 LCA。
    函数语义：在以 root 为根的子树中找 p 或 q，若找到返回找到的节点或 LCA；
    否则返回 None。
    """
    # 基准情形：空节点或找到 p/q
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # p 和 q 分列两侧，当前节点就是 LCA
    if left and right:
        return root
    # 否则返回非空的那一侧
    return left if left else right


# ──────────────────────────────────────────────
# 方法2：迭代（记录父节点）
# ──────────────────────────────────────────────

def lowest_common_ancestor_iterative(
    root: Optional[TreeNode],
    p: TreeNode,
    q: TreeNode
) -> Optional[TreeNode]:
    """
    迭代法：
    1. DFS 遍历整棵树，用字典记录每个节点的父节点
    2. 从 p 向上收集祖先集合
    3. 从 q 向上逐步走，第一个在 p 祖先集合中的节点即为 LCA
    """
    parent = {root: None}
    stack = [root]

    # 找到 p 和 q 后即可停止 DFS
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # 收集 p 的所有祖先
    ancestors = set()
    cur = p
    while cur is not None:
        ancestors.add(cur)
        cur = parent[cur]

    # q 向上走，第一个出现在 ancestors 中的即为 LCA
    cur = q
    while cur not in ancestors:
        cur = parent[cur]
    return cur


# ──────────────────────────────────────────────
# 扩展：BST 的 LCA（#235，利用 BST 性质）
# ──────────────────────────────────────────────

def lca_bst(
    root: Optional[TreeNode],
    p: TreeNode,
    q: TreeNode
) -> Optional[TreeNode]:
    """
    BST 专用：利用 BST 性质，避免遍历整棵树。
    若 p、q 都小于当前节点 -> 向左走
    若 p、q 都大于当前节点 -> 向右走
    否则当前节点就是 LCA
    Time O(h), Space O(1) 迭代版
    """
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
    return None


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # ── 普通二叉树 LCA ──
    # 树: [3,5,1,6,2,0,8,null,null,7,4]
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])

    p5 = find_node(root, 5)
    p1 = find_node(root, 1)
    p4 = find_node(root, 4)
    p6 = find_node(root, 6)

    # LCA(5, 1) = 3
    assert lowest_common_ancestor(root, p5, p1).val == 3
    assert lowest_common_ancestor_iterative(root, p5, p1).val == 3

    # LCA(5, 4) = 5（p 是 q 的祖先）
    assert lowest_common_ancestor(root, p5, p4).val == 5
    assert lowest_common_ancestor_iterative(root, p5, p4).val == 5

    # LCA(6, 4) = 5
    assert lowest_common_ancestor(root, p6, p4).val == 5
    assert lowest_common_ancestor_iterative(root, p6, p4).val == 5

    # ── BST LCA ──
    # BST: [6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]
    bst_root = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    bp2 = find_node(bst_root, 2)
    bp8 = find_node(bst_root, 8)
    bp4 = find_node(bst_root, 4)

    # LCA(2, 8) = 6
    assert lca_bst(bst_root, bp2, bp8).val == 6
    # LCA(2, 4) = 2
    assert lca_bst(bst_root, bp2, bp4).val == 2

    print("All tests passed!")


if __name__ == "__main__":
    test()
