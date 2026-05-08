"""
题目：合并区间
难度：Medium | 高频出现：字节/阿里/腾讯/微软
标签：数组、排序、区间
LeetCode：#56


题目描述
---------
以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi]。
请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。

示例
------
输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
输出: [[1,6],[8,10],[15,18]]

输入: intervals = [[1,4],[4,5]]
输出: [[1,5]]

约束
------
- 1 <= intervals.length <= 10^4
- 0 <= starti <= endi <= 10^4

TL;DR（30秒速览）
- 思路：按左端点排序，维护当前合并区间，若下一个区间左端点 <= 当前右端点则合并
- 时间：O(n log n)  空间：O(n)（输出）
- 陷阱：排序后仍需注意合并时取 max(cur_end, next_end)，而不是直接替换

详细解析
---------
核心观察：排序后，所有可合并的区间一定是连续的。

算法步骤：
  1. 按区间起点排序。
  2. 初始化 merged = [intervals[0]]。
  3. 遍历剩余区间 [start, end]：
       - 若 start <= merged[-1][1]（有重叠或相邻），则合并：
         merged[-1][1] = max(merged[-1][1], end)。
       - 否则直接追加新区间。
  4. 返回 merged。

常见变题：
  - #57 插入区间：先找插入位置，再合并（O(n) 无需排序）。
  - #252/#253 会议室：判断区间是否有重叠，最少会议室数量（扫描线/堆）。
"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            # 有重叠，扩展右端点
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# 进阶：插入区间 #57
def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    result = []
    i, n = 0, len(intervals)

    # 添加所有在 new_interval 左侧的区间
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # 合并所有与 new_interval 重叠的区间
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # 添加剩余区间
    result.extend(intervals[i:])
    return result


if __name__ == "__main__":
    # #56 合并区间
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge([[1, 4], [2, 3]]) == [[1, 4]]
    assert merge([[1, 4]]) == [[1, 4]]
    assert merge([]) == []

    # #57 插入区间
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == \
           [[1, 2], [3, 10], [12, 16]]
    assert insert([], [5, 7]) == [[5, 7]]

    print("All tests passed.")
