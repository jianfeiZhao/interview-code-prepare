"""
题目：最长公共前缀
难度：Easy | 高频出现：字节/阿里/腾讯
标签：字符串、Trie、二分
LeetCode：#14


题目描述
---------
使用 Trie 实现查找字符串数组中最长公共前缀的功能。
编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 ""。

示例
------
输入: strs = ["flower","flow","flight"]
输出: "fl"

输入: strs = ["dog","racecar","car"]
输出: ""

约束
------
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200，strs[i] 仅由小写英文字母组成

TL;DR（30秒速览）
- 核心思路：横向扫描（逐字符串缩短前缀）最简洁；纵向扫描/Trie/二分均可
- 时间 O(S)（S=所有字符串总长），空间 O(1)
- 关键陷阱：空数组直接返回""；任意字符串为空则公共前缀为""

详细解析
---------
方法1（横向扫描）：
  - 以第一个字符串为初始前缀，逐一与后续字符串求公共前缀（Python os.path.commonprefix）
  - 每次用 while not s.startswith(prefix): prefix = prefix[:-1]

方法2（纵向扫描）：
  - 按列扫描，发现不一致则返回当前列之前的部分

方法3（二分）：
  - 对前缀长度二分，判断是否所有字符串都有该前缀

方法4（Trie）：
  - 插入所有字符串，从根一路走只有一个子节点且非末尾的路径
"""

from typing import List


# ===== 方法1：横向扫描（最简洁）=====
def longestCommonPrefixHorizontal(strs: List[str]) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


# ===== 方法2：纵向扫描 =====
def longestCommonPrefixVertical(strs: List[str]) -> str:
    if not strs:
        return ""
    for i in range(len(strs[0])):
        ch = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]


# ===== 方法3：二分 =====
def longestCommonPrefixBinary(strs: List[str]) -> str:
    if not strs:
        return ""
    min_len = min(len(s) for s in strs)

    def is_common_prefix(length):
        prefix = strs[0][:length]
        return all(s[:length] == prefix for s in strs)

    lo, hi = 0, min_len
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if is_common_prefix(mid):
            lo = mid
        else:
            hi = mid - 1

    return strs[0][:lo]


# ===== 方法4：Trie =====
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # 经过该节点的字符串数


def longestCommonPrefixTrie(strs: List[str]) -> str:
    if not strs:
        return ""
    root = TrieNode()
    n = len(strs)

    for s in strs:
        node = root
        for ch in s:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    # 从根走，只要子节点唯一且 count==n 且非终止
    prefix = []
    node = root
    while len(node.children) == 1 and not node.is_end:
        ch = next(iter(node.children))
        child = node.children[ch]
        if child.count < n:
            break
        prefix.append(ch)
        node = child

    return ''.join(prefix)


if __name__ == "__main__":
    cases = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        ([""], ""),
        (["a"], "a"),
        (["abc", "abc", "abc"], "abc"),
        (["ab", "a"], "a"),
    ]
    for strs, expected in cases:
        assert longestCommonPrefixHorizontal(strs) == expected, f"Horizontal: {strs}"
        assert longestCommonPrefixVertical(strs) == expected, f"Vertical: {strs}"
        assert longestCommonPrefixBinary(strs) == expected, f"Binary: {strs}"
        assert longestCommonPrefixTrie(strs) == expected, f"Trie: {strs}"

    print("All tests passed.")
