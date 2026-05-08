"""
题目：两两交换链表中的节点
难度：Medium | 高频出现：字节/腾讯
标签：链表、递归、迭代
LeetCode：#24 Swap Nodes in Pairs


题目描述
---------
给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。
必须实际交换节点，而不是仅修改节点内的值。

示例
------
输入: head = [1,2,3,4]
输出: [2,1,4,3]

输入: head = []
输出: []

约束
------
- 链表中节点的数目在范围 [0, 100] 内
- 0 <= Node.val <= 100

TL;DR（30秒速览）
- 核心思路（递归）：交换当前头两个节点，子问题交给递归处理
- 核心思路（迭代）：虚头节点，每次用 prev 重连两个节点后移动三步
- 时间 O(n)，空间 O(n)（递归栈）/ O(1)（迭代）
- 关键陷阱：迭代法需提前保存 next 指针再修改 next，避免链断失

详细解析
---------
方法一：递归
  base case：head 为空或只有一个节点，返回 head
  递归步骤：
    1. second = head.next
    2. head.next = swap_pairs(second.next)  # 子问题
    3. second.next = head                   # 交换
    4. return second                        # 新头

方法二：迭代（推荐，空间 O(1)）
  使用 dummy 虚头节点，prev 始终指向当前待交换对的前驱：
    pair 示意：prev -> node1 -> node2 -> rest
    目标：  prev -> node2 -> node1 -> rest

    步骤：
      1. node1 = prev.next
      2. node2 = prev.next.next
      3. prev.next = node2
      4. node1.next = node2.next
      5. node2.next = node1
      6. prev = node1  （node1 现在是这一对的第二个，也是下一对的 prev）

  图示：
    dummy -> 1 -> 2 -> 3 -> 4
    step1:   dummy -> 2 -> 1 -> 3 -> 4  (prev=1)
    step2:   dummy -> 2 -> 1 -> 4 -> 3  (prev=3)
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def swap_pairs_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    方法一：递归法，O(n) 时间，O(n) 空间（递归栈深度 n/2）。
    """
    # base case：0 或 1 个节点，无法交换
    if not head or not head.next:
        return head

    second = head.next
    # 递归处理第三个节点之后的部分
    head.next = swap_pairs_recursive(second.next)
    # 交换头两个节点
    second.next = head

    return second  # second 成为新头


def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    方法二：迭代法（推荐），O(n) 时间，O(1) 空间。
    """
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    while prev.next and prev.next.next:
        node1 = prev.next         # 第一个节点
        node2 = prev.next.next    # 第二个节点

        # 重连：prev -> node2 -> node1 -> rest
        prev.next = node2
        node1.next = node2.next
        node2.next = node1

        # prev 移到 node1（交换后 node1 是当前对的第二个节点，即下一对的前驱）
        prev = node1

    return dummy.next


# ─── 辅助函数 ──────────────────────────────────────────────

def list_to_linked(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4], [2, 1, 4, 3]),
        ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]),  # 奇数长度，最后一个不交换
        ([1], [1]),
        ([], []),
        ([1, 2], [2, 1]),
    ]

    for vals, expected in test_cases:
        r1 = linked_to_list(swap_pairs_recursive(list_to_linked(vals)))
        r2 = linked_to_list(swap_pairs(list_to_linked(vals)))
        assert r1 == expected, f"recursive: {vals} -> {r1}, expected {expected}"
        assert r2 == expected, f"iterative: {vals} -> {r2}, expected {expected}"

    print("All tests passed.")
