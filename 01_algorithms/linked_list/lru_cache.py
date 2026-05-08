"""
题目：LRU 缓存
难度：Medium | 高频出现：字节/腾讯/阿里
标签：哈希表、双向链表、设计题
LeetCode：#146


题目描述
---------
请你设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构。
实现 LRUCache 类：
  - LRUCache(capacity)：以正整数作为容量初始化缓存
  - get(key)：如果关键字存在于缓存中，则返回关键字的值，否则返回 -1
  - put(key, value)：插入或更新；容量满时，在插入新数据前先淘汰最久未使用的数据

get 和 put 必须以 O(1) 的平均时间复杂度运行。

示例
------
输入: ["LRUCache","put","put","get","put","get","put","get","get","get"]
      [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
输出: [null,null,null,1,null,-1,null,-1,3,4]

约束
------
- 1 <= capacity <= 3000
- 0 <= key <= 10^4，0 <= value <= 10^5

TL;DR（30秒速览）
- 思路：OrderedDict（内部是哈希+双链表），move_to_end 标记最近使用
- 时间：O(1) get/put  空间：O(capacity)
- 陷阱：put 时若 key 已存在也要 move_to_end（更新位置）

详细解析
---------
方法1 - OrderedDict（面试快速实现）：
  有序字典维护插入/访问顺序
  get: 查到则 move_to_end（最近使用）
  put: key存在则 move_to_end；不存在则插入；超容量则 popitem(last=False) 删最旧

方法2 - 手写双向链表 + 哈希表（体现原理，推荐在面试中说明）：
  链表维护顺序：head（最旧）↔ ... ↔ tail（最新）
  哈希表 key→node 实现 O(1) 查找
  每次访问/插入，把节点移到 tail 前
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)


class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = self.next = None


class LRUCacheManual:
    """手写双向链表版，便于面试展示原理"""
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head = DLinkedNode()  # dummy head（最旧端）
        self.tail = DLinkedNode()  # dummy tail（最新端）
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = DLinkedNode(key, value)
        self._add_to_tail(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]


if __name__ == "__main__":
    for LRU in [LRUCache, LRUCacheManual]:
        cache = LRU(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)       # 淘汰 key=2
        assert cache.get(2) == -1
        cache.put(4, 4)       # 淘汰 key=1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4
    print("All tests passed.")
