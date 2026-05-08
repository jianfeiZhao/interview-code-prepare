"""
LeetCode #114 - Flatten Binary Tree to Linked List
难度: Medium
高频公司: 字节跳动 / 腾讯

题目描述:
给定一个二叉树的根节点 root，请将它展开为一个单链表（原地修改）。
展开后链表的顺序与前序遍历顺序一致，所有节点的 left 指针置为 None，
right 指针指向链表的下一个节点。

示例:
    输入: root = [1,2,5,3,4,null,6]
    输出: [1,null,2,null,3,null,4,null,5,null,6]

约束条件:
    - 树中节点数目在 [0, 2000] 内
    - -100 <= Node.val <= 100
    - 不能使用额外空间（in-place 修改）

TL;DR:
    核心思路（三种方法）：
        方法1 递归（后序）：
            先递归展开左、右子树 -> 将已展开的左链表接到 root.right，
            再把已展开的右链表接到新 root.right 的末尾。
            关键：先处理右子树，再处理左子树（反后序）。

        方法2 寻找前驱（最优，O(1) 空间）：
            前序遍历中，左子树根的最右节点是右子树根的「前驱」。
            原地操作：找到左子树最右节点 -> 将右子树接到其 right ->
            将左子树提升为右子树 -> left 置 None -> 移动到 right 继续。

        方法3 迭代前序（使用栈，直觉最清晰）：
            前序遍历，按访问顺序用 prev 节点串起来。

    复杂度:
        方法1/3: Time O(n), Space O(h)
        方法2:   Time O(n), Space O(1)
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


def linked_list_to_vals(root: Optional[TreeNode]) -> List[int]:
    """将展平后的链表（通过 right 指针）转为值列表。"""
    result = []
    cur = root
    while cur:
        assert cur.left is None, f"节点 {cur.val} 的 left 不为 None"
        result.append(cur.val)
        cur = cur.right
    return result


# ──────────────────────────────────────────────
# 方法1：递归（反后序：右 -> 左 -> 根）
# ──────────────────────────────────────────────

def flatten_recursive(root: Optional[TreeNode]) -> None:
    """
    递归展开。
    使用 nonlocal prev，按「右->左->根」的反前序顺序访问，
    倒着将节点串起来形成正向链表。
    """
    prev = [None]  # 用列表包装，方便内层函数修改

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        dfs(node.right)
        dfs(node.left)
        node.right = prev[0]
        node.left = None
        prev[0] = node

    dfs(root)


# ──────────────────────────────────────────────
# 方法2：寻找前驱（O(1) 空间） ★ 最优
# ──────────────────────────────────────────────

def flatten(root: Optional[TreeNode]) -> None:
    """
    原地展开，O(1) 额外空间。
    每次将左子树"插入"到当前节点和右子树之间：
        1. 找到左子树最右节点（前序遍历中右子树的前驱）
        2. 将右子树接到该前驱节点的 right
        3. 将左子树移到 right，left 置 None
        4. 向右移动到下一个节点
    """
    cur = root
    while cur:
        if cur.left:
            # 找左子树最右节点
            predecessor = cur.left
            while predecessor.right:
                predecessor = predecessor.right
            # 将右子树接到前驱的 right
            predecessor.right = cur.right
            # 左子树提升为右子树
            cur.right = cur.left
            cur.left = None
        cur = cur.right


# ──────────────────────────────────────────────
# 方法3：迭代（显式栈）
# ──────────────────────────────────────────────

def flatten_iterative(root: Optional[TreeNode]) -> None:
    """
    迭代展开，用栈模拟前序遍历，prev 指针串联节点。
    """
    if root is None:
        return
    stack = [root]
    prev = None

    while stack:
        node = stack.pop()
        if prev:
            prev.right = node
            prev.left = None
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
        prev = node
    if prev:
        prev.left = None


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    expected = [1, 2, 3, 4, 5, 6]

    # 用例1: [1,2,5,3,4,null,6] -> [1,2,3,4,5,6]
    root1 = build_tree([1, 2, 5, 3, 4, None, 6])
    flatten_recursive(root1)
    assert linked_list_to_vals(root1) == expected

    root1b = build_tree([1, 2, 5, 3, 4, None, 6])
    flatten(root1b)
    assert linked_list_to_vals(root1b) == expected

    root1c = build_tree([1, 2, 5, 3, 4, None, 6])
    flatten_iterative(root1c)
    assert linked_list_to_vals(root1c) == expected

    # 用例2: 空树 -> 无操作
    flatten(None)
    flatten_recursive(None)
    flatten_iterative(None)

    # 用例3: 单节点 [1] -> [1]
    root3 = build_tree([1])
    flatten(root3)
    assert linked_list_to_vals(root3) == [1]

    # 用例4: 只有右子树 [1,null,2,null,3] -> [1,2,3]
    root4 = build_tree([1, None, 2, None, 3])
    flatten(root4)
    assert linked_list_to_vals(root4) == [1, 2, 3]

    # 用例5: 只有左子树 [1,2,null,3] -> [1,2,3]
    root5 = build_tree([1, 2, None, 3])
    flatten(root5)
    assert linked_list_to_vals(root5) == [1, 2, 3]

    print("All tests passed!")


if __name__ == "__main__":
    test()
