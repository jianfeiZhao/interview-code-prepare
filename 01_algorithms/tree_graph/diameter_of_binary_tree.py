"""
LeetCode #543 - Diameter of Binary Tree
难度: Easy
高频公司: 字节跳动 / 腾讯 / 阿里巴巴  ★ 高频

题目描述:
给定一棵二叉树，你需要计算它的直径长度。
一棵二叉树的直径长度是任意两节点路径长度中的最大值。
这条路径可能穿过也可能不穿过根节点。
路径长度 = 经过的边数（不是节点数）。

示例:
    输入:
         1
        / \
       2   3
      / \
     4   5
    输出: 3
    解释: 路径 [4,2,1,3] 或 [5,2,1,3]，长度为 3

约束条件:
    - 树中节点数目在 [1, 10^4] 内
    - -100 <= Node.val <= 100

TL;DR:
    核心思路：
        直径 = 左子树深度 + 右子树深度（以某节点为转折点）。
        对每个节点计算「该节点的左子树最大深度 + 右子树最大深度」，
        取全局最大值。
        这一过程可以在后序 DFS 计算深度时顺带完成，
        函数返回当前节点的最大深度（max(left, right) + 1），
        同时更新全局最大直径。

        关键变量：
        - depth(node) = 从 node 出发向下的最长路径边数
        - diameter = max(depth(node.left) + depth(node.right)) 对所有节点

    复杂度:
        Time O(n)，Space O(h)

    变体（高频追问）：
        - 二叉树中最长路径（节点值之和最大）-> 路径可为负，需要细心处理
        - 题 #124 Binary Tree Maximum Path Sum（节点值求和版直径）
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
# 方法1：后序 DFS，全局变量记录最大直径 ★
# ──────────────────────────────────────────────

def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    后序 DFS：在计算每个节点高度时，顺带更新全局最大直径。
    depth(node) 定义为从该节点出发的最长路径包含的边数。
    """
    max_diameter = [0]  # 用列表包装，方便内层函数修改

    def depth(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        # 以当前节点为转折点的直径
        max_diameter[0] = max(max_diameter[0], left_depth + right_depth)
        return max(left_depth, right_depth) + 1

    depth(root)
    return max_diameter[0]


# ──────────────────────────────────────────────
# 扩展：#124 Binary Tree Maximum Path Sum（节点值求和版）
# ──────────────────────────────────────────────

def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    LeetCode #124 - Binary Tree Maximum Path Sum
    找出节点值之和最大的路径（路径可以从任意节点开始/结束）。

    关键点：
        - gain(node) 返回以 node 为起点向下延伸的最大「单侧」路径和
        - 若某侧为负，则不选该侧（取 max(gain, 0)）
        - 以 node 为转折点的路径和 = node.val + left_gain + right_gain
    """
    max_sum = [float('-inf')]

    def gain(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_gain = max(gain(node.left), 0)   # 负贡献不选
        right_gain = max(gain(node.right), 0)
        # 以当前节点为转折点的路径和
        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)
        # 向上只能选一侧
        return node.val + max(left_gain, right_gain)

    gain(root)
    return max_sum[0]


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # ── 直径 ──
    # 用例1: [1,2,3,4,5] -> 3 (路径 4-2-1-3 或 5-2-1-3)
    root1 = build_tree([1, 2, 3, 4, 5])
    assert diameter_of_binary_tree(root1) == 3

    # 用例2: [1,2] -> 1
    root2 = build_tree([1, 2])
    assert diameter_of_binary_tree(root2) == 1

    # 用例3: 单节点 -> 0
    root3 = build_tree([1])
    assert diameter_of_binary_tree(root3) == 0

    # 用例4: [1,2,3,4,5,6,7] -> 4 (例如 4-2-1-3-7)
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert diameter_of_binary_tree(root4) == 4

    # 用例5: 左倾树 [1,2,null,3,null,4] -> 3
    root5 = build_tree([1, 2, None, 3, None, 4])
    assert diameter_of_binary_tree(root5) == 3

    # ── 最大路径和 ──
    # 用例6: [1,2,3] -> 6 (2+1+3)
    root6 = build_tree([1, 2, 3])
    assert max_path_sum(root6) == 6

    # 用例7: [-3] -> -3 (单节点，无法不选)
    root7 = build_tree([-3])
    assert max_path_sum(root7) == -3

    # 用例8: [-10,9,20,null,null,15,7] -> 42 (15+20+7)
    root8 = build_tree([-10, 9, 20, None, None, 15, 7])
    assert max_path_sum(root8) == 42

    print("All tests passed!")


if __name__ == "__main__":
    test()
