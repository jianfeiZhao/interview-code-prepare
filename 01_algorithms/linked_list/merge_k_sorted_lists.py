"""
题目：合并 K 个升序链表
难度：Hard | 高频出现：字节/腾讯/阿里
标签：堆、分治、链表
LeetCode：#23

题目描述
---------
给定一个链表数组，每个链表都已按升序排列，将所有链表合并成一个升序链表并返回。
需要处理 k 个链表共 n 个节点的合并，要求时间复杂度优于朴素的逐一合并。

示例
------
输入: lists = [[1,4,5],[1,3,4],[2,6]]
输出: [1,1,2,3,4,4,5,6]

输入: lists = []
输出: []

约束
------
- k == lists.length，0 <= k <= 10⁴
- 每个链表节点数在 [0, 500] 之间，所有节点总数不超过 10⁴
- -10⁴ <= Node.val <= 10⁴

TL;DR（30秒速览）
- 思路：最小堆，每次弹出全局最小节点，将其 next 再入堆
- 时间：O(n log k)  空间：O(k)（堆大小）
- 陷阱：Python heapq 需要比较对象，给 ListNode 加 __lt__ 或改存 (val, index, node)

详细解析
---------
方法1 - 最小堆（推荐）：
  初始化：把所有链表的头节点放入堆
  每次 heappop 最小节点，接入结果链表
  若该节点有 next，heappush 进堆
  时间 O(n log k)，n 是总节点数

方法2 - 分治归并：
  两两合并（类似归并排序），递归分治
  时间 O(n log k)，空间 O(log k) 递归栈
"""

from typing import List, Optional
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __lt__(self, other):
        return self.val < other.val


def merge_k_lists_heap(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    for node in lists:
        if node:
            heapq.heappush(heap, node)
    dummy = ListNode(0)
    cur = dummy
    while heap:
        node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, node.next)
    return dummy.next


def merge_k_lists_divide(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    def merge_two(l1, l2):
        dummy = ListNode(0)
        cur = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                cur.next = l1; l1 = l1.next
            else:
                cur.next = l2; l2 = l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

    if not lists: return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i+1] if i+1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged
    return lists[0]


def arr_to_list(arr):
    dummy = ListNode(0)
    cur = dummy
    for v in arr: cur.next = ListNode(v); cur = cur.next
    return dummy.next

def list_to_arr(head):
    res = []
    while head: res.append(head.val); head = head.next
    return res


if __name__ == "__main__":
    lists = [arr_to_list([1,4,5]), arr_to_list([1,3,4]), arr_to_list([2,6])]
    assert list_to_arr(merge_k_lists_heap(lists)) == [1,1,2,3,4,4,5,6]

    lists = [arr_to_list([1,4,5]), arr_to_list([1,3,4]), arr_to_list([2,6])]
    assert list_to_arr(merge_k_lists_divide(lists)) == [1,1,2,3,4,4,5,6]
    print("All tests passed.")
