"""
题目：反转链表
难度：Easy | 高频出现：全系大厂必考
标签：链表、双指针
LeetCode：#206


题目描述
---------
给你单链表的头节点 head，请你反转链表，并返回反转后的链表。
进阶：能否用 O(1) 额外空间解决此题？

示例
------
输入: head = [1,2,3,4,5]
输出: [5,4,3,2,1]

输入: head = [1,2]
输出: [2,1]

约束
------
- 链表中节点的数目范围是 [0, 5000]
- -5000 <= Node.val <= 5000

TL;DR（30秒速览）
- 思路：迭代用 prev/cur 双指针，每步把 cur.next 指向 prev
- 时间：O(n)  空间：O(1)（迭代）
- 陷阱：先保存 cur.next 再修改指针，否则链表断裂

详细解析
---------
迭代（推荐）：
  prev=None, cur=head
  循环: next_node=cur.next; cur.next=prev; prev=cur; cur=next_node
  最终 prev 即新头节点

递归：
  base case: head 为空或只有一节点 → 返回 head
  递归反转 head.next 之后的部分，再将 head.next.next = head, head.next = None

进阶：
  - 反转链表前 N 个节点
  - 反转 [left, right] 区间内的节点 (LeetCode #92)
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev, cur = None, head
    while cur:
        next_node = cur.next
        cur.next = prev
        prev = cur
        cur = next_node
    return prev


def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


def list_to_arr(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def arr_to_list(arr):
    dummy = ListNode(0)
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


if __name__ == "__main__":
    assert list_to_arr(reverse_list(arr_to_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert list_to_arr(reverse_list(arr_to_list([1, 2]))) == [2, 1]
    assert list_to_arr(reverse_list(arr_to_list([]))) == []
    print("All tests passed.")
