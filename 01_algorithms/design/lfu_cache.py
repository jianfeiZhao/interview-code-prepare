"""
题目：LFU 缓存
难度：Hard | 高频出现：字节/阿里/腾讯
标签：设计、哈希表、双向链表
LeetCode：#460

题目描述
---------
设计并实现一个满足 LFU（最不经常使用）缓存淘汰策略的数据结构。需支持 get 和 put 操作，
均要求 O(1) 时间复杂度。当缓存达到容量上限时，淘汰使用频率最低的 key；若有多个 key
频率相同，则淘汰其中最久未使用的那个（即 LRU 作为同频率的二次排序依据）。

示例
------
输入: capacity=2, 操作序列: put(1,1), put(2,2), get(1)→1, put(3,3)[淘汰key2], get(2)→-1
输出: get(1)=1, get(2)=-1, get(3)=3

约束
------
- 0 <= capacity <= 10^4
- 0 <= key <= 10^5，0 <= value <= 10^9
- 最多调用 2×10^5 次 get 和 put

TL;DR（30秒速览）
- 三个哈希表：key→value/freq，key→双链表节点，freq→双链表
- 维护 min_freq，O(1) get/put
- 时间 O(1)，空间 O(capacity)

详细解析
---------
数据结构：
  key_map: key → (value, freq)
  freq_map: freq → OrderedDict（按访问顺序，最久未访问在前）
  min_freq: 当前最小频率

get(key)：取值，频率+1，从旧freq桶移到新freq桶
put(key, value)：
  若已存在：更新值，频率+1
  若不存在：若满容量，删除 min_freq 桶中最久未访问的，再插入（freq=1）
"""

from collections import defaultdict, OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_map = {}        # key → [value, freq]
        self.freq_map = defaultdict(OrderedDict)  # freq → {key: None}

    def _update(self, key):
        val, freq = self.key_map[key]
        del self.freq_map[freq][key]
        if not self.freq_map[freq] and freq == self.min_freq:
            self.min_freq += 1
        freq += 1
        self.key_map[key] = [val, freq]
        self.freq_map[freq][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        self._update(key)
        return self.key_map[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_map:
            self.key_map[key][0] = value
            self._update(key)
        else:
            if len(self.key_map) >= self.capacity:
                # 删除最小频率中最久未使用的
                evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
                del self.key_map[evict_key]
            self.key_map[key] = [value, 1]
            self.freq_map[1][key] = None
            self.min_freq = 1


if __name__ == "__main__":
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1      # freq[1]=2, freq[2]=1
    cache.put(3, 3)               # 容量满，删除 freq 最小的 key=2
    assert cache.get(2) == -1     # 已被删除
    assert cache.get(3) == 3
    cache.put(4, 4)               # 容量满，删除 freq 最小的 key=3（freq=1）
    assert cache.get(1) == 1
    assert cache.get(3) == -1
    assert cache.get(4) == 4
    print("All tests passed.")
