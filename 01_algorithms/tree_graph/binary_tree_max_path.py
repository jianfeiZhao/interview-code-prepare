"""
题目：二叉树中的最大路径和
难度：Hard | 高频出现：字节/阿里/腾讯/Meta
标签：二叉树、DFS、后序遍历、动态规划
LeetCode：#124


题目描述
---------
二叉树中的路径被定义为一条节点序列，序列中每对相邻节点之间都存在一条边，
同一节点在一条路径序列中至多出现一次，该路径不必经过根节点，也不必经过叶节点。
路径和是路径中各节点值的总和。给你一个二叉树的根节点 root，返回其最大路径和。

示例
------
输入: root = [1,2,3]
输出: 6  （路径 2→1→3）

输入: root = [-10,9,20,null,null,15,7]
输出: 42  （路径 15→20→7）

约束
------
- 树中节点数目范围是 [1, 3 * 10^4]
- -1000 <= Node.val <= 1000

TL;DR（30秒速览）
- 核心思路：后序DFS，每个节点返回"向上延伸的最大贡献值"，同时用左右贡献更新全局答案
- 时间 O(n)，空间 O(H)
- 关键陷阱：贡献值为负时取0（相当于不选该子树）；路径可以不过根节点

详细解析
---------
对于每个节点 node：
  - left_gain = max(dfs(node.left), 0)   # 负数不要
  - right_gain = max(dfs(node.right), 0)
  - 经过 node 的最大路径和 = node.val + left_gain + right_gain  -> 更新全局最大值
  - 向上只能选一边：return node.val + max(left_gain, right_gain)

注意：路径和可能全为负数，因此全局变量初始化为 float('-inf')
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root: Optional[TreeNode]) -> int:
    res = [float('-inf')]

    def dfs(node) -> int:
        """返回以 node 为端点向上延伸的最大路径和（贡献值）"""
        if not node:
            return 0
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        # 经过当前节点的路径（可以拐弯）
        res[0] = max(res[0], node.val + left_gain + right_gain)
        # 向父节点只能选一侧
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return res[0]


def build(vals):
    from collections import deque
    if not vals:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    # 示例1: [1,2,3] -> 6 (2->1->3)
    assert maxPathSum(build([1, 2, 3])) == 6

    # 示例2: [-10,9,20,None,None,15,7] -> 42 (15->20->7)
    assert maxPathSum(build([-10, 9, 20, None, None, 15, 7])) == 42

    # 全负数: [-3] -> -3
    assert maxPathSum(build([-3])) == -3

    # 全负数多节点: [-1,-2,-3] -> -1
    assert maxPathSum(build([-1, -2, -3])) == -1

    # 单节点正数
    assert maxPathSum(build([5])) == 5

    print("All tests passed.")
