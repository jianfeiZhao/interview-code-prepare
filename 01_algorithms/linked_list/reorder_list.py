"""
题目: 重排链表
编号: LeetCode #143
难度: Medium
高频公司: 字节跳动、腾讯、阿里巴巴、Amazon

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给定一个单链表 L：L0 → L1 → … → Ln-1 → Ln，将其重新排列后变为：
L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

示例
------
输入: head = [1,2,3,4]
输出: [1,4,2,3]

输入: head = [1,2,3,4,5]
输出: [1,5,2,4,3]

约束
------
- 链表的长度范围为 [1, 5 * 10^4]
- 1 <= Node.val <= 1000

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标: L0->L1->...->Ln 变为 L0->Ln->L1->Ln-1->L2->Ln-2->...
算法: 三步走，O(n) 时间 O(1) 空间
  步骤1: 快慢指针找链表中点，切断为前后两段
  步骤2: 反转后半段链表
  步骤3: 交替合并前半段和（已反转的）后半段
核心: 把问题拆解为三个经典子问题，每步都是独立模板
时间: O(n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
举例: [1,2,3,4,5]
  Step1 找中点并切断:
    slow 停在 3，将 slow.next = None
    前半: 1->2->3  后半: 4->5
  Step2 反转后半段:
    4->5 变为 5->4
  Step3 交替合并:
    取前半一个 (1)，取后半一个 (5)
    取前半一个 (2)，取后半一个 (4)
    取前半一个 (3)，后半已空
    结果: 1->5->2->4->3

偶数情况: [1,2,3,4]
  前半: 1->2  后半(reversed): 4->3
  合并: 1->4->2->3

合并细节 (原地交叉插入):
  while second:
      tmp1, tmp2 = first.next, second.next
      first.next = second
      second.next = tmp1
      first, second = tmp1, tmp2

找中点的快慢指针停止条件:
  while fast.next and fast.next.next:
  此条件使 slow 停在 前半段末尾 (偶数时停在左中点)
  [1,2,3,4]: slow=2, 切断后前半1->2, 后半3->4 (长度相等，合并时前半正好消耗完)
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


# ── 主函数 (原地修改，无返回值) ───────────────────────────

def reorderList(head: ListNode) -> None:
    if not head or not head.next:
        return

    # Step 1: 找中点，切断为两半
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    # slow 是前半段末尾节点
    second = slow.next
    slow.next = None       # 切断

    # Step 2: 反转后半段
    prev, cur = None, second
    while cur:
        cur.next, prev, cur = prev, cur, cur.next
    second = prev          # second 现在是反转后半段的头

    # Step 3: 交替合并
    first = head
    while second:
        tmp1 = first.next
        tmp2 = second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 奇数长度: [1,2,3,4,5] -> [1,5,2,4,3]
    head = arr_to_list([1, 2, 3, 4, 5])
    reorderList(head)
    assert list_to_arr(head) == [1, 5, 2, 4, 3], list_to_arr(head)

    # 偶数长度: [1,2,3,4] -> [1,4,2,3]
    head = arr_to_list([1, 2, 3, 4])
    reorderList(head)
    assert list_to_arr(head) == [1, 4, 2, 3], list_to_arr(head)

    # 两个节点: [1,2] -> [1,2]
    head = arr_to_list([1, 2])
    reorderList(head)
    assert list_to_arr(head) == [1, 2], list_to_arr(head)

    # 单节点: [1] -> [1]
    head = arr_to_list([1])
    reorderList(head)
    assert list_to_arr(head) == [1], list_to_arr(head)

    # 三个节点: [1,2,3] -> [1,3,2]
    head = arr_to_list([1, 2, 3])
    reorderList(head)
    assert list_to_arr(head) == [1, 3, 2], list_to_arr(head)

    # 六个节点: [1,2,3,4,5,6] -> [1,6,2,5,3,4]
    head = arr_to_list([1, 2, 3, 4, 5, 6])
    reorderList(head)
    assert list_to_arr(head) == [1, 6, 2, 5, 3, 4], list_to_arr(head)

    print("All tests passed for reorder_list!")
