"""
题目：IPO（最大化资本）
难度：Hard | 高频出现：字节/阿里
标签：贪心、堆
LeetCode：#502

题目描述
---------
给定 n 个项目，第 i 个项目需要 capital[i] 的启动资金，完成后可获得纯利润 profits[i]。
初始资金为 w，每次选择一个可负担（所需资金 <= 当前资金）的项目完成，最多完成 k 个项目。
返回完成最多 k 个项目后能获得的最大资本。

示例
------
输入: k=2, w=0, profits=[1,2,3], capital=[0,1,1]
输出: 4  # 先做项目0赚1（资金→1），再做项目2赚3（资金→4）

输入: k=3, w=0, profits=[1,2,3], capital=[0,1,2]
输出: 6  # 依次完成三个项目

约束
------
- 1 <= k <= 10^5
- 0 <= w <= 10^9
- 1 <= len(profits) == len(capital) <= 10^5
- 0 <= profits[i] <= 10^4，0 <= capital[i] <= 10^9

TL;DR（30秒速览）
- 按资本排序，将当前可做项目的利润入最大堆，每轮选利润最大的
- 时间 O(n log n)，空间 O(n)

详细解析
---------
贪心 + 双堆：
  1. 将项目按所需资本排序
  2. 每轮：将当前资本可解锁的项目利润全部入最大堆
  3. 从堆中取利润最大的项目执行，累加资本
  4. 重复k轮
"""

from typing import List
import heapq


def find_maximized_capital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    # 按所需资本排序
    projects = sorted(zip(capital, profits))
    max_heap = []  # 存负利润（模拟最大堆）
    i = 0
    for _ in range(k):
        # 将所有当前资本可解锁的项目入堆
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(max_heap, -projects[i][1])
            i += 1
        if not max_heap:
            break
        w += -heapq.heappop(max_heap)
    return w


if __name__ == "__main__":
    assert find_maximized_capital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert find_maximized_capital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    assert find_maximized_capital(1, 0, [1, 2, 3], [1, 1, 2]) == 0  # 无法解锁任何项目
    print("All tests passed.")
