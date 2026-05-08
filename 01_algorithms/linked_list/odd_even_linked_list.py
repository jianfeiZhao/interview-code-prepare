"""
题目: 奇偶链表
编号: LeetCode #328
难度: Medium
高频公司: 字节跳动、美团、腾讯、LinkedIn

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给定单链表的头节点 head，将所有下标为奇数的节点和偶数的节点分别组合在一起，
然后返回重新排序的列表。奇数组在前，偶数组在后，节点顺序保持原有相对顺序。
要求空间复杂度 O(1)，时间复杂度 O(n)。

示例
------
输入: head = [1,2,3,4,5]
输出: [1,3,5,2,4]

输入: head = [2,1,3,5,6,4,7]
输出: [2,3,6,7,1,5,4]

约束
------
- n == 链表中的节点数，0 <= n <= 10^4
- -10^6 <= Node.val <= 10^6

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标: 将所有奇数位节点放前面，偶数位节点放后面，保持相对顺序
     注意是位置的奇偶（1-indexed），不是节点值的奇偶
算法: 双指针分离法，原地修改，O(n) 时间 O(1) 空间
核心技巧:
  维护两条链: 奇数链 (odd) 和 偶数链 (even)
  odd 指针跳过偶数节点，even 指针跳过奇数节点
  最后将奇数链尾部接上偶数链头部
关键: even_head 在循环前保存偶数链头节点，最后用于拼接
时间: O(n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
举例: [1,2,3,4,5]
  初始: odd=1, even=2, even_head=2
  迭代1: odd.next=even.next=3, odd=3; even.next=odd.next=4, even=4
  迭代2: odd.next=even.next=5, odd=5; even.next=odd.next=None, even=None
  循环结束 (even=None): odd.next = even_head (=2)
  结果: 1->3->5->2->4

循环条件: while even and even.next
  - even 为 None: 偶数节点全处理完（偶数长度链表）
  - even.next 为 None: 最后一个奇数节点已处理（奇数长度链表）

初始化:
  odd = head         (第1个节点，奇数位)
  even = head.next   (第2个节点，偶数位)
  even_head = even   (保存偶数链头，最后拼接用)

连接: odd.next = even_head (在 odd 指针移动到奇数链最后时)

边界情况:
  - 空链表或只有1个节点: 直接返回
  - 两个节点: odd=1, even=2，循环不执行，odd.next=even_head=2，正确
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

def oddEvenList(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    odd = head
    even = head.next
    even_head = even        # 保存偶数链头

    while even and even.next:
        odd.next = even.next    # 奇数链跳过偶数节点
        odd = odd.next
        even.next = odd.next    # 偶数链跳过奇数节点
        even = even.next

    odd.next = even_head        # 奇数链尾接上偶数链头
    return head


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 基本用例: [1,2,3,4,5] -> [1,3,5,2,4]
    head = arr_to_list([1, 2, 3, 4, 5])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1, 3, 5, 2, 4], list_to_arr(result)

    # 偶数长度: [2,1,3,5,6,4,7] -> [2,3,6,7,1,5,4]
    head = arr_to_list([2, 1, 3, 5, 6, 4, 7])
    result = oddEvenList(head)
    assert list_to_arr(result) == [2, 3, 6, 7, 1, 5, 4], list_to_arr(result)

    # 四个节点: [1,2,3,4] -> [1,3,2,4]
    head = arr_to_list([1, 2, 3, 4])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1, 3, 2, 4], list_to_arr(result)

    # 两个节点: [1,2] -> [1,2]
    head = arr_to_list([1, 2])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1, 2], list_to_arr(result)

    # 单节点: [1] -> [1]
    head = arr_to_list([1])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1], list_to_arr(result)

    # 空链表
    assert oddEvenList(None) is None

    # 三个节点: [1,2,3] -> [1,3,2]
    head = arr_to_list([1, 2, 3])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1, 3, 2], list_to_arr(result)

    # 全相同值: [1,1,1,1,1] -> [1,1,1,1,1] (顺序变了但值相同)
    head = arr_to_list([1, 1, 1, 1, 1])
    result = oddEvenList(head)
    assert list_to_arr(result) == [1, 1, 1, 1, 1]

    print("All tests passed for odd_even_linked_list!")
