"""
LeetCode #112 - Path Sum  /  #113 - Path Sum II
难度: Easy (#112) / Medium (#113)
高频公司: 字节跳动 / 阿里巴巴

题目描述:
    #112 路径总和 I：
        给定一棵二叉树和目标和 targetSum，判断树中是否存在从根节点到叶子节点
        的路径，使得路径上所有节点的值之和等于 targetSum。
        输入: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
        输出: True  （路径: 5->4->11->2）

    #113 路径总和 II：
        返回所有满足上述条件的路径（从根到叶子），路径以节点值列表表示。
        输入: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
        输出: [[5,4,11,2], [5,8,4,5]]（第二条路径需 targetSum=22 可以是另一棵树）

约束条件:
    - 树中节点数目在 [0, 5000] 内
    - -1000 <= Node.val <= 1000
    - -1000 <= targetSum <= 1000

TL;DR:
    核心思路：
        DFS 回溯：携带当前路径和剩余目标值向下递归。
        到达叶子时检查 remaining == leaf.val。
        Path Sum I 只返回 bool，一旦找到可提前终止。
        Path Sum II 用路径列表回溯：进入节点时 path.append，
        回退时 path.pop，叶子满足时深拷贝 path 加入结果。

    复杂度:
        Time O(n)  [每个节点访问一次]
        Space O(h) [递归栈深度，最坏 O(n)]
        Path Sum II 最坏拷贝所有路径 O(n^2)
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
# #112 Path Sum I
# ──────────────────────────────────────────────

def has_path_sum(root: Optional[TreeNode], targetSum: int) -> bool:
    """
    判断是否存在根到叶子路径和等于 targetSum。
    DFS：将目标值逐层减去当前节点值，到叶子时判断是否恰好归零。
    """
    if root is None:
        return False
    # 到达叶子节点，判断当前节点值是否等于剩余目标
    if root.left is None and root.right is None:
        return root.val == targetSum
    remaining = targetSum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


def has_path_sum_iterative(root: Optional[TreeNode], targetSum: int) -> bool:
    """
    迭代版 Path Sum I（DFS 栈）。
    栈中存储 (节点, 到达该节点时的剩余目标值)。
    """
    if root is None:
        return False
    stack = [(root, targetSum)]
    while stack:
        node, remaining = stack.pop()
        remaining -= node.val
        if node.left is None and node.right is None and remaining == 0:
            return True
        if node.right:
            stack.append((node.right, remaining))
        if node.left:
            stack.append((node.left, remaining))
    return False


# ──────────────────────────────────────────────
# #113 Path Sum II
# ──────────────────────────────────────────────

def path_sum(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    """
    找出所有根到叶子路径和等于 targetSum 的路径。
    DFS 回溯：path 记录当前路径，到达满足条件的叶子时深拷贝保存。
    """
    result = []
    path = []

    def dfs(node: Optional[TreeNode], remaining: int):
        if node is None:
            return
        path.append(node.val)
        remaining -= node.val

        if node.left is None and node.right is None and remaining == 0:
            result.append(path[:])  # 深拷贝当前路径
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)

        path.pop()  # 回溯

    dfs(root, targetSum)
    return result


def path_sum_iterative(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    """
    迭代版 Path Sum II（DFS 栈）。
    栈中存储 (节点, 到达该节点时的剩余目标值, 当前路径)。
    注意：每次入栈时需要拷贝路径（否则所有节点共享同一列表）。
    """
    if root is None:
        return []
    result = []
    stack = [(root, targetSum, [])]
    while stack:
        node, remaining, path = stack.pop()
        path = path + [node.val]          # 创建新列表（不修改父节点路径）
        remaining -= node.val
        if node.left is None and node.right is None and remaining == 0:
            result.append(path)
        if node.right:
            stack.append((node.right, remaining, path))
        if node.left:
            stack.append((node.left, remaining, path))
    return result


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # ── Path Sum I ──
    # 用例1: 存在路径 5->4->11->2 = 22
    root1 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    assert has_path_sum(root1, 22) is True
    assert has_path_sum_iterative(root1, 22) is True

    # 用例2: 不存在路径和为 5
    root2 = build_tree([1, 2, 3])
    assert has_path_sum(root2, 5) is False
    assert has_path_sum_iterative(root2, 5) is False

    # 用例3: 空树
    assert has_path_sum(None, 0) is False
    assert has_path_sum_iterative(None, 0) is False

    # 用例4: 单节点等于目标值
    root4 = build_tree([1])
    assert has_path_sum(root4, 1) is True
    assert has_path_sum_iterative(root4, 1) is True

    # 用例5: 含负数 [-2, null, -3] targetSum=-5
    root5 = build_tree([-2, None, -3])
    assert has_path_sum(root5, -5) is True
    assert has_path_sum_iterative(root5, -5) is True

    # ── Path Sum II ──
    # 用例6: [5,4,8,11,null,13,4,7,2,null,null,5,1] targetSum=22
    #        路径: [5,4,11,2] 和 [5,8,4,5]
    root6 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    result6 = path_sum(root6, 22)
    assert sorted(result6) == sorted([[5, 4, 11, 2], [5, 8, 4, 5]])
    result6_iter = path_sum_iterative(root6, 22)
    assert sorted(result6_iter) == sorted([[5, 4, 11, 2], [5, 8, 4, 5]])

    # 用例7: 空树
    assert path_sum(None, 0) == []
    assert path_sum_iterative(None, 0) == []

    # 用例8: 无满足路径
    root8 = build_tree([1, 2, 3])
    assert path_sum(root8, 100) == []
    assert path_sum_iterative(root8, 100) == []

    print("All tests passed!")


if __name__ == "__main__":
    test()
