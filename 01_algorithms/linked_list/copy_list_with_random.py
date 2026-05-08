"""
题目: 复制带随机指针的链表
编号: LeetCode #138
难度: Medium
高频公司: 字节跳动、阿里巴巴、腾讯、Amazon、Microsoft

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

题目描述
---------
给你一个长度为 n 的链表，每个节点包含一个额外增加的随机指针 random，
该指针可以指向链表中的任何节点或空节点。构造这个链表的深拷贝，
返回复制链表的头节点。不能使用原始链表的任何节点的指针或引用。

示例
------
输入: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出: [[7,null],[13,0],[11,4],[10,2],[1,0]]  （深拷贝，新节点）

约束
------
- 0 <= n <= 1000
- -10^4 <= Node.val <= 10^4
- Node.random 为 null 或指向链表中某节点

TL;DR 速览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
两种方案:
  方案A (哈希表): 原节点->新节点 的映射，两次遍历，O(n)空间
  方案B (原地交织): 不用额外空间，三次遍历，O(1)空间 (面试首选)

方案B 核心三步:
  Step1: 在每个原节点后插入其复制节点
         1->1'->2->2'->3->3'->None
  Step2: 设置每个复制节点的 random 指针
         new.random = old.random.next (原random的下一个就是复制的random)
  Step3: 拆分两个链表，恢复原链表结构
时间: O(n), 空间: O(1) (方案B)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
详细解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
方案A (哈希表) 流程:
  1. 遍历原链表，为每个节点创建对应的新节点，存入 hash_map
  2. 再次遍历，用 hash_map 设置 next 和 random

方案B (原地交织) 详细流程:
  Step1: 插入复制节点
    cur -> cur.next 变为 cur -> cur_copy -> cur.next
    cur_copy.next = cur.next (先保存原来的 next)
    cur.next = cur_copy
    cur = cur_copy.next

  Step2: 设置 random 指针
    遍历原链表节点 (步长2)
    cur.next.random = cur.random.next if cur.random else None
    注意: cur.next 是复制节点，cur.random.next 是 random 指向的复制节点

  Step3: 拆分
    用 dummy_new 收集新链表
    同时修复原链表的 next 指针
    cur.next = cur.next.next (跳过复制节点)
    new_cur.next = new_cur.next.next (跳过原节点)

易错点:
  - Step2 中 cur.random 可能为 None，需判断
  - Step3 拆分时要保证原链表和新链表都被正确断开
"""


class Node:
    def __init__(self, x: int, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


# ── 辅助函数 ──────────────────────────────────────────────

def arr_to_list(arr):
    """
    arr: [[val, random_index], ...], random_index 为 None 或整数索引
    返回 (head, nodes列表)
    """
    if not arr:
        return None, []
    nodes = [Node(v) for v, _ in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    for i, (_, rand_idx) in enumerate(arr):
        if rand_idx is not None:
            nodes[i].random = nodes[rand_idx]
    return nodes[0], nodes


def list_to_arr(head):
    """返回 [[val, random_index], ...]"""
    if not head:
        return []
    nodes, cur = [], head
    while cur:
        nodes.append(cur)
        cur = cur.next
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    return [[n.val, node_to_idx.get(n.random)] for n in nodes]


# ── 方案A: 哈希表，O(n)空间 ───────────────────────────────

def copyRandomList_hashmap(head: Node) -> Node:
    if not head:
        return None
    hash_map = {}
    cur = head
    while cur:
        hash_map[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        hash_map[cur].next = hash_map.get(cur.next)
        hash_map[cur].random = hash_map.get(cur.random)
        cur = cur.next
    return hash_map[head]


# ── 方案B: 原地交织，O(1)空间 (推荐) ─────────────────────

def copyRandomList(head: Node) -> Node:
    if not head:
        return None

    # Step 1: 在每个原节点后插入复制节点
    cur = head
    while cur:
        copy = Node(cur.val)
        copy.next = cur.next
        cur.next = copy
        cur = copy.next     # 跳到下一个原节点

    # Step 2: 设置复制节点的 random 指针
    cur = head
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        # else: cur.next.random 默认是 None，无需赋值
        cur = cur.next.next

    # Step 3: 拆分两个链表
    dummy = Node(0)
    new_cur = dummy
    cur = head
    while cur:
        new_cur.next = cur.next        # 新节点接到新链表
        cur.next = cur.next.next       # 修复原链表
        new_cur = new_cur.next
        cur = cur.next

    return dummy.next


# ── 测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    def deep_equal(h1, h2):
        """深度比较两个带随机指针链表是否内容相同（且是不同节点对象）"""
        arr1 = list_to_arr(h1)
        arr2 = list_to_arr(h2)
        return arr1 == arr2

    def no_shared_nodes(orig, copy):
        """检查复制链表中所有节点都是新对象"""
        orig_nodes, cur = set(), orig
        while cur:
            orig_nodes.add(id(cur))
            cur = cur.next
        cur = copy
        while cur:
            if id(cur) in orig_nodes:
                return False
            cur = cur.next
        return True

    # 用例1: [[7,None],[13,0],[11,4],[10,2],[1,0]]
    data = [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
    orig, _ = arr_to_list(data)
    copy = copyRandomList(orig)
    assert deep_equal(orig, copy), f"内容不同: {list_to_arr(orig)} vs {list_to_arr(copy)}"
    assert no_shared_nodes(orig, copy), "存在共享节点"

    # 方案A 也测试
    orig2, _ = arr_to_list(data)
    copy2 = copyRandomList_hashmap(orig2)
    assert deep_equal(orig2, copy2)
    assert no_shared_nodes(orig2, copy2)

    # 用例2: [[1,1],[2,1]] (random 指向自身或相邻)
    data2 = [[1, 1], [2, 1]]
    orig, _ = arr_to_list(data2)
    copy = copyRandomList(orig)
    assert deep_equal(orig, copy), list_to_arr(copy)
    assert no_shared_nodes(orig, copy)

    # 用例3: [[3,None],[3,0],[3,None]]
    data3 = [[3, None], [3, 0], [3, None]]
    orig, _ = arr_to_list(data3)
    copy = copyRandomList(orig)
    assert list_to_arr(copy) == data3, list_to_arr(copy)
    assert no_shared_nodes(orig, copy)

    # 用例4: 空链表
    assert copyRandomList(None) is None

    # 用例5: 单节点，random 指向自身
    data5 = [[1, 0]]
    orig, nodes = arr_to_list(data5)
    copy = copyRandomList(orig)
    assert copy.val == 1
    assert copy.random is copy           # 复制节点的 random 应指向自身（复制体）
    assert copy is not orig

    print("All tests passed for copy_list_with_random!")
