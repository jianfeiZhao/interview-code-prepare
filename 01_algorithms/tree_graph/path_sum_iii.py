"""
题目：路径总和 III
难度：Medium | 高频出现：字节/腾讯/阿里
标签：二叉树、前缀和、哈希表、DFS
LeetCode：#437


题目描述
---------
给定一个二叉树的根节点 root，和一个整数 targetSum，求该二叉树里节点值之和等于 targetSum
的路径的数目。路径不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的
（只能从父节点到子节点）。

示例
------
输入: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出: 3  （路径 [5,3], [5,2,1], [-3,11] 各一条）

约束
------
- 二叉树的节点数目在范围 [0, 1000] 内
- -10^9 <= Node.val <= 10^9
- -1000 <= targetSum <= 1000

TL;DR（30秒速览）
- 核心思路：前缀和 + 哈希表，O(n) 解决"路径和等于目标值"计数问题
- 时间 O(n)，空间 O(n)
- 关键陷阱：回溯时要撤销哈希表中的前缀和，否则影响其他分支；路径只能向下

详细解析
---------
前缀和思路：
  - prefix[i] 表示根到节点i的路径和
  - 若存在祖先节点j使得 prefix[i] - prefix[j] == target，则存在一条路径
  - 维护哈希表 cnt[prefix_sum] = 出现次数
  - DFS进入时 cnt[cur_prefix] += 1，退出时 cnt[cur_prefix] -= 1（回溯）
  - 初始化 cnt[0] = 1（空路径，处理从根开始的路径）

暴力方法（O(n^2)）：对每个节点做DFS搜索，不推荐面试使用
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ===== 方法1：前缀和 + 哈希表 O(n) =====
def pathSum(root: Optional[TreeNode], targetSum: int) -> int:
    from collections import defaultdict
    cnt = defaultdict(int)
    cnt[0] = 1
    res = [0]

    def dfs(node, prefix):
        if not node:
            return
        prefix += node.val
        res[0] += cnt[prefix - targetSum]
        cnt[prefix] += 1
        dfs(node.left, prefix)
        dfs(node.right, prefix)
        cnt[prefix] -= 1  # 回溯

    dfs(root, 0)
    return res[0]


# ===== 方法2：暴力双重DFS O(n^2) =====
def pathSumBrute(root: Optional[TreeNode], targetSum: int) -> int:
    def count(node, remain):
        if not node:
            return 0
        res = 1 if node.val == remain else 0
        res += count(node.left, remain - node.val)
        res += count(node.right, remain - node.val)
        return res

    if not root:
        return 0
    return count(root, targetSum) + pathSumBrute(root.left, targetSum) + pathSumBrute(root.right, targetSum)


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
    # 示例1: [10,5,-3,3,2,None,11,3,-2,None,1], targetSum=8 -> 3
    root1 = build([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    assert pathSum(root1, 8) == 3
    assert pathSumBrute(build([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8) == 3

    # 示例2: [5,4,8,11,None,13,4,7,2,None,None,5,1], targetSum=22 -> 3
    root2 = build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    assert pathSum(root2, 22) == 3

    # 边界：单节点
    assert pathSum(build([1]), 1) == 1
    assert pathSum(build([1]), 0) == 0

    print("All tests passed.")
