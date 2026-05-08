"""
题目: 两数相加
编号: LeetCode #2
难度: Medium
高频公司: 字节跳动、腾讯、阿里巴巴、Google、Amazon、微软 (超高频)

题目描述
---------
给定两个非空链表，分别表示两个非负整数，每个节点存储一位数字，数字按逆序存储（个位在链表头）。
将两个数相加，并以相同形式返回表示结果的链表。
例如，342 存为 2->4->3，465 存为 5->6->4，相加结果 807 应返回 7->0->8。

示例
------
输入: l1 = [2,4,3], l2 = [5,6,4]
输出: [7,0,8]  （342 + 465 = 807）

输入: l1 = [9,9,9], l2 = [1]
输出: [0,0,0,1]  （999 + 1 = 1000）

约束
------
- 每个链表节点数在 [1, 100] 之间
- 0 <= Node.val <= 9
- 保证输入代表的数字不含前导零（除数字 0 本身）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: 模拟竖式加法，逐位相加并处理进位
核心技巧:
  1. 哑节点 dummy 简化头节点处理
  2. 同时遍历两链表，用 carry 维护进位
  3. 循环条件: while l1 or l2 or carry (最后的进位也要处理)
  4. 每位: val = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
     新节点值 = val % 10, 新进位 = val // 10
链表存储方式: 逆序存储，即个位在链表头
              342 存为 2->4->3，符合加法从低位开始的方向
时间: O(max(m,n)), 空间: O(max(m,n)+1) 用于结果

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
举例: 342 + 465 = 807
  l1: 2->4->3  l2: 5->6->4
  位1: 2+5+0=7, carry=0, 结果位=7
  位2: 4+6+0=10, carry=1, 结果位=0
  位3: 3+4+1=8, carry=0, 结果位=8
  结果: 7->0->8  表示 807

进位延伸场景: 999 + 1 = 1000
  l1: 9->9->9  l2: 1
  位1: 9+1=10, carry=1, 结果=0
  位2: 9+0+1=10, carry=1, 结果=0
  位3: 9+0+1=10, carry=1, 结果=0
  l1, l2 均为 None，但 carry=1，继续循环
  位4: 0+0+1=1, carry=0, 结果=1
  最终: 0->0->0->1 表示 1000

关键: while l1 or l2 or carry 确保最高位进位被处理

变体: #445 两数相加II (正序存储) -> 用栈或反转链表后再用本算法
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ── 辅助函数 ──────────────────────────────────────────────

def arr_to_list(arr):
    """数组转链表 (arr[0] 是个位)"""
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


def num_to_list(num):
    """整数转链表 (逆序，个位在头)"""
    if num == 0:
        return ListNode(0)
    digits = []
    while num:
        digits.append(num % 10)
        num //= 10
    return arr_to_list(digits)


def list_to_num(head):
    """链表转整数 (逆序，个位在头)"""
    result, mul, cur = 0, 1, head
    while cur:
        result += cur.val * mul
        mul *= 10
        cur = cur.next
    return result


# ── 主函数 ────────────────────────────────────────────────

def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)
    cur = dummy
    carry = 0

    while l1 or l2 or carry:
        val = carry
        if l1:
            val += l1.val
            l1 = l1.next
        if l2:
            val += l2.val
            l2 = l2.next

        carry, digit = divmod(val, 10)   # carry = val//10, digit = val%10
        cur.next = ListNode(digit)
        cur = cur.next

    return dummy.next


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 基本用例: 342 + 465 = 807
    l1 = num_to_list(342)
    l2 = num_to_list(465)
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == 807, list_to_num(result)

    # 进位产生额外节点: 999 + 1 = 1000
    l1 = num_to_list(999)
    l2 = num_to_list(1)
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == 1000, list_to_num(result)
    assert list_to_arr(result) == [0, 0, 0, 1], list_to_arr(result)

    # 长度不等: 9999 + 1 = 10000
    l1 = num_to_list(9999)
    l2 = num_to_list(1)
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == 10000, list_to_num(result)

    # 一个为0: 0 + 0 = 0
    l1 = num_to_list(0)
    l2 = num_to_list(0)
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == 0, list_to_num(result)

    # 一个为0: 123 + 0 = 123
    l1 = num_to_list(123)
    l2 = num_to_list(0)
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == 123, list_to_num(result)

    # 较大数字
    l1 = num_to_list(9999999)
    l2 = num_to_list(9999)
    expected = 9999999 + 9999
    result = addTwoNumbers(l1, l2)
    assert list_to_num(result) == expected, f"{list_to_num(result)} != {expected}"

    # 逐位验证: 2->4->3 + 5->6->4 = 7->0->8
    l1 = arr_to_list([2, 4, 3])
    l2 = arr_to_list([5, 6, 4])
    result = addTwoNumbers(l1, l2)
    assert list_to_arr(result) == [7, 0, 8], list_to_arr(result)

    print("All tests passed for add_two_numbers!")
