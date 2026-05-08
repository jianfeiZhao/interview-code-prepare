"""
题目: 链表环检测 + 入口节点
编号: LeetCode #141 (环检测) + #142 (入口节点)
难度: Medium
高频公司: 字节跳动、腾讯、阿里巴巴、美团、微软、Google (全系高频)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给你一个链表的头节点 head，判断链表中是否有环。
如果链表中存在环，则返回 True，否则返回 False。
进阶：能否用 O(1) 内存解决此题？

示例
------
输入: head = [3,2,0,-4]，tail 连接到下标 1 的节点
输出: True

输入: head = [1,2]，tail 连接到下标 0 的节点
输出: True

约束
------
- 链表中节点的数目范围是 [0, 10^4]
- -10^5 <= Node.val <= 10^5

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法: Floyd 判圈算法 (龟兔赛跑)
核心技巧:
  1. 快慢指针同时出发，slow每次走1步，fast每次走2步
  2. 若有环，fast 和 slow 必然在环内相遇
  3. 找入口: 相遇后，将 slow 重置到 head，fast 留在相遇点
     两者同速前进，再次相遇即为环入口
关键数学推导:
  设链表头到环入口距离为 a，环长为 b，相遇点距环入口为 k
  相遇时: slow走了 a+k，fast走了 a+k+n*b (n≥1圈)
  fast = 2*slow => a+k+n*b = 2*(a+k) => a = n*b - k
  即: 从头走 a 步 == 从相遇点再走 (n*b-k) 步，均到达环入口
时间: O(n), 空间: O(1)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#141 判断是否有环:
  - slow/fast 同起点，slow+1, fast+2
  - fast 或 fast.next 为 None => 无环
  - slow == fast => 有环

#142 找环的入口节点:
  - 先用 #141 找到相遇点
  - 再令 ptr1=head, ptr2=相遇点，同速前进
  - 再次相遇即为入口 (利用上面的数学关系)

易错点:
  - fast 指针移动前需检查 fast 和 fast.next 是否为 None
  - 相遇不代表是入口，需要第二次追及
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ── 辅助函数 ──────────────────────────────────────────────

def arr_to_list(arr):
    """数组转链表，返回头节点"""
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for v in arr[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def list_to_arr(head, limit=100):
    """链表转数组（防止死循环加 limit）"""
    result, cur, cnt = [], head, 0
    while cur and cnt < limit:
        result.append(cur.val)
        cur = cur.next
        cnt += 1
    return result


def make_cycle(head, pos):
    """将链表尾部连接到第 pos 个节点（0-indexed），pos=-1 表示不成环"""
    if pos == -1 or not head:
        return head
    tail, entry, cur, idx = head, None, head, 0
    while cur.next:
        if idx == pos:
            entry = cur
        cur = cur.next
        idx += 1
    if idx == pos:
        entry = cur          # pos 恰好是最后一个节点
    cur.next = entry         # 尾部指向 entry，形成环
    return head


# ── #141 环检测 ────────────────────────────────────────────

def has_cycle(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# ── #142 找环入口 ──────────────────────────────────────────

def detect_cycle(head: ListNode):
    """返回环入口节点，无环返回 None"""
    slow = fast = head
    # Phase 1: 找相遇点
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None          # fast 或 fast.next 为 None，无环

    # Phase 2: 找入口
    ptr = head
    while ptr is not slow:
        ptr = ptr.next
        slow = slow.next
    return ptr               # 再次相遇即为环入口


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    # ---- 测试 has_cycle ----
    # 无环链表
    head = arr_to_list([3, 2, 0, -4])
    assert has_cycle(head) is False, "无环应返回 False"

    # 有环: 尾->索引1 (值为2)
    head = arr_to_list([3, 2, 0, -4])
    make_cycle(head, 1)
    assert has_cycle(head) is True, "有环应返回 True"

    # 单节点无环
    head = arr_to_list([1])
    assert has_cycle(head) is False

    # 单节点自环
    head = arr_to_list([1])
    head.next = head
    assert has_cycle(head) is True

    # ---- 测试 detect_cycle ----
    # 无环
    head = arr_to_list([3, 2, 0, -4])
    assert detect_cycle(head) is None

    # 尾->索引1 (值为2)
    head = arr_to_list([3, 2, 0, -4])
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[1]   # 手动成环，入口=nodes[1]
    entry = detect_cycle(head)
    assert entry is nodes[1], f"入口应为 nodes[1](val=2)，实际 val={entry.val}"

    # 尾->索引0 (整个链表是一个大环)
    head = arr_to_list([1, 2])
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[0]
    entry = detect_cycle(head)
    assert entry is nodes[0], f"入口应为 head(val=1)，实际 val={entry.val}"

    print("All tests passed for linked_list_cycle!")
