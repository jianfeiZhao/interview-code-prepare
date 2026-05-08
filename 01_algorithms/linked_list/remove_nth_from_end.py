"""
题目: 删除链表的倒数第 N 个节点
编号: LeetCode #19
难度: Medium
高频公司: 字节跳动、腾讯、美团、微软

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。
进阶：能否用一趟扫描实现？

示例
------
输入: head = [1,2,3,4,5], n = 2
输出: [1,2,3,5]

输入: head = [1], n = 1
输出: []

约束
------
- 链表中结点的数目为 sz，1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: 快慢双指针 + 哑节点 (dummy node)，一次遍历
核心技巧:
  1. 设虚拟头节点 dummy，使删除头节点与普通节点统一处理
  2. fast 先走 n+1 步（多走1步是为了让 slow 停在被删节点的前驱）
  3. fast/slow 同步前进，直到 fast 到达链表末尾 (fast == None)
  4. 此时 slow.next 就是要删除的节点，执行 slow.next = slow.next.next
为什么是 n+1 步:
  链表长 L，倒数第 n 个即正数第 L-n+1 个
  slow 需停在第 L-n 个 (0-indexed: dummy 为第0)
  fast 从 dummy 走 n+1 步后在第 n+1 个位置
  同步走 L-n 步后，fast 在第 n+1+L-n = L+1 位置 = None
时间: O(n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
哑节点的作用:
  - 当 n == 链表长度时，要删除的是头节点
  - 没有哑节点需要特判 head；有哑节点统一处理

步骤:
  1. dummy -> head，slow = fast = dummy
  2. fast 向前走 n+1 步
  3. while fast != None: slow = slow.next; fast = fast.next
  4. slow.next = slow.next.next
  5. return dummy.next

边界情况:
  - 链表只有一个节点，n=1 -> 删除头节点 -> 返回 None
  - 删除头节点 (n == 链表长度)
  - 删除尾节点 (n == 1)
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ── 辅助函数 ──────────────────────────────────────────────

def arr_to_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for v in arr[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def list_to_arr(head):
    result, cur = [], head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result


# ── 主函数 ────────────────────────────────────────────────

def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    slow = fast = dummy

    # fast 先走 n+1 步
    for _ in range(n + 1):
        fast = fast.next

    # 同步前进直到 fast 到达链表末尾之后（None）
    while fast:
        slow = slow.next
        fast = fast.next

    # slow 现在指向被删节点的前驱
    slow.next = slow.next.next
    return dummy.next


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 基本用例: [1,2,3,4,5] 删倒数第2 -> [1,2,3,5]
    head = arr_to_list([1, 2, 3, 4, 5])
    result = removeNthFromEnd(head, 2)
    assert list_to_arr(result) == [1, 2, 3, 5], list_to_arr(result)

    # 删倒数第1 (尾节点): [1,2,3,4,5] -> [1,2,3,4]
    head = arr_to_list([1, 2, 3, 4, 5])
    result = removeNthFromEnd(head, 1)
    assert list_to_arr(result) == [1, 2, 3, 4], list_to_arr(result)

    # 删倒数第5 (头节点): [1,2,3,4,5] -> [2,3,4,5]
    head = arr_to_list([1, 2, 3, 4, 5])
    result = removeNthFromEnd(head, 5)
    assert list_to_arr(result) == [2, 3, 4, 5], list_to_arr(result)

    # 单节点: [1] 删倒数第1 -> []
    head = arr_to_list([1])
    result = removeNthFromEnd(head, 1)
    assert list_to_arr(result) == [], list_to_arr(result)

    # 两节点: [1,2] 删倒数第2 (头节点) -> [2]
    head = arr_to_list([1, 2])
    result = removeNthFromEnd(head, 2)
    assert list_to_arr(result) == [2], list_to_arr(result)

    # 两节点: [1,2] 删倒数第1 (尾节点) -> [1]
    head = arr_to_list([1, 2])
    result = removeNthFromEnd(head, 1)
    assert list_to_arr(result) == [1], list_to_arr(result)

    print("All tests passed for remove_nth_from_end!")
