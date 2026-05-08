"""
题目: 两两交换链表中的节点
编号: LeetCode #24
难度: Medium
高频公司: 字节跳动、腾讯、阿里巴巴、微软

题目描述
---------
给定一个链表，两两交换其中相邻的节点，并返回交换后的链表头节点。
必须实际进行节点交换（改变指针），而不是仅仅改变节点内部的值。
若链表节点数为奇数，最后一个节点不参与交换，保持原位。

示例
------
输入: head = [1, 2, 3, 4]
输出: [2, 1, 4, 3]

输入: head = [1, 2, 3]
输出: [2, 1, 3]

约束
------
- 链表节点数在 [0, 100] 之间
- 0 <= Node.val <= 100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标: 交换每两个相邻节点 (不改变节点值，只改变指针)
算法: 迭代法 (dummy节点) 或 递归法，均 O(n) 时间 O(1)/O(n)空间
核心技巧 (迭代):
  dummy -> 1 -> 2 -> 3 -> 4
  prev = dummy, node1 = 1, node2 = 2
  操作: prev->2->1->3，然后 prev 移到 1（此时的位置）
  关键: 每次交换前保存 node2.next (即下一对的第一个节点)
递归核心思路:
  swapPairs(head) = head.next 成为新头
  head.next = swapPairs(head.next.next)  递归处理后续
  head.next.next = head                  交换当前对
时间: O(n), 空间: 迭代O(1) / 递归O(n)栈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
迭代步骤图解 (以 [1,2,3,4] 为例):
  初始: dummy -> 1 -> 2 -> 3 -> 4
  第1轮: prev=dummy, node1=1, node2=2
    next_pair = node2.next = 3
    prev.next = node2        => dummy -> 2
    node2.next = node1       => dummy -> 2 -> 1
    node1.next = next_pair   => dummy -> 2 -> 1 -> 3 -> 4
    prev = node1 (=1), 继续
  第2轮: prev=1, node1=3, node2=4
    next_pair = None
    prev.next = 4, 4.next = 3, 3.next = None
    结果: dummy -> 2 -> 1 -> 4 -> 3

指针操作顺序很关键，用 next_pair 提前保存下一对头节点
可简化为:
  node1, node2 = prev.next, prev.next.next
  prev.next, node2.next, node1.next = node2, node1, node2.next
  注意: Python 右侧表达式先全部求值，再同时赋值，可以这样写

奇数长度处理:
  [1,2,3]: 交换1,2后 -> [2,1,3]，3没有配对，保持原位
  while prev.next and prev.next.next: 确保有两个节点才交换
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


# ── 方案A: 迭代 (推荐，O(1)空间) ─────────────────────────

def swapPairs(head: ListNode) -> ListNode:
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next and prev.next.next:
        node1 = prev.next
        node2 = prev.next.next

        # 保存下一对的头节点
        next_pair = node2.next

        # 执行交换
        prev.next = node2
        node2.next = node1
        node1.next = next_pair

        # prev 移动到已交换对的末尾 (node1 现在是后者)
        prev = node1

    return dummy.next


# ── 方案B: 递归 (简洁，O(n)栈空间) ──────────────────────

def swapPairsRecursive(head: ListNode) -> ListNode:
    # 基本情况: 没有节点或只有一个节点
    if not head or not head.next:
        return head

    new_head = head.next        # 第二个节点成为新头
    head.next = swapPairsRecursive(new_head.next)  # 递归处理后续
    new_head.next = head        # 交换当前对
    return new_head


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # 偶数长度: [1,2,3,4] -> [2,1,4,3]
    head = arr_to_list([1, 2, 3, 4])
    result = swapPairs(head)
    assert list_to_arr(result) == [2, 1, 4, 3], list_to_arr(result)

    # 奇数长度: [1,2,3] -> [2,1,3]
    head = arr_to_list([1, 2, 3])
    result = swapPairs(head)
    assert list_to_arr(result) == [2, 1, 3], list_to_arr(result)

    # 单节点: [1] -> [1]
    head = arr_to_list([1])
    result = swapPairs(head)
    assert list_to_arr(result) == [1], list_to_arr(result)

    # 空链表
    result = swapPairs(None)
    assert result is None

    # 两节点: [1,2] -> [2,1]
    head = arr_to_list([1, 2])
    result = swapPairs(head)
    assert list_to_arr(result) == [2, 1], list_to_arr(result)

    # 六节点: [1,2,3,4,5,6] -> [2,1,4,3,6,5]
    head = arr_to_list([1, 2, 3, 4, 5, 6])
    result = swapPairs(head)
    assert list_to_arr(result) == [2, 1, 4, 3, 6, 5], list_to_arr(result)

    # 测试递归版本
    head = arr_to_list([1, 2, 3, 4])
    result = swapPairsRecursive(head)
    assert list_to_arr(result) == [2, 1, 4, 3], list_to_arr(result)

    head = arr_to_list([1, 2, 3])
    result = swapPairsRecursive(head)
    assert list_to_arr(result) == [2, 1, 3], list_to_arr(result)

    head = arr_to_list([1, 2, 3, 4, 5, 6])
    result = swapPairsRecursive(head)
    assert list_to_arr(result) == [2, 1, 4, 3, 6, 5], list_to_arr(result)

    print("All tests passed for swap_pairs!")
