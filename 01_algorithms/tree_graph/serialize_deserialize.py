"""
题目：二叉树的序列化与反序列化
难度：Hard | 高频出现：字节/阿里/腾讯
标签：二叉树、BFS、DFS、设计
LeetCode：#297

题目描述
---------
设计一个算法，能将二叉树序列化为字符串，也能将该字符串反序列化还原为原始二叉树。
序列化是将数据结构转化为可存储/传输格式的过程，反序列化则是其逆过程。
没有限制序列化格式，但需保证序列化与反序列化互为逆操作，且能处理任意二叉树结构。

示例
------
输入: root = [1, 2, 3, null, null, 4, 5]
输出: 序列化后得到某字符串 s，再反序列化后得到与原树结构和值完全相同的树

输入: root = []
输出: 空树序列化后反序列化仍为 null

约束
------
- 树中节点数量在 [0, 10^4] 范围内
- -1000 <= Node.val <= 1000
- 输入的树不保证是 BST 或完美二叉树

TL;DR（30秒速览）
- 核心思路：BFS层序（空节点用"#"占位）或DFS前序（递归）均可；反序列化按相同顺序重建
- 时间 O(n)，空间 O(n)
- 关键陷阱：空节点必须序列化，否则无法唯一重建；分隔符不能与节点值冲突

详细解析
---------
方法1（BFS层序）：
  - 序列化：队列逐层遍历，空节点写"#"
  - 反序列化：按序列顺序重建，用队列记录待填充左右孩子的父节点
  - 优点：直观，适合"层序"相关题目

方法2（DFS前序）：
  - 序列化：前序(根左右)递归，空节点写"#"
  - 反序列化：用迭代器按前序顺序重建
  - 优点：代码更简洁
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ===== 方法1：BFS 层序 =====
class CodecBFS:
    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root:
            return ""
        res = []
        q = deque([root])
        while q:
            node = q.popleft()
            if node is None:
                res.append("#")
            else:
                res.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
        return ",".join(res)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        if not data:
            return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        q = deque([root])
        i = 1
        while q and i < len(vals):
            node = q.popleft()
            if vals[i] != "#":
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != "#":
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1
        return root


# ===== 方法2：DFS 前序 =====
class CodecDFS:
    def serialize(self, root: Optional[TreeNode]) -> str:
        res = []

        def dfs(node):
            if node is None:
                res.append("#")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        vals = iter(data.split(","))

        def dfs():
            v = next(vals)
            if v == "#":
                return None
            node = TreeNode(int(v))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


def build_tree(vals):
    """辅助：从列表构建树（None表示空节点）"""
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


def tree_to_list(root):
    """辅助：将树转为层序列表"""
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        node = q.popleft()
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    # 去掉末尾 None
    while res and res[-1] is None:
        res.pop()
    return res


if __name__ == "__main__":
    tree = build_tree([1, 2, 3, None, None, 4, 5])

    # BFS
    codec_bfs = CodecBFS()
    s = codec_bfs.serialize(tree)
    recovered = codec_bfs.deserialize(s)
    assert tree_to_list(recovered) == [1, 2, 3, 4, 5], f"BFS failed: {tree_to_list(recovered)}"

    # DFS
    codec_dfs = CodecDFS()
    s2 = codec_dfs.serialize(tree)
    recovered2 = codec_dfs.deserialize(s2)
    assert tree_to_list(recovered2) == [1, 2, 3, 4, 5], f"DFS failed: {tree_to_list(recovered2)}"

    # 空树
    assert codec_bfs.deserialize(codec_bfs.serialize(None)) is None
    assert codec_dfs.deserialize(codec_dfs.serialize(None)) is None

    print("All tests passed.")
