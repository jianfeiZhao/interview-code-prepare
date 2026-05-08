"""
题目：键值映射
难度：Medium | 高频出现：字节
标签：Trie、设计、前缀和
LeetCode：#677


题目描述
---------
实现一个 MapSum 类，支持两个方法 insert 和 sum：
  - insert(key, val)：插入 key-val 键值对，若 key 已经存在，则重置 val
  - sum(prefix)：返回所有以 prefix 为前缀的 key 的值的总和

示例
------
输入: ["MapSum","insert","sum","insert","sum"]
      [[],["apple",3],["ap"],["app",2],["ap"]]
输出: [null,null,3,null,5]

约束
------
- 1 <= key.length, prefix.length <= 50，key 和 prefix 仅由小写英文字母组成
- 1 <= val <= 1000
- 最多调用 50 次 insert 和 sum

TL;DR（30秒速览）
- 核心思路：Trie每个节点维护前缀和（sum），insert时沿路径累加/更新差值，sum直接返回末尾节点的sum
- 时间 O(L)（insert/sum），空间 O(总字符数)
- 关键陷阱：同一key再次insert时需计算新旧值的差值（delta），而非直接加新值

详细解析
---------
每个 TrieNode 存储 val_sum（所有以此为前缀的key的value之和）

insert(key, val)：
  - 计算 delta = val - old_val（old_val 是之前该 key 的值，默认0）
  - 沿路径每个节点 node.val_sum += delta

sum(prefix)：
  - 走到 prefix 末尾节点，直接返回 node.val_sum
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.val_sum = 0  # 以该前缀结尾的所有key的val之和


class MapSum:
    def __init__(self):
        self.root = TrieNode()
        self.key_val = {}  # 记录每个key当前的val

    def insert(self, key: str, val: int) -> None:
        delta = val - self.key_val.get(key, 0)
        self.key_val[key] = val
        node = self.root
        node.val_sum += delta
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.val_sum += delta

    def sum(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.val_sum


if __name__ == "__main__":
    ms = MapSum()
    ms.insert("apple", 3)
    assert ms.sum("ap") == 3
    ms.insert("app", 2)
    assert ms.sum("ap") == 5

    # 覆盖更新
    ms.insert("apple", 5)  # 更新 apple 从 3 -> 5，delta=2
    assert ms.sum("ap") == 7  # app(2) + apple(5)
    assert ms.sum("apple") == 5

    # 不存在的前缀
    assert ms.sum("b") == 0
    assert ms.sum("appl") == 5

    # 重新设置为0
    ms.insert("app", 0)
    assert ms.sum("ap") == 5  # 只有 apple(5)

    print("All tests passed.")
