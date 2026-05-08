"""
题目：合并K个升序链表
难度：Hard | 高频出现：字节/阿里/腾讯/美团
标签：堆、分治、链表
LeetCode：#23

题目描述
---------
给定 k 个已按升序排好序的链表，将它们合并成一个升序链表并返回。
合并后的链表应由所有输入链表的节点组成，不能新建节点（复用原节点即可）。

示例
------
输入: lists = [[1,4,5],[1,3,4],[2,6]]
输出: [1,1,2,3,4,4,5,6]

输入: lists = []
输出: []

约束
------
- 0 <= k <= 10^4
- 0 <= 每条链表的节点总数 <= 500
- -10^4 <= node.val <= 10^4

TL;DR（30秒速览）
- 方法1：最小堆，每次取最小节点，O(n log k)
- 方法2：分治归并，两两合并，O(n log k)
- 时间 O(n log k)，空间 O(k) 堆空间

详细解析
---------
设 k 个链表，共 n 个节点。

方法1 最小堆：
  将k个链表头入堆，每次弹出最小值并将其下一节点入堆
  Python heapq 不支持自定义类比较，用 (val, idx, node) 元组绕开

方法2 分治：
  两两合并链表，log k 轮后完成
  每轮 O(n)，共 O(n log k)
"""

from typing import List, Optional
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists_heap(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    cur = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


def merge_k_lists_divide(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    def merge_two(l1, l2):
        dummy = ListNode()
        cur = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                cur.next, l1 = l1, l1.next
            else:
                cur.next, l2 = l2, l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

    if not lists:
        return None
    interval = 1
    while interval < len(lists):
        for i in range(0, len(lists) - interval, interval * 2):
            lists[i] = merge_two(lists[i], lists[i + interval])
        interval *= 2
    return lists[0]


def to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def build(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


if __name__ == "__main__":
    lists = [build([1, 4, 5]), build([1, 3, 4]), build([2, 6])]
    assert to_list(merge_k_lists_heap(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

    lists2 = [build([1, 4, 5]), build([1, 3, 4]), build([2, 6])]
    assert to_list(merge_k_lists_divide(lists2)) == [1, 1, 2, 3, 4, 4, 5, 6]

    assert to_list(merge_k_lists_heap([])) is None
    assert to_list(merge_k_lists_heap([None])) is None
    print("All tests passed.")
