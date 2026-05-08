"""
题目：基于时间的键值存储
难度：Medium | 高频出现：字节/阿里
标签：设计、二分查找、哈希表
LeetCode：#981


题目描述
---------
设计一个基于时间的键值数据结构，该结构支持在不同时间戳存储同一个键的多个值，
并针对特定时间戳检索键的值。实现 TimeMap 类：
  - set(key, value, timestamp)：存储键 key、值 value，以及给定的时间戳 timestamp
  - get(key, timestamp)：返回先前调用 set 存储的、键 key 对应的最大时间戳 ts <= timestamp 的值

示例
------
输入: ["TimeMap","set","get","get","set","get","get"]
      [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]
输出: [null,null,"bar","bar",null,"bar2","bar2"]

约束
------
- set 的 timestamp 严格递增；1 <= key.length, value.length <= 100

TL;DR（30秒速览）
- 哈希表存 key → [(timestamp, value)] 有序列表
- get：二分查找最大的 timestamp <= t
- 时间 set O(1)，get O(log n)

详细解析
---------
set 保证 timestamp 单调递增，所以列表天然有序。
get 用 bisect_right 找到 timestamp 的插入位置，
  位置-1即为最大的 <= t 的时间戳的索引。
"""

from collections import defaultdict
import bisect


class TimeMap:
    def __init__(self):
        self.data = defaultdict(list)   # key → [(timestamp, value)]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.data:
            return ""
        entries = self.data[key]
        # 找到最大 ts <= timestamp
        idx = bisect.bisect_right(entries, (timestamp, chr(127))) - 1
        if idx < 0:
            return ""
        return entries[idx][1]


if __name__ == "__main__":
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 0) == ""
    print("All tests passed.")
