"""
LeetCode #105 - Construct Binary Tree from Preorder and Inorder Traversal
难度: Medium
高频公司: 字节跳动 / 阿里巴巴

题目描述:
给定一棵树的前序遍历 preorder 与中序遍历 inorder，构造该二叉树并返回根节点。
注意：树中没有重复元素。

示例:
    输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    输出: [3,9,20,null,null,15,7]

约束条件:
    - 1 <= 节点个数 <= 3000
    - -3000 <= Node.val <= 3000
    - preorder 和 inorder 均无重复元素
    - inorder 均出现在 preorder 中
    - preorder 保证为正确的前序遍历序列
    - inorder 保证为正确的中序遍历序列

TL;DR:
    核心思路（递归分治）：
        1. 前序遍历首元素 preorder[0] 是当前子树的根
        2. 在中序遍历中找到根的位置 mid，
           mid 左侧是左子树中序，右侧是右子树中序
        3. 左子树节点数 left_size = mid（相对中序子数组的索引）
        4. 递归构建左子树：preorder[1 : 1+left_size]，inorder[:mid]
        5. 递归构建右子树：preorder[1+left_size:]，inorder[mid+1:]

        优化：用哈希表预存中序值->索引，将每次查找从 O(n) 降到 O(1)，
        整体时间复杂度 O(n)。

    复杂度:
        Time O(n)，Space O(n) [哈希表 + 递归栈]
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


def tree_to_list(root: Optional[TreeNode]) -> List:
    """将二叉树转回层序数组（用于断言对比）。"""
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    # 去掉末尾的 None
    while result and result[-1] is None:
        result.pop()
    return result


def get_inorder(root: Optional[TreeNode]) -> List[int]:
    """获取树的中序遍历，用于验证构造结果。"""
    if root is None:
        return []
    return get_inorder(root.left) + [root.val] + get_inorder(root.right)


def get_preorder(root: Optional[TreeNode]) -> List[int]:
    """获取树的前序遍历，用于验证构造结果。"""
    if root is None:
        return []
    return [root.val] + get_preorder(root.left) + get_preorder(root.right)


# ──────────────────────────────────────────────
# 方法1：递归（切片）——直观但有额外空间
# ──────────────────────────────────────────────

def build_tree_v1(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    递归构造，每次切片传入子数组。
    逻辑清晰，但切片会产生 O(n^2) 的额外空间。
    """
    if not preorder:
        return None

    root_val = preorder[0]
    root = TreeNode(root_val)

    mid = inorder.index(root_val)  # 找根在中序中的位置

    root.left = build_tree_v1(preorder[1: 1 + mid], inorder[:mid])
    root.right = build_tree_v1(preorder[1 + mid:], inorder[mid + 1:])

    return root


# ──────────────────────────────────────────────
# 方法2：递归（哈希表 + 索引） ★ 最优写法
# ──────────────────────────────────────────────

def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    递归构造，哈希表预存中序索引，O(n) 时间。
    使用 pre_start / pre_end 和 in_start / in_end 代替切片。
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}

    def helper(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[TreeNode]:
        if pre_start > pre_end:
            return None

        root_val = preorder[pre_start]
        root = TreeNode(root_val)

        mid = inorder_map[root_val]
        left_size = mid - in_start

        root.left = helper(pre_start + 1, pre_start + left_size,
                           in_start, mid - 1)
        root.right = helper(pre_start + left_size + 1, pre_end,
                            mid + 1, in_end)
        return root

    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)


# ──────────────────────────────────────────────
# 扩展：从中序 + 后序构造（#106）
# ──────────────────────────────────────────────

def build_tree_from_inorder_postorder(
    inorder: List[int],
    postorder: List[int]
) -> Optional[TreeNode]:
    """
    LeetCode #106：从中序和后序遍历构造二叉树。
    后序最后一个元素是根；在中序中找根的位置，分左右子树递归。
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}

    def helper(in_start: int, in_end: int, post_start: int, post_end: int) -> Optional[TreeNode]:
        if in_start > in_end:
            return None

        root_val = postorder[post_end]
        root = TreeNode(root_val)

        mid = inorder_map[root_val]
        left_size = mid - in_start

        root.left = helper(in_start, mid - 1, post_start, post_start + left_size - 1)
        root.right = helper(mid + 1, in_end, post_start + left_size, post_end - 1)
        return root

    return helper(0, len(inorder) - 1, 0, len(postorder) - 1)


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: preorder=[3,9,20,15,7] inorder=[9,3,15,20,7]
    preorder1 = [3, 9, 20, 15, 7]
    inorder1 = [9, 3, 15, 20, 7]

    root1_v1 = build_tree_v1(preorder1, inorder1)
    root1_v2 = build_tree(preorder1, inorder1)
    assert get_preorder(root1_v1) == preorder1
    assert get_inorder(root1_v1) == inorder1
    assert get_preorder(root1_v2) == preorder1
    assert get_inorder(root1_v2) == inorder1

    # 用例2: 单节点
    root2 = build_tree([1], [1])
    assert root2.val == 1
    assert root2.left is None and root2.right is None

    # 用例3: 只有左子树 preorder=[1,2] inorder=[2,1]
    root3 = build_tree([1, 2], [2, 1])
    assert root3.val == 1
    assert root3.left.val == 2
    assert root3.right is None

    # 用例4: 只有右子树 preorder=[1,2] inorder=[1,2]
    root4 = build_tree([1, 2], [1, 2])
    assert root4.val == 1
    assert root4.left is None
    assert root4.right.val == 2

    # 用例5: 中序 + 后序构造（#106）
    inorder5 = [9, 3, 15, 20, 7]
    postorder5 = [9, 15, 7, 20, 3]
    root5 = build_tree_from_inorder_postorder(inorder5, postorder5)
    assert get_inorder(root5) == inorder5
    assert get_preorder(root5) == [3, 9, 20, 15, 7]

    print("All tests passed!")


if __name__ == "__main__":
    test()
