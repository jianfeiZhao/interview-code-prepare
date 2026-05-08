"""
题目：将有序数组转换为二叉搜索树
难度：Easy | 高频出现：字节/阿里
标签：BST、分治、递归
LeetCode：#108

题目描述
---------
给定一个升序排列的整数数组 nums，将其转换为一棵高度平衡的二叉搜索树（BST）。
高度平衡指任意节点的左右子树高度差不超过 1。需要返回构建好的 BST 的根节点。
由于中点选取方式不同，答案可能不唯一，任意合法结果均可通过。

示例
------
输入: nums = [-10, -3, 0, 5, 9]
输出: [0, -3, 9, -10, null, 5]（或其他合法的高度平衡 BST）

输入: nums = [1, 3]
输出: [3, 1] 或 [1, null, 3]

约束
------
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums 严格递增排列

TL;DR（30秒速览）
- 核心思路：每次取数组中点作根节点，左半段建左子树，右半段建右子树（分治）
- 时间 O(n)，空间 O(log n)（递归栈）
- 关键陷阱：中点选左中或右中均可，题目要求"高度平衡"即左右子树高度差≤1

详细解析
---------
分治取中点：
  - mid = (lo + hi) // 2
  - nums[mid] 作根，递归处理 [lo, mid-1] 和 [mid+1, hi]
  - 结果是高度平衡的 BST（叶子层最多相差1层）
"""

from typing import List, Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sortedArrayToBST(nums: List[int]) -> Optional[TreeNode]:
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        root = TreeNode(nums[mid])
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(nums) - 1)


def is_balanced(root: Optional[TreeNode]) -> bool:
    """验证是否高度平衡"""
    def height(node):
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1:
            return -1
        return max(l, r) + 1
    return height(root) != -1


def is_bst(root: Optional[TreeNode], lo=float('-inf'), hi=float('inf')) -> bool:
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_bst(root.left, lo, root.val) and is_bst(root.right, root.val, hi)


def inorder(root):
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res


if __name__ == "__main__":
    nums1 = [-10, -3, 0, 5, 9]
    root1 = sortedArrayToBST(nums1)
    assert inorder(root1) == nums1
    assert is_bst(root1)
    assert is_balanced(root1)

    nums2 = [1, 3]
    root2 = sortedArrayToBST(nums2)
    assert inorder(root2) == nums2
    assert is_bst(root2)
    assert is_balanced(root2)

    root3 = sortedArrayToBST([0])
    assert root3.val == 0

    print("All tests passed.")
