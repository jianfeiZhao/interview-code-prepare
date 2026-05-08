"""
题目：填充每个节点的下一个右侧节点指针
难度：Medium | 高频出现：字节/腾讯
标签：二叉树、BFS、链表、O(1)空间
LeetCode：#116（完美二叉树）/ #117（任意二叉树）

题目描述
---------
给定一棵完美二叉树（#116）或任意二叉树（#117），每个节点除 val/left/right 外还有一个
next 指针，初始为 null。要求填充每个节点的 next 指针，使其指向同层右侧紧邻的节点；
若该节点是当前层的最右节点，则 next 指向 null。要求原地修改并返回树的根节点。

示例
------
输入: root = [1, 2, 3, 4, 5, 6, 7]（完美二叉树）
输出: 每层节点通过 next 串联：1->null, 2->3->null, 4->5->6->7->null

输入: root = [1, 2, 3, 4, 5, null, 7]（任意二叉树）
输出: 1->null, 2->3->null, 4->5->7->null

约束
------
- 树中节点数量在 [0, 6000] 范围内（#116 完美二叉树保证所有叶子在同一层）
- -100 <= Node.val <= 100
- #116 进阶要求使用 O(1) 额外空间

TL;DR（30秒速览）
- 核心思路：BFS逐层连接（通用），或利用已建好的next指针O(1)空间遍历下一层（#116专用）
- 时间 O(n)，空间 O(1)（O(1)空间法）/ O(n)（BFS）
- 关键陷阱：#117中节点可能缺左/右孩子，需用"哨兵"dummy节点串联下一层

详细解析
---------
方法1（BFS，通用）：
  - 逐层收集节点，相邻节点连接next，最后一个节点next=None

方法2（O(1)空间，#116完美二叉树）：
  - 利用当前层已有的next，推进建立下一层的next连接
  - 每层从最左节点出发，处理两种连接：同父亲相邻 + 跨父亲相邻（通过父的next）

方法3（dummy头节点，#117任意二叉树）：
  - 用dummy.next指向每层最左节点，cur指向当前层，tail推进下一层
"""

from typing import Optional
from collections import deque


class Node:
    def __init__(self, val: int = 0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


# ===== 方法1：BFS（#116/#117 通用）=====
def connect_bfs(root: Optional[Node]) -> Optional[Node]:
    if not root:
        return root
    q = deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i < size - 1:
                node.next = q[0]
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return root


# ===== 方法2：O(1)空间（#116 完美二叉树）=====
def connect_o1(root: Optional[Node]) -> Optional[Node]:
    if not root:
        return root
    leftmost = root
    while leftmost.left:
        cur = leftmost
        while cur:
            # 同父：左->右
            cur.left.next = cur.right
            # 跨父：右->下一父的左
            if cur.next:
                cur.right.next = cur.next.left
            cur = cur.next
        leftmost = leftmost.left
    return root


# ===== 方法3：dummy节点（#117 任意二叉树）=====
def connect_117(root: Optional[Node]) -> Optional[Node]:
    cur = root
    while cur:
        dummy = Node(0)
        tail = dummy
        while cur:
            if cur.left:
                tail.next = cur.left
                tail = tail.next
            if cur.right:
                tail.next = cur.right
                tail = tail.next
            cur = cur.next
        cur = dummy.next
    return root


def build_perfect(vals):
    """构建完美二叉树"""
    if not vals:
        return None
    nodes = [Node(v) if v is not None else None for v in vals]
    for i in range(len(nodes)):
        if nodes[i]:
            li, ri = 2 * i + 1, 2 * i + 2
            if li < len(nodes):
                nodes[i].left = nodes[li]
            if ri < len(nodes):
                nodes[i].right = nodes[ri]
    return nodes[0]


def collect_nexts(root):
    """收集每层next链"""
    result = []
    cur = root
    while cur:
        row, node = [], cur
        while node:
            row.append(node.val)
            node = node.next
        result.append(row)
        cur = cur.left
    return result


if __name__ == "__main__":
    # #116: 完美二叉树 [1,2,3,4,5,6,7]
    root = build_perfect([1, 2, 3, 4, 5, 6, 7])
    connect_o1(root)
    assert collect_nexts(root) == [[1], [2, 3], [4, 5, 6, 7]]

    root2 = build_perfect([1, 2, 3, 4, 5, 6, 7])
    connect_bfs(root2)
    assert collect_nexts(root2) == [[1], [2, 3], [4, 5, 6, 7]]

    # #117: 非完美二叉树 [1,2,3,4,5,None,7]
    root3 = build_perfect([1, 2, 3, 4, 5, None, 7])
    connect_117(root3)
    # 层序：[1], [2,3], [4,5,7]
    row0 = root3
    row1 = root3.left
    assert row1.val == 2 and row1.next.val == 3 and row1.next.next is None
    row2 = root3.left.left
    assert row2.val == 4 and row2.next.val == 5 and row2.next.next.val == 7

    print("All tests passed.")
