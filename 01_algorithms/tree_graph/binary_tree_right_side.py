"""
LeetCode #199 - Binary Tree Right Side View
难度: Medium
高频公司: 字节跳动 / 美团

题目描述:
给定一个二叉树的根节点 root，想象自己站在它的右侧，
按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

示例:
    输入: root = [1,2,3,null,5,null,4]
    输出: [1, 3, 4]

    输入: root = [1, null, 3]
    输出: [1, 3]

约束条件:
    - 树中节点数目在 [0, 100] 内
    - -100 <= Node.val <= 100

TL;DR:
    核心思路：
        方法1 BFS（层序遍历）：对每一层，只记录最后一个节点的值。
              逐层用队列遍历，每层结束时取最右节点。

        方法2 DFS（右优先前序）：先访问右子树，再访问左子树。
              用 depth 记录当前深度，当 depth == len(result) 时，
              说明该节点是当前深度第一次（最右）被访问，加入结果。

    复杂度:
        Time O(n)，Space O(n) BFS / O(h) DFS
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
# 方法1：BFS 层序遍历 ★ 直观
# ──────────────────────────────────────────────

def right_side_view_bfs(root: Optional[TreeNode]) -> List[int]:
    """
    BFS 层序遍历，每层记录最后一个节点的值。
    """
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:  # 每层最后一个节点
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result


# ──────────────────────────────────────────────
# 方法2：DFS（右优先前序遍历）
# ──────────────────────────────────────────────

def right_side_view_dfs(root: Optional[TreeNode]) -> List[int]:
    """
    DFS 右优先：先访问右子节点，再访问左子节点。
    每层第一次被访问的节点即为右视图中的可见节点。
    """
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        # 当前深度第一次被访问（从右侧开始），即最右可见节点
        if depth == len(result):
            result.append(node.val)
        dfs(node.right, depth + 1)  # 先右后左
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: [1,2,3,null,5,null,4] -> [1,3,4]
    root1 = build_tree([1, 2, 3, None, 5, None, 4])
    assert right_side_view_bfs(root1) == [1, 3, 4]
    assert right_side_view_dfs(root1) == [1, 3, 4]

    # 用例2: [1, null, 3] -> [1, 3]
    root2 = build_tree([1, None, 3])
    assert right_side_view_bfs(root2) == [1, 3]
    assert right_side_view_dfs(root2) == [1, 3]

    # 用例3: 空树 -> []
    assert right_side_view_bfs(None) == []
    assert right_side_view_dfs(None) == []

    # 用例4: 单节点 -> [1]
    root4 = build_tree([1])
    assert right_side_view_bfs(root4) == [1]
    assert right_side_view_dfs(root4) == [1]

    # 用例5: 只有左子树 [1, 2, null, 3] -> [1, 2, 3]
    root5 = build_tree([1, 2, None, 3])
    assert right_side_view_bfs(root5) == [1, 2, 3]
    assert right_side_view_dfs(root5) == [1, 2, 3]

    # 用例6: 满树 [1,2,3,4,5,6,7] -> [1,3,7]
    root6 = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert right_side_view_bfs(root6) == [1, 3, 7]
    assert right_side_view_dfs(root6) == [1, 3, 7]

    print("All tests passed!")


if __name__ == "__main__":
    test()
