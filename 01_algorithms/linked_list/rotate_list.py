"""
题目：旋转链表
难度：Medium | 高频出现：字节/腾讯
标签：链表、双指针
LeetCode：#61 Rotate List


题目描述
---------
给你一个链表的头节点 head，旋转链表，将链表每个节点向右移动 k 个位置。

示例
------
输入: head = [1,2,3,4,5], k = 2
输出: [4,5,1,2,3]

输入: head = [0,1,2], k = 4
输出: [2,0,1]

约束
------
- 链表中节点的数目在范围 [0, 500] 内
- -100 <= Node.val <= 100
- 0 <= k <= 2 * 10^9

TL;DR（30秒速览）
- 核心思路：先成环（尾接头），计算新断点位置（n - k%n - 1），从断点断开
- 时间 O(n)，空间 O(1)
- 关键陷阱：k 可能大于链表长度，需对 n 取模；k%n==0 时直接返回原链表

详细解析
---------
方法：成环再断开
  1. 遍历得链表长度 n，tail 指向末尾节点
  2. tail.next = head（成环）
  3. 实际右移步数 k = k % n（k>=n 时等价于 k%n）
  4. 新尾节点在正数第 n-k 个位置（0-indexed: n-k-1）
     移动 n-k-1 步后的节点是新尾，其 next 是新头
  5. new_head = new_tail.next，new_tail.next = None（断环）

可视化（[1->2->3->4->5], k=2）：
  n=5, k%5=2, 新尾在 index 5-2-1=2（节点3），新头是节点4
  结果：4->5->1->2->3

方法二：快慢指针
  right 先走 k 步，然后 left/right 同步前进直到 right.next 为 None
  此时 right 指向新尾，left.next 是新头
  优点：更直观，适合理解；缺点：需额外处理 k%n
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    方法一：成环再断开，O(n) 时间，O(1) 空间。
    """
    if not head or not head.next or k == 0:
        return head

    # Step 1: 计算链表长度，找到尾节点
    tail = head
    n = 1
    while tail.next:
        tail = tail.next
        n += 1

    # Step 2: 处理 k >= n 的情况
    k = k % n
    if k == 0:
        return head

    # Step 3: 成环
    tail.next = head

    # Step 4: 找新尾节点（走 n-k-1 步）
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next

    # Step 5: 断环，返回新头
    new_head = new_tail.next
    new_tail.next = None

    return new_head


def rotate_right_two_ptr(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    方法二：快慢指针，O(n) 时间，O(1) 空间。
    right 先走 k%n 步，然后 left/right 同步直到 right.next 为 None。
    """
    if not head or not head.next or k == 0:
        return head

    # 先算长度以得到 k%n
    n = 0
    curr = head
    while curr:
        n += 1
        curr = curr.next

    k = k % n
    if k == 0:
        return head

    # right 先走 k 步
    left = right = head
    for _ in range(k):
        right = right.next

    # 同步前进，直到 right.next 为 None（right 指向新尾）
    while right.next:
        left = left.next
        right = right.next

    # left.next 是新头，right 是新尾
    new_head = left.next
    left.next = None
    right.next = head

    return new_head


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
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([0, 1, 2], 4, [2, 0, 1]),    # k > n
        ([1, 2], 1, [2, 1]),
        ([1], 0, [1]),
        ([1, 2, 3], 3, [1, 2, 3]),    # k == n，不变
        ([1, 2, 3], 0, [1, 2, 3]),    # k == 0
    ]

    for vals, k, expected in test_cases:
        r1 = linked_to_list(rotate_right(list_to_linked(vals), k))
        r2 = linked_to_list(rotate_right_two_ptr(list_to_linked(vals), k))
        assert r1 == expected, f"method1: {vals}, k={k} -> {r1}, expected {expected}"
        assert r2 == expected, f"method2: {vals}, k={k} -> {r2}, expected {expected}"

    print("All tests passed.")
