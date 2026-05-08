"""
题目：合并两个有序链表
难度：Easy | 高频出现：字节/腾讯/美团
标签：链表、递归
LeetCode：#21


题目描述
---------
将两个升序链表合并为一个新的升序链表并返回。
新链表是通过拼接给定的两个链表的所有节点组成的。

示例
------
输入: list1 = [1,2,4], list2 = [1,3,4]
输出: [1,1,2,3,4,4]

输入: list1 = [], list2 = [0]
输出: [0]

约束
------
- 两个链表的节点数目范围是 [0, 50]
- -100 <= Node.val <= 100

TL;DR（30秒速览）
- 思路：虚拟头节点 + 迭代，比较两链表头节点大小，依次接入
- 时间：O(m+n)  空间：O(1)（迭代）/ O(m+n)（递归栈）
- 陷阱：循环结束后别忘了接上剩余链表

详细解析
---------
迭代法（推荐）：
  dummy → 虚拟头节点，省去处理空头节点的特殊情况
  cur 指针遍历，比较 l1/l2 当前节点，把小的接到 cur.next，推进

递归法（代码更简洁，但递归栈占用 O(m+n) 空间）：
  base case: 任意链表为空则返回另一个
  递归: 取较小头节点，其 next = merge(剩余部分)
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next


def merge_two_lists_recursive(l1, l2):
    if not l1: return l2
    if not l2: return l1
    if l1.val <= l2.val:
        l1.next = merge_two_lists_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists_recursive(l1, l2.next)
        return l2


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
    l1 = arr_to_list([1, 2, 4])
    l2 = arr_to_list([1, 3, 4])
    assert list_to_arr(merge_two_lists(l1, l2)) == [1, 1, 2, 3, 4, 4]

    l1 = arr_to_list([])
    l2 = arr_to_list([0])
    assert list_to_arr(merge_two_lists(l1, l2)) == [0]
    print("All tests passed.")
