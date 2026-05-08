"""
题目：寻找右区间
难度：Medium | 高频出现：字节
标签：二分查找、排序、数组
LeetCode：#436


题目描述
---------
给你一个区间数组 intervals，其中 intervals[i] = [starti, endi]，
且每个 starti 都不同。对于每个区间 i，找到满足 startj >= endi 的最小 startj 对应的区间 j。
返回一个整数数组 result，其中 result[i] 是区间 i 的"右侧区间"的下标；若不存在，则返回 -1。

示例
------
输入: intervals = [[1,2]]
输出: [-1]

输入: intervals = [[3,4],[2,3],[1,2]]
输出: [-1,0,1]

约束
------
- 1 <= intervals.length <= 2 * 10^4
- intervals[i].length == 2，0 <= starti <= endi <= 10^6

TL;DR（30秒速览）
- 将所有区间起点排序建索引，对每个区间的终点做二分查找最小起点 >= 终点
- 时间 O(n log n)，空间 O(n)
- 关键陷阱：结果要返回原始下标（非排序后下标），需用字典映射起点→原始下标

详细解析
---------
步骤：
  1. 构建 start_map：起点 → 原始区间下标（起点唯一，题目保证）
  2. 对所有起点排序，得到有序起点列表 sorted_starts
  3. 对每个区间的终点 end，在 sorted_starts 中二分查找最小的 start >= end
     - 若找到：result[i] = start_map[sorted_starts[pos]]
     - 若不存在（bisect 返回 len(sorted_starts)）：result[i] = -1

二分使用 bisect.bisect_left：找第一个 >= end 的位置。
"""

from typing import List
import bisect


def find_right_interval(intervals: List[List[int]]) -> List[int]:
    n = len(intervals)
    # 起点 → 原始下标
    start_map = {intervals[i][0]: i for i in range(n)}
    sorted_starts = sorted(start_map.keys())

    result = []
    for start, end in intervals:
        pos = bisect.bisect_left(sorted_starts, end)
        if pos < n:
            result.append(start_map[sorted_starts[pos]])
        else:
            result.append(-1)

    return result


if __name__ == "__main__":
    # [[1,2]] -> [-1]（没有起点 >= 2）
    assert find_right_interval([[1, 2]]) == [-1]

    # [[3,4],[2,3],[1,2]] -> [-1, 0, 1]
    # 区间0终点4：无起点>=4 -> -1
    # 区间1终点3：起点3(区间0) -> 0
    # 区间2终点2：起点2(区间1) -> 1... wait 起点2是区间1（索引1）
    assert find_right_interval([[3, 4], [2, 3], [1, 2]]) == [-1, 0, 1]

    # [[1,4],[2,3],[3,4]] -> [-1, 2, -1]
    assert find_right_interval([[1, 4], [2, 3], [3, 4]]) == [-1, 2, -1]

    print("All tests passed.")
