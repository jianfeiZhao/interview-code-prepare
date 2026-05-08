"""
题目: 任务调度器（贪心 + 堆）
LeetCode: #621 (Medium)
高频公司: 字节跳动、阿里巴巴

题目描述:
给你一个用字符数组 tasks 表示的 CPU 需要执行的任务列表，用字母 A 到 Z 表示，以及一个冷却时间 n。
每个周期或时间间隔允许完成一项任务。任务可以按任何顺序完成，但有一个限制：
两个相同种类的任务之间必须有长度为整数 n 的冷却时间。
返回完成所有任务所需要的最短时间间隔。

示例 1: tasks = ["A","A","A","B","B","B"], n = 2 -> 8
         (A -> B -> idle -> A -> B -> idle -> A -> B)
示例 2: tasks = ["A","A","A","B","B","B"], n = 0 -> 6
示例 3: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2 -> 16

================================================================================
TL;DR:

方法1 - 数学公式（O(n)，最简）:
  - 设最高频任务频率为 f_max，有 k 种任务频率为 f_max
  - 最短时间 = max(len(tasks), (f_max - 1) * (n + 1) + k)
  - (f_max-1) 个完整框架 + 最后一排 k 个最高频任务

方法2 - 贪心模拟 + 大顶堆（展示思考过程，面试更有说服力）:
  - 每轮（n+1 个时间槽）从堆中取最多 n+1 个频率最高的任务执行
  - 不够 n+1 个则补 idle，直到所有任务完成

时间复杂度: O(n) [数学公式] / O(n log n) [堆]
空间复杂度: O(1)（任务种类最多26个）
================================================================================
"""

import heapq
from collections import Counter
from typing import List


# ===================== 方法1: 数学公式 =====================

def leastInterval_math(tasks: List[str], n: int) -> int:
    """
    数学推导：
    将任务排列成如下框架（以 n=2，tasks=[A*3,B*3] 为例）:
      [A, B, idle] [A, B, idle] [A, B]
      一框 = n+1 个槽，共 f_max-1 个完整框，加上最后一行

    最高频次 f_max，有 k 种频率达到 f_max 的任务：
      最少时间 = (f_max - 1) * (n + 1) + k
    但当任务很多时，可能不需要 idle，直接 len(tasks) 就够了。
    """
    count = Counter(tasks)
    f_max = max(count.values())
    # 统计有多少种任务频率等于 f_max
    k = sum(1 for v in count.values() if v == f_max)

    return max(len(tasks), (f_max - 1) * (n + 1) + k)


# ===================== 方法2: 贪心 + 大顶堆 =====================

def leastInterval_heap(tasks: List[str], n: int) -> int:
    """
    模拟每个时间单位的调度过程：
    - 用大顶堆存储各任务剩余次数
    - 每轮从堆中最多取 n+1 个频率最高的任务（一个调度周期）
    - 若本轮可取任务不足 n+1 个，剩余时间为 idle

    为什么每轮取频率最高的？
    贪心：优先处理出现次数多的任务，减少整体等待时间。
    """
    count = Counter(tasks)
    # Python heapq 是小顶堆，取反模拟大顶堆
    max_heap = [-v for v in count.values()]
    heapq.heapify(max_heap)

    time = 0

    while max_heap:
        cycle = []       # 本轮执行的任务（最多 n+1 个）
        cycle_time = 0   # 本轮花费时间（含 idle）

        for _ in range(n + 1):
            if max_heap:
                freq = heapq.heappop(max_heap)  # 取频率最高的（存的是负值）
                cycle.append(freq + 1)           # 执行后频率 -1（负值+1）
                cycle_time += 1

        # 将本轮未执行完的任务放回堆
        for freq in cycle:
            if freq < 0:  # 还有剩余（负值未归零）
                heapq.heappush(max_heap, freq)

        # 如果堆空，本轮不需要补 idle（最后一轮可能不满 n+1 个槽）
        if max_heap:
            time += n + 1   # 完整周期
        else:
            time += cycle_time  # 最后一轮只计实际执行时间

    return time


def leastInterval_simulate(tasks: List[str], n: int) -> int:
    """
    逐时间单位模拟（更直观，但效率低，仅用于理解）。
    使用队列存储冷却中的任务，每个时间步骤：
    1. 从大顶堆取最高频任务执行
    2. 执行的任务进入冷却队列，n 步后才能重新入堆
    """
    from collections import deque

    count = Counter(tasks)
    max_heap = [(-v, k) for k, v in count.items()]
    heapq.heapify(max_heap)

    time = 0
    cooldown_queue = deque()  # (available_time, remaining_count, task)

    while max_heap or cooldown_queue:
        time += 1

        # 将冷却完成的任务放回堆
        if cooldown_queue and cooldown_queue[0][0] <= time:
            avail, remaining, task = cooldown_queue.popleft()
            heapq.heappush(max_heap, (remaining, task))

        if max_heap:
            freq, task = heapq.heappop(max_heap)
            freq += 1  # 执行一次（负值减小绝对值）
            if freq < 0:
                # 还有剩余，n 步后可用
                cooldown_queue.append((time + n + 1, freq, task))
        # else: idle

    return time


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    test_cases = [
        (["A","A","A","B","B","B"], 2, 8),
        (["A","A","A","B","B","B"], 0, 6),
        (["A","A","A","A","A","A","B","C","D","E","F","G"], 2, 16),
        (["A"], 2, 1),
        (["A","B","C"], 2, 3),              # 无需 idle
        (["A","A","A"], 2, 7),              # A -> idle -> idle -> A -> idle -> idle -> A
        (["A","A","B","B"], 2, 5),          # A -> B -> idle -> A -> B
        (["A","A","A","B","B","B","C","C","C"], 2, 9),  # 刚好无 idle
    ]

    for tasks, n, expected in test_cases:
        r1 = leastInterval_math(tasks, n)
        r2 = leastInterval_heap(tasks, n)

        assert r1 == expected, f"math: tasks={tasks}, n={n}, got={r1}, expected={expected}"
        assert r2 == expected, f"heap: tasks={tasks}, n={n}, got={r2}, expected={expected}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"[A*3,B*3], n=2: {leastInterval_math(['A','A','A','B','B','B'], 2)}")  # 8
    print(f"[A*3,B*3], n=0: {leastInterval_math(['A','A','A','B','B','B'], 0)}")  # 6
    print(f"[A*6,B,C,D,E,F,G], n=2: {leastInterval_math(['A','A','A','A','A','A','B','C','D','E','F','G'], 2)}")  # 16

    print(f"\n思路对比:")
    print(f"  数学公式: max(总任务数, (最高频-1)*(n+1)+最高频任务种类数)")
    print(f"  贪心+堆:  每轮选 n+1 个最高频任务，不足则 idle")
