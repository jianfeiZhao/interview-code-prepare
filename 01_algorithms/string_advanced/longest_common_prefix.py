"""
LeetCode #14 - 最长公共前缀 (Longest Common Prefix)
难度: Easy | 频率: 全系

=== 题目描述 ===
编写一个函数来查找字符串数组中的最长公共前缀。
如果不存在公共前缀，返回空字符串 ""。

示例 1:
  输入: strs = ["flower","flow","flight"]
  输出: "fl"

示例 2:
  输入: strs = ["dog","racecar","car"]
  输出: ""（没有公共前缀）

提示: 1 <= strs.length <= 200，0 <= strs[i].length <= 200，仅含小写英文字母

=== TL;DR ===
核心思路:
  方法1（横向扫描）: 以第一个字符串为基准，逐一和后续字符串求公共前缀
  方法2（纵向扫描）: 逐列比较所有字符串的同一位置字符，遇到不一致立即停止（面试最清晰）
  方法3（排序）: 只需比较排序后第一个和最后一个字符串的公共前缀
  方法4（分治）: 分成两半各求公共前缀再合并

时间复杂度: O(m*n)，m 为最短字符串长度，n 为字符串个数
空间复杂度: O(1)（排序方法 O(n log n) 时间，O(1) 额外空间）

=== 详细解析 ===
关键技巧:
1. 纵向扫描: 外层循环列索引 j，内层循环每个字符串，发现不匹配或越界则返回 s[:j]
2. 排序方法: 字符串排序后，最长公共前缀只可能是字典序最小和最大字符串的公共前缀
   因为中间字符串一定包含两端的公共前缀
3. os.path.commonprefix 可直接调用（了解即可，面试不要用）
4. 注意空数组边界处理
"""

import os


# ===== 方法1: 横向扫描 =====
def longest_common_prefix_horizontal(strs: list) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        # 逐步缩短 prefix 直到是 s 的前缀
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


# ===== 方法2: 纵向扫描（面试推荐，最清晰）=====
def longest_common_prefix_vertical(strs: list) -> str:
    if not strs:
        return ""
    for j in range(len(strs[0])):
        c = strs[0][j]
        for s in strs[1:]:
            if j >= len(s) or s[j] != c:
                return strs[0][:j]
    return strs[0]


# ===== 方法3: 排序后比较首尾 =====
def longest_common_prefix_sort(strs: list) -> str:
    if not strs:
        return ""
    strs_sorted = sorted(strs)
    first, last = strs_sorted[0], strs_sorted[-1]
    i = 0
    while i < len(first) and i < len(last) and first[i] == last[i]:
        i += 1
    return first[:i]


# ===== 方法4: 分治 =====
def longest_common_prefix_divide(strs: list) -> str:
    def common(s1: str, s2: str) -> str:
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[:i]

    def solve(lo: int, hi: int) -> str:
        if lo == hi:
            return strs[lo]
        mid = (lo + hi) // 2
        left = solve(lo, mid)
        right = solve(mid + 1, hi)
        return common(left, right)

    if not strs:
        return ""
    return solve(0, len(strs) - 1)


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [
        longest_common_prefix_horizontal,
        longest_common_prefix_vertical,
        longest_common_prefix_sort,
        longest_common_prefix_divide,
    ]
    for func in funcs:
        assert func(["flower", "flow", "flight"]) == "fl"
        assert func(["dog", "racecar", "car"]) == ""
        assert func(["a"]) == "a"
        assert func([""]) == ""
        assert func(["abc", "abc", "abc"]) == "abc"
        assert func(["ab", "a"]) == "a"
        assert func(["", "b"]) == ""
        assert func(["flower", "flower", "flower"]) == "flower"
        assert func(["c", "acc", "ccc"]) == ""

    # 使用标准库验证
    assert os.path.commonprefix(["flower", "flow", "flight"]) == "fl"

    print("All tests passed!")
