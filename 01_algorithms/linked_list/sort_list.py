"""
题目: 排序链表
编号: LeetCode #148
难度: Medium
高频公司: 字节跳动、阿里巴巴、腾讯、百度

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给你链表的头结点 head，请将其按升序排列并返回排序后的链表。
进阶：能否以 O(n log n) 时间复杂度和 O(1) 的额外空间复杂度（不计递归栈）对链表排序？

示例
------
输入: head = [4,2,1,3]
输出: [1,2,3,4]

输入: head = [-1,5,3,4,0]
输出: [-1,0,3,4,5]

约束
------
- 链表中节点的数目在范围 [0, 5 * 10^4] 内
- -10^5 <= Node.val <= 10^5

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: 自顶向下归并排序 (递归)，O(n log n) 时间 O(log n) 空间
进阶: 自底向上归并排序，O(n log n) 时间 O(1) 空间 (面试加分)
核心三步:
  1. 快慢指针找中点，切断链表为两半
  2. 递归排序左半段和右半段
  3. 合并两个有序链表 (merge two sorted lists)
为什么用归并而不是快排:
  链表无法随机访问，快排的 partition 需要频繁跳跃，效率低
  归并天然适合顺序访问，且保证 O(n log n) 最坏复杂度
时间: O(n log n), 空间: O(log n) 递归栈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
找中点细节 (fast.next 而非 fast):
  while fast.next and fast.next.next:
  奇数 [1,2,3]: slow 停在 1（第一个），切为 [1] 和 [2,3]
  偶数 [1,2,3,4]: slow 停在 2，切为 [1,2] 和 [3,4]
  -> 使两半尽量等长，避免无限递归

切断: 保存 slow.next，将 slow.next = None

合并两有序链表:
  用 dummy 头节点，比较 l1/l2 的头部，小的接上去
  while l1 and l2: ...
  接剩余部分: cur.next = l1 or l2

自底向上归并 (O(1)空间):
  从 sublen=1 开始，每次合并相邻的 sublen 长度段
  sublen 每轮翻倍 (1, 2, 4, 8...)
  共 log n 轮，每轮 O(n)，总 O(n log n)

易错点:
  - 找中点时的停止条件影响是否死循环
  - 切断左半段 (slow.next = None) 不可漏
  - 合并时 l1 或 l2 为 None 的边界
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


# ── 合并两个有序链表 ──────────────────────────────────────

def merge(l1: ListNode, l2: ListNode) -> ListNode:
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
    cur.next = l1 if l1 else l2
    return dummy.next


# ── 方案A: 自顶向下归并排序 (递归) ────────────────────────

def sortList(head: ListNode) -> ListNode:
    # 基本情况: 空或单节点
    if not head or not head.next:
        return head

    # Step 1: 快慢指针找中点，切断
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None   # 切断左右两半

    # Step 2: 递归排序
    left = sortList(head)
    right = sortList(mid)

    # Step 3: 合并
    return merge(left, right)


# ── 方案B: 自底向上归并排序 (迭代，O(1)空间) ─────────────

def sortListBottomUp(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    # 计算链表长度
    length, cur = 0, head
    while cur:
        length += 1
        cur = cur.next

    dummy = ListNode(0, head)
    sublen = 1

    while sublen < length:
        cur = dummy.next
        tail = dummy      # 已排序部分的尾节点

        while cur:
            # 取左半段 (sublen 个节点)
            left = cur
            right = split(left, sublen)   # 切出左半，right 是右半头
            cur = split(right, sublen)    # 切出右半，cur 是下一组头

            # 合并左右，接到 tail 后面
            merged_head, merged_tail = merge_with_tail(left, right)
            tail.next = merged_head
            tail = merged_tail

        tail.next = None   # 防止旧指针残留
        sublen *= 2

    return dummy.next


def split(head: ListNode, n: int):
    """从 head 开始取 n 个节点，切断并返回后续链表头"""
    cur = head
    for _ in range(n - 1):
        if cur and cur.next:
            cur = cur.next
        else:
            break
    if not cur:
        return None
    rest = cur.next
    cur.next = None
    return rest


def merge_with_tail(l1: ListNode, l2: ListNode):
    """合并两个有序链表，返回 (头, 尾)"""
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
    cur.next = l1 if l1 else l2
    while cur.next:
        cur = cur.next
    return dummy.next, cur


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 基本用例: [4,2,1,3] -> [1,2,3,4]
    head = arr_to_list([4, 2, 1, 3])
    result = sortList(head)
    assert list_to_arr(result) == [1, 2, 3, 4], list_to_arr(result)

    # 含负数: [-1,5,3,4,0] -> [-1,0,3,4,5]
    head = arr_to_list([-1, 5, 3, 4, 0])
    result = sortList(head)
    assert list_to_arr(result) == [-1, 0, 3, 4, 5], list_to_arr(result)

    # 已排序: [1,2,3,4,5]
    head = arr_to_list([1, 2, 3, 4, 5])
    result = sortList(head)
    assert list_to_arr(result) == [1, 2, 3, 4, 5]

    # 逆序: [5,4,3,2,1]
    head = arr_to_list([5, 4, 3, 2, 1])
    result = sortList(head)
    assert list_to_arr(result) == [1, 2, 3, 4, 5]

    # 单节点
    head = arr_to_list([1])
    result = sortList(head)
    assert list_to_arr(result) == [1]

    # 两节点: [2,1] -> [1,2]
    head = arr_to_list([2, 1])
    result = sortList(head)
    assert list_to_arr(result) == [1, 2]

    # 重复元素: [3,1,2,1,3] -> [1,1,2,3,3]
    head = arr_to_list([3, 1, 2, 1, 3])
    result = sortList(head)
    assert list_to_arr(result) == [1, 1, 2, 3, 3]

    # 空链表
    result = sortList(None)
    assert result is None

    # 测试自底向上版本
    head = arr_to_list([4, 2, 1, 3])
    result = sortListBottomUp(head)
    assert list_to_arr(result) == [1, 2, 3, 4], list_to_arr(result)

    head = arr_to_list([-1, 5, 3, 4, 0])
    result = sortListBottomUp(head)
    assert list_to_arr(result) == [-1, 0, 3, 4, 5], list_to_arr(result)

    print("All tests passed for sort_list!")
