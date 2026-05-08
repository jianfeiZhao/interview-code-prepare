"""
题目：环形链表 II
难度：Medium | 高频出现：字节/阿里/腾讯
标签：链表、双指针、Floyd判圈
LeetCode：#142 Linked List Cycle II


题目描述
---------
给定一个链表的头节点 head，返回链表开始入环的第一个节点。
如果链表无环，则返回 null。不允许修改链表。

示例
------
输入: head = [3,2,0,-4]，tail 连接到下标 1
输出: 下标 1 处的节点（值为 2）

输入: head = [1,2]，tail 连接到下标 0
输出: 下标 0 处的节点（值为 1）

约束
------
- 链表中节点的数目范围在 [0, 10^4] 内
- -10^5 <= Node.val <= 10^5

TL;DR（30秒速览）
- 核心思路：Floyd 快慢指针——先找到相遇点，再用两个慢指针找环入口
- 时间 O(n)，空间 O(1)
- 关键陷阱：无环时返回 None；相遇后将一个指针重置到 head，两者同速再走直到相遇即为入口

详细解析
---------
数学推导：
  设：链表头到环入口距离 = a
      环入口到相遇点距离 = b
      环的长度 = c

  fast 走的路程 = slow 走的路程 × 2
  => a + b + nc = 2(a + b)    (n 为 fast 多走的圈数，n>=1)
  => a = nc - b = (n-1)c + (c - b)

  当 n=1 时：a = c - b
  即：从 head 到环入口的距离 = 从相遇点沿环方向到环入口的距离

  因此：相遇后，一个指针从 head 出发，另一个从相遇点出发，
        两者每次都走一步，再次相遇的地方就是环入口。

步骤：
  1. slow/fast 从 head 出发，slow 走1步，fast 走2步
  2. 若 fast/fast.next 为 None：无环，返回 None
  3. 相遇后：ptr1 = head，ptr2 = meeting point
  4. ptr1/ptr2 同速前进，相遇点即为环入口

扩展：#141 环形链表 I（只判断有无环，返回 bool）
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Floyd 快慢指针，O(n) 时间，O(1) 空间。
    返回环入口节点，无环返回 None。
    """
    # Phase 1: 找相遇点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        # fast 或 fast.next 为 None，无环
        return None

    # Phase 2: 找环入口
    # ptr1 从 head，ptr2 从相遇点，同速前进
    ptr1 = head
    ptr2 = slow
    while ptr1 is not ptr2:
        ptr1 = ptr1.next
        ptr2 = ptr2.next

    return ptr1  # 相遇点即为环入口


def detect_cycle_hashset(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    方法二：哈希集合，O(n) 时间，O(n) 空间。
    遍历链表，将节点存入 set，第一个重复出现的就是环入口。
    面试时快速写出，但空间不优。
    """
    visited = set()
    curr = head
    while curr:
        if curr in visited:
            return curr
        visited.add(curr)
        curr = curr.next
    return None


# ─── 辅助函数 ──────────────────────────────────────────────

def build_cycle_list(vals, pos):
    """构造带环链表，pos 为环入口下标（-1 表示无环）。"""
    if not vals:
        return None, None
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    cycle_entry = None
    if pos >= 0:
        nodes[-1].next = nodes[pos]
        cycle_entry = nodes[pos]
    return nodes[0], cycle_entry


if __name__ == "__main__":
    # 有环：入口在 index 1
    head, expected = build_cycle_list([3, 2, 0, -4], 1)
    assert detect_cycle(head) is expected
    assert detect_cycle_hashset(head) is expected

    # 有环：入口在 index 0
    head, expected = build_cycle_list([1, 2], 0)
    assert detect_cycle(head) is expected
    assert detect_cycle_hashset(head) is expected

    # 自环：单节点指向自身
    head, expected = build_cycle_list([1], 0)
    assert detect_cycle(head) is expected
    assert detect_cycle_hashset(head) is expected

    # 无环
    head, _ = build_cycle_list([1, 2, 3], -1)
    assert detect_cycle(head) is None
    assert detect_cycle_hashset(head) is None

    # 空链表
    assert detect_cycle(None) is None

    print("All tests passed.")
