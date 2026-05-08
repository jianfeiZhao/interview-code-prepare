"""
题目：合并区间 + 插入区间
难度：Medium | 高频出现：字节/阿里/腾讯
标签：贪心、区间
LeetCode：#56 合并区间，#57 插入区间


题目描述
---------
#56 合并区间：以数组 intervals 表示若干区间，合并所有重叠区间后返回不重叠的区间数组。

#57 插入区间：给你一个无重叠的区间列表 intervals（已按起点升序排列）及一个新区间 newInterval，
请你将 newInterval 插入到列表中，使得列表仍保持有序且无重叠（必要时合并区间）。

示例
------
#56 输入: [[1,3],[2,6],[8,10],[15,18]]  输出: [[1,6],[8,10],[15,18]]
#57 输入: intervals=[[1,3],[6,9]], newInterval=[2,5]  输出: [[1,5],[6,9]]

约束
------
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2，0 <= start <= end <= 10^4

TL;DR（30秒速览）
- #56：排序后按起点扫描，合并重叠区间，O(n log n)
- #57：找到插入位置并合并，O(n)
- 关键：重叠条件 new_start <= cur_end

详细解析
---------
#56 合并区间：
  按起点排序，遍历时若当前区间起点 <= 结果末尾区间的终点，则合并（取max终点）
  否则直接追加

#57 插入区间：
  三段：完全在新区间左侧 → 与新区间重叠合并 → 完全在右侧
"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort()
    result = []
    for start, end in intervals:
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    result = []
    i, n = 0, len(intervals)
    ns, ne = new_interval

    # 完全在新区间左侧
    while i < n and intervals[i][1] < ns:
        result.append(intervals[i])
        i += 1

    # 与新区间重叠，合并
    while i < n and intervals[i][0] <= ne:
        ns = min(ns, intervals[i][0])
        ne = max(ne, intervals[i][1])
        i += 1
    result.append([ns, ne])

    # 完全在右侧
    while i < n:
        result.append(intervals[i])
        i += 1
    return result


if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge([[1, 4], [0, 4]]) == [[0, 4]]

    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert insert([], [5, 7]) == [[5, 7]]
    print("All tests passed.")
