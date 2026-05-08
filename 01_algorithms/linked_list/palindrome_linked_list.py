"""
题目: 回文链表
编号: LeetCode #234
难度: Easy
高频公司: 字节跳动、阿里巴巴、腾讯、微软、Facebook

题目描述
---------
给定一个单链表的头节点 head，判断该链表是否为回文链表，是则返回 true，否则返回 false。
回文即链表正向读与逆向读完全相同，如 [1,2,2,1] 或 [1,2,3,2,1]。
进阶要求：用 O(n) 时间复杂度和 O(1) 空间复杂度解决。

示例
------
输入: head = [1, 2, 2, 1]
输出: true

输入: head = [1, 2]
输出: false

约束
------
- 链表节点数在 [1, 10⁵] 之间
- 0 <= Node.val <= 9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: 找中点 + 反转后半段 + 双指针比较，O(n) 时间 O(1) 空间
核心三步:
  1. 快慢指针找链表中点 (slow 走到中点)
  2. 反转 slow.next 之后的后半段
  3. 双指针从两端向中间比对，全部相等则是回文
注意奇偶:
  - 奇数长度: [1,2,3,2,1] 中点是3，后半段从2开始
  - 偶数长度: [1,2,2,1] 中点是第一个2，后半段从第二个2开始
  快指针条件 fast and fast.next 使 slow 停在 左半段末尾
恢复链表 (面试加分): 比较完成后再次反转后半段，链表恢复原样
时间: O(n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
找中点细节:
  slow, fast = head, head
  while fast and fast.next:
      slow = slow.next; fast = fast.next.next
  -> 奇数长[1,2,3,2,1]: slow停在3; 偶数长[1,2,2,1]: slow停在第一个2

反转链表 (迭代):
  prev = None
  while cur: cur.next, prev, cur = prev, cur, cur.next
  return prev

比较:
  left = head, right = reversed_second_half
  while right: if left.val != right.val: return False
  return True

复杂度对比:
  - 暴力转数组: O(n) 时间 O(n) 空间
  - 本方案:     O(n) 时间 O(1) 空间 (原地)
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


# ── 反转链表辅助 ──────────────────────────────────────────

def reverse_list(head: ListNode) -> ListNode:
    prev, cur = None, head
    while cur:
        cur.next, prev, cur = prev, cur, cur.next
    return prev


# ── 主函数 ────────────────────────────────────────────────

def isPalindrome(head: ListNode) -> bool:
    if not head or not head.next:
        return True

    # Step 1: 快慢指针找中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: 反转后半段 (slow.next 开始)
    second_half_head = reverse_list(slow.next)

    # Step 3: 双指针逐一比较
    left, right = head, second_half_head
    is_palindrome = True
    while right:          # 后半段更短（奇数时），以 right 为准
        if left.val != right.val:
            is_palindrome = False
            break
        left = left.next
        right = right.next

    # Step 4: 恢复链表（可选，面试加分）
    slow.next = reverse_list(second_half_head)

    return is_palindrome


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 奇数长度回文: [1,2,3,2,1] -> True
    head = arr_to_list([1, 2, 3, 2, 1])
    assert isPalindrome(head) is True
    assert list_to_arr(head) == [1, 2, 3, 2, 1], "链表应被恢复"

    # 偶数长度回文: [1,2,2,1] -> True
    head = arr_to_list([1, 2, 2, 1])
    assert isPalindrome(head) is True
    assert list_to_arr(head) == [1, 2, 2, 1], "链表应被恢复"

    # 非回文: [1,2] -> False
    head = arr_to_list([1, 2])
    assert isPalindrome(head) is False

    # 非回文: [1,2,3,1] -> False
    head = arr_to_list([1, 2, 3, 1])
    assert isPalindrome(head) is False

    # 单节点: [1] -> True
    head = arr_to_list([1])
    assert isPalindrome(head) is True

    # 两节点回文: [1,1] -> True
    head = arr_to_list([1, 1])
    assert isPalindrome(head) is True

    # 全相同: [2,2,2,2] -> True
    head = arr_to_list([2, 2, 2, 2])
    assert isPalindrome(head) is True

    print("All tests passed for palindrome_linked_list!")
