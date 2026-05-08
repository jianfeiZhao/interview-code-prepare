"""
LeetCode #253 - 会议室 II (Meeting Rooms II)
难度: Medium | 频率: 字节/阿里/腾讯，必考

=== 题目描述 ===
给你一个会议时间安排的数组 intervals，每个会议时间都会包括开始和结束的时间
intervals[i] = [start_i, end_i]，为避免会议冲突，同时要考虑充分利用会议室资源，
请你计算至少需要多少间会议室，才能满足这些会议安排。

示例 1: 输入: intervals = [[0,30],[5,10],[15,20]]  输出: 2
示例 2: 输入: intervals = [[7,10],[2,4]]           输出: 1

扩展: #252 会议室 I（判断能否参加所有会议，即判断是否有重叠）

=== TL;DR ===
核心思路:
  方法1（最小堆/优先队列）: 按开始时间排序，维护小顶堆存储各会议室的结束时间
    若堆顶（最早结束）<= 当前会议开始，弹出堆顶（复用该会议室）；否则堆大小+1
    — O(n log n) 时间，O(n) 空间（面试推荐）
  方法2（差分数组/扫描线）: 将开始计+1，结束计-1，前缀最大值即答案 — O(n log n)
  方法3（双指针+排序）: 开始时间和结束时间分别排序，双指针扫描 — O(n log n) O(n)

时间复杂度: O(n log n)
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. 堆法: heapq 存会议室结束时间，len(heap) = 当前会议室数
2. 注意: 结束时间 <= 开始时间时可复用（不是严格小于，因为前一个结束后立即可开始）
3. 差分/扫描线: 创建事件列表 [(time, type)]，type: +1=开始 -1=结束
   同一时刻先处理结束事件（end 排在 start 前），计算前缀最大值
4. 双指针: starts 和 ends 各排序，end_ptr 指向最早结束时间，
   若 starts[i] >= ends[end_ptr]，end_ptr 右移（复用房间）；否则需要新房间

补充 - #252 会议室I判断逻辑:
  排序后检查相邻两个区间是否重叠: intervals[i][0] < intervals[i-1][1]
"""

import heapq


# ===== 方法1: 最小堆（面试推荐）=====
def min_meeting_rooms_heap(intervals: list) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])  # 按开始时间排序
    heap = []  # 小顶堆，存各会议室的结束时间

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)  # 复用结束最早的会议室
        else:
            heapq.heappush(heap, end)     # 需要新开一间

    return len(heap)


# ===== 方法2: 扫描线/差分 =====
def min_meeting_rooms_sweep(intervals: list) -> int:
    events = []
    for start, end in intervals:
        events.append((start, 1))   # 开始: +1
        events.append((end, -1))    # 结束: -1
    # 同时刻先处理结束(−1)再处理开始(+1)，所以 key=(time, type) 升序即可
    events.sort()

    rooms = max_rooms = 0
    for _, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)
    return max_rooms


# ===== 方法3: 双指针（O(1) 额外空间思路）=====
def min_meeting_rooms_two_pointers(intervals: list) -> int:
    if not intervals:
        return 0
    starts = sorted(x[0] for x in intervals)
    ends = sorted(x[1] for x in intervals)

    rooms = 0
    end_ptr = 0
    for i in range(len(intervals)):
        if starts[i] < ends[end_ptr]:
            rooms += 1   # 需要新会议室
        else:
            end_ptr += 1  # 复用一间（end_ptr 前进）
    return rooms


# ===== 补充: #252 会议室I =====
def can_attend_meetings(intervals: list) -> bool:
    """判断能否参加所有会议（即区间之间没有重叠）"""
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([[0, 30], [5, 10], [15, 20]], 2),
        ([[7, 10], [2, 4]], 1),
        ([], 0),
        ([[1, 5]], 1),
        ([[1, 5], [2, 6], [3, 7]], 3),
        ([[1, 4], [2, 5], [7, 10]], 2),
        ([[1, 10], [2, 3], [4, 5], [6, 7]], 2),
        ([[4, 9], [4, 17], [9, 17]], 2),
        ([[1, 5], [5, 10]], 1),   # 结束时间等于开始时间，可复用
    ]

    for func in [min_meeting_rooms_heap, min_meeting_rooms_sweep, min_meeting_rooms_two_pointers]:
        for intervals, expected in cases:
            result = func([list(x) for x in intervals])
            assert result == expected, \
                f"{func.__name__}({intervals}) = {result}, expected {expected}"

    # #252 测试
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) == False
    assert can_attend_meetings([[7, 10], [2, 4]]) == True
    assert can_attend_meetings([]) == True

    print("All tests passed!")
