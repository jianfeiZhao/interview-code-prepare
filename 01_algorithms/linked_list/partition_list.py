"""
题目：分隔链表
难度：Medium | 高频出现：字节/腾讯
标签：链表、双指针
LeetCode：#86 Partition List

题目描述
---------
给定一个链表的头节点 head 和一个特定值 x，对链表进行分隔，使得所有小于 x 的节点都出现在大于或等于 x 的节点之前。
在保留两个分区中每个节点初始相对顺序的同时，返回重新排列后的链表头节点。

示例
------
输入: head = [1,4,3,2,5,2], x = 3
输出: [1,2,2,4,3,5]

输入: head = [2,1], x = 2
输出: [1,2]

约束
------
- 链表节点数在 [0, 200] 之间
- -100 <= Node.val <= 100
- -200 <= x <= 200

TL;DR（30秒速览）
- 核心思路：建两条虚拟链表（小于x的链 + 大于等于x的链），最后拼接
- 时间 O(n)，空间 O(1)（只用了常数个指针，未新建节点）
- 关键陷阱：拼接时大链表末尾必须置 None，否则形成环

详细解析
---------
方法：双虚头节点（Dummy Node）
  - less_dummy：收集所有 val < x 的节点
  - greater_dummy：收集所有 val >= x 的节点
  - 遍历原链表，按 val 分流节点
  - 最后：less_tail.next = greater_dummy.next
          greater_tail.next = None  ← 必须切断，防止环

为什么需要两个虚头节点？
  虚头节点让链表操作无需特判头部为空的情况，代码更简洁统一。

步骤可视化（x=3, [1->4->3->2->5->2]）：
  less:    1 -> 2 -> 2
  greater: 4 -> 3 -> 5
  result:  1 -> 2 -> 2 -> 4 -> 3 -> 5
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    """
    双虚头节点法，O(n) 时间，O(1) 空间。
    """
    less_dummy = ListNode(0)    # 小于 x 的链表虚头
    greater_dummy = ListNode(0) # 大于等于 x 的链表虚头

    less = less_dummy
    greater = greater_dummy

    curr = head
    while curr:
        if curr.val < x:
            less.next = curr
            less = less.next
        else:
            greater.next = curr
            greater = greater.next
        curr = curr.next

    # 关键：大链表末尾必须置 None，防止形成环
    greater.next = None
    # 拼接两条链表
    less.next = greater_dummy.next

    return less_dummy.next


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
    # [1,4,3,2,5,2], x=3 -> [1,2,2,4,3,5]
    head = list_to_linked([1, 4, 3, 2, 5, 2])
    result = partition(head, 3)
    assert linked_to_list(result) == [1, 2, 2, 4, 3, 5], linked_to_list(result)

    # [2,1], x=2 -> [1,2]
    head = list_to_linked([2, 1])
    result = partition(head, 2)
    assert linked_to_list(result) == [1, 2]

    # 全部小于 x
    head = list_to_linked([1, 2, 3])
    result = partition(head, 10)
    assert linked_to_list(result) == [1, 2, 3]

    # 全部大于等于 x
    head = list_to_linked([3, 4, 5])
    result = partition(head, 3)
    assert linked_to_list(result) == [3, 4, 5]

    # 空链表
    assert partition(None, 0) is None

    print("All tests passed.")
