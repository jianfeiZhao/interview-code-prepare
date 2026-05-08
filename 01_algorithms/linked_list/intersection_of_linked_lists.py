"""
题目: 相交链表
编号: LeetCode #160
难度: Easy
高频公司: 字节跳动、腾讯、阿里巴巴、美团、百度 (全系高频)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给你两个单链表的头节点 headA 和 headB，请你找出并返回两个单链表相交的起始节点。
如果两个链表不存在相交节点，返回 null。不能破坏链表结构，时间 O(n)，空间 O(1)。

示例
------
输入: intersectVal=8, listA=[4,1,8,4,5], listB=[5,6,1,8,4,5]
输出: 相交节点（值为 8）

输入: intersectVal=0, listA=[2,6,4], listB=[1,5]
输出: null

约束
------
- listA 中节点数量为 m，listB 中节点数量为 n
- 1 <= m, n <= 3 * 10^4
- 不能修改链表

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: 双指针"消除长度差"，O(n) 时间 O(1) 空间
核心技巧:
  两个指针 pA, pB 分别从 headA, headB 出发
  走到末尾后切换到对方的起点继续走
  若有交点: 两指针走了相同路程 (a+b+c 或 b+a+c) 时相遇在交点
  若无交点: 两者同时到达 None (a+b == b+a)
数学原理:
  设 A 独有长度为 a, B 独有长度为 b, 公共部分长度为 c
  pA 走: a + c + b，pB 走: b + c + a，步数相同，交点相遇
  无交点: a + b == b + a，同时到 None，返回 None
时间: O(m+n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
实现细节:
  pA = pA.next if pA else headB
  pB = pB.next if pB else headA
  注意: 用 is None 判断，而不是 if pA.next，因为 pA 可能已经是 None

  当 pA 到达 None (不是 pA.next 为 None)，才切换到 headB
  这样 pA 走完 A 的全部节点后才跳到 B 的起点

无交点情况:
  两指针都会在第二轮结束时同时到达 None
  None == None 为 True，循环 while pA is not pB 退出
  返回 pA (即 None)

注意: 相交是指节点对象相同（内存地址相同），不是值相同
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


def make_intersect(arrA_unique, arrB_unique, arr_common):
    """
    构造两个相交链表
    arrA_unique: A 独有部分 (值列表)
    arrB_unique: B 独有部分 (值列表)
    arr_common:  公共部分 (值列表)，可为空
    返回 (headA, headB, intersect_node or None)
    """
    common_head = arr_to_list(arr_common) if arr_common else None

    headA = arr_to_list(arrA_unique) if arrA_unique else None
    headB = arr_to_list(arrB_unique) if arrB_unique else None

    # 将 A 的尾部接上公共部分
    if headA:
        cur = headA
        while cur.next:
            cur = cur.next
        cur.next = common_head
    else:
        headA = common_head

    # 将 B 的尾部接上公共部分
    if headB:
        cur = headB
        while cur.next:
            cur = cur.next
        cur.next = common_head
    else:
        headB = common_head

    return headA, headB, common_head


# ── 主函数 ────────────────────────────────────────────────

def getIntersectionNode(headA: ListNode, headB: ListNode) -> ListNode:
    pA, pB = headA, headB
    while pA is not pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
    return pA   # 相交节点 或 None


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 用例1: 有交点
    # A: 4->1->8->4->5, B: 5->6->1->8->4->5 (公共: 8->4->5)
    headA, headB, common = make_intersect([4, 1], [5, 6, 1], [8, 4, 5])
    result = getIntersectionNode(headA, headB)
    assert result is common, f"应返回公共头节点(val=8)，实际val={result.val if result else None}"

    # 用例2: A和B完全相同 (headA == headB)
    common_only = arr_to_list([1, 2, 3])
    result = getIntersectionNode(common_only, common_only)
    assert result is common_only

    # 用例3: 无交点
    headA = arr_to_list([2, 6, 4])
    headB = arr_to_list([1, 5])
    result = getIntersectionNode(headA, headB)
    assert result is None, f"无交点应返回 None，实际 {result}"

    # 用例4: 交点是末尾节点 (共享最后一个节点)
    headA, headB, common = make_intersect([1, 2, 3], [4, 5], [9])
    result = getIntersectionNode(headA, headB)
    assert result is common and result.val == 9

    # 用例5: 交点是 A 的头节点 (A 独有部分为空)
    headA, headB, common = make_intersect([], [1, 2], [3, 4, 5])
    result = getIntersectionNode(headA, headB)
    assert result is common

    # 用例6: 两个链表都只有一个节点且相交
    node = ListNode(1)
    result = getIntersectionNode(node, node)
    assert result is node

    # 用例7: 两个链表都只有一个节点但不相交
    a, b = ListNode(1), ListNode(1)
    result = getIntersectionNode(a, b)
    assert result is None

    print("All tests passed for intersection_of_linked_lists!")
