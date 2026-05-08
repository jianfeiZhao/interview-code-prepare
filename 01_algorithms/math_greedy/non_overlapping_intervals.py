"""
题目：无重叠区间 + 用最少数量的箭刺破气球
难度：Medium | 高频出现：字节/阿里
标签：贪心、区间调度
LeetCode：#435 无重叠区间，#452 用最少数量的箭刺破气球

题目描述
---------
给定一个区间数组 intervals，其中 intervals[i] = [start, end]。
找出需要移除的最少区间数量，使剩下的区间互不重叠（端点相邻 [1,2] 和 [2,3] 不算重叠）。
返回需要移除的最少区间数。

示例
------
输入: intervals = [[1,2],[2,3],[3,4],[1,3]]
输出: 1（移除 [1,3] 后剩余区间互不重叠）

输入: intervals = [[1,2],[1,2],[1,2]]
输出: 2（移除两个 [1,2] 后剩余一个）

约束
------
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2，-5×10^4 <= start < end <= 5×10^4

TL;DR（30秒速览）
- 贪心：按区间结束时间排序，每次选最早结束的不重叠区间
- #435 移除最少 = 总数 - 最多不重叠区间数
- #452 最少箭数 = 最多不重叠区间数（每支箭消除一组重叠区间）
- 时间 O(n log n)，空间 O(1)

详细解析
---------
区间调度最大化问题（贪心经典）：
  按结束时间升序排序，每次贪心选择结束最早的不冲突区间
  这样给后续区间留下最多空间

#452 与 #435 几乎相同，区别在于 [1,2] 和 [2,3] 的重叠定义：
  #435 中 [1,2] 和 [2,3] 不重叠（start < end）
  #452 中 [1,2] 和 [2,3] 可被同一支箭射到（start <= end）
"""

from typing import List


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    count = 1  # 保留的区间数
    end = intervals[0][1]
    for start, e in intervals[1:]:
        if start >= end:  # 不重叠
            count += 1
            end = e
    return len(intervals) - count


def find_min_arrow_shots(points: List[List[int]]) -> int:
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for start, e in points[1:]:
        if start > end:  # 注意：这里 start == end 时仍可被同一箭射到
            arrows += 1
            end = e
    return arrows


if __name__ == "__main__":
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0

    assert find_min_arrow_shots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert find_min_arrow_shots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
    assert find_min_arrow_shots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
    print("All tests passed.")
