"""
打家劫舍 I + II + III
LeetCode #198 (Medium) + #213 (Medium) + #337 (Medium)
高频考点: 字节跳动 / 阿里巴巴 / 腾讯 (必考)

============================================================

题目描述
---------
你是一个专业的小偷，计划偷窃沿街的房屋。每间房屋有一定的现金，
但相邻两间房屋装有相互连通的防盗系统，若相邻两间被同一天闯入则触发警报。

#198（线性）：给定一个整数数组，计算不触发警报能偷到的最高金额。
#213（环形）：房屋围成环，首尾也不能同时被盗。
#337（树形）：房屋以二叉树形式排列，相邻节点不能同时被盗。

示例
------
#198 输入: nums = [2,3,2]   输出: 3
#213 输入: nums = [2,3,2]   输出: 3
#337 输入: root = [3,2,3,null,3,null,1]  输出: 7

约束
------
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

TL;DR
============================================================
I (线性):
  状态: dp[i] = 前 i 间房子能偷的最大金额
  转移: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
  空间优化: 滚动变量 prev2, prev1

II (环形):
  环形 = 不能同时选首尾
  → 拆成两个线性子问题：[0..n-2] 和 [1..n-1]，取最大值

III (二叉树):
  状态: dfs(node) → (不选node的最大值, 选node的最大值)
  转移:
    rob    = node.val + left[0] + right[0]   # 选当前，子节点不选
    no_rob = max(left) + max(right)           # 不选当前，子节点随意
============================================================
"""

from typing import Optional, List


# ─────────────────────────────────────────────
# I. 打家劫舍（线性）
# ─────────────────────────────────────────────
def rob_linear(nums: List[int]) -> int:
    """
    解题思路:
      dp[i] 表示偷前 i+1 间的最大收益。
      每间房只有两种决策：偷 or 不偷。
        - 偷：dp[i-2] + nums[i]（上一间不能偷）
        - 不偷：dp[i-1]
      初始: dp[0]=nums[0], dp[1]=max(nums[0],nums[1])

    空间优化: 只需保留前两个状态，O(1) 空间。
    时间: O(n)，空间: O(1)
    """
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, n):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1


# ─────────────────────────────────────────────
# II. 打家劫舍 II（环形数组）
# ─────────────────────────────────────────────
def rob_circular(nums: List[int]) -> int:
    """
    解题思路:
      首尾房间不能同时偷 → 分两种情况线性求解：
        1. 不偷最后一间：nums[0..n-2]
        2. 不偷第一间：nums[1..n-1]
      两者取 max 即为答案。

    时间: O(n)，空间: O(1)
    """
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums)

    def rob_range(arr: List[int]) -> int:
        prev2, prev1 = arr[0], max(arr[0], arr[1])
        for i in range(2, len(arr)):
            prev2, prev1 = prev1, max(prev1, prev2 + arr[i])
        return prev1

    return max(rob_range(nums[:-1]), rob_range(nums[1:]))


# ─────────────────────────────────────────────
# III. 打家劫舍 III（二叉树）
# ─────────────────────────────────────────────
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rob_tree(root: Optional[TreeNode]) -> int:
    """
    解题思路:
      树形 DP：后序遍历，每个节点返回二元组 (不选, 选)。
        - 选当前节点: node.val + left[0] + right[0]
        - 不选当前节点: max(left) + max(right)
      因为不选时子节点可选可不选，取各自较大值即可。

    避免重复计算：每个节点只遍历一次，O(n) 时间，O(h) 空间（树高）。
    """
    def dfs(node):
        if not node:
            return (0, 0)  # (不选, 选)
        left = dfs(node.left)
        right = dfs(node.right)
        # 选当前节点，左右子节点均不能选
        rob = node.val + left[0] + right[0]
        # 不选当前节点，左右子节点各自取最优
        no_rob = max(left) + max(right)
        return (no_rob, rob)

    return max(dfs(root))


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_house_robber():
    # I. 线性
    assert rob_linear([1, 2, 3, 1]) == 4        # 选 1,3
    assert rob_linear([2, 7, 9, 3, 1]) == 12    # 选 2,9,1
    assert rob_linear([2, 1, 1, 2]) == 4        # 选 2,2
    assert rob_linear([0]) == 0
    assert rob_linear([5]) == 5
    print("rob_linear: all passed")

    # II. 环形
    assert rob_circular([2, 3, 2]) == 3         # 不能选 2,2（首尾），只选 3
    assert rob_circular([1, 2, 3, 1]) == 4      # 选 1,3
    assert rob_circular([1, 2, 3]) == 3
    assert rob_circular([0]) == 0
    print("rob_circular: all passed")

    # III. 二叉树
    #       3
    #      / \
    #     2   3
    #      \   \
    #       3   1
    root = TreeNode(3,
                    TreeNode(2, None, TreeNode(3)),
                    TreeNode(3, None, TreeNode(1)))
    assert rob_tree(root) == 7   # 3 + 3 + 1 = 7

    #         3
    #        / \
    #       4   5
    #      / \ / \
    #     1  3 x  1
    root2 = TreeNode(3,
                     TreeNode(4, TreeNode(1), TreeNode(3)),
                     TreeNode(5, None, TreeNode(1)))
    assert rob_tree(root2) == 9  # 4 + 5 = 9（选第二层）
    print("rob_tree: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_house_robber()
