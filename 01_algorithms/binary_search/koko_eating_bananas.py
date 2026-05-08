"""
题目：爱吃香蕉的珂珂
难度：Medium | 高频出现：字节/阿里
标签：二分查找
LeetCode：#875

题目描述
---------
珂珂有 n 堆香蕉，第 i 堆有 piles[i] 根，警卫将在 h 小时后回来。
珂珂每小时选择一堆，以速度 k（根/小时）吃，若该堆不足 k 根则全部吃完（不吃其他堆）。
返回珂珂能在 h 小时内吃完所有香蕉的最小速度 k。

示例
------
输入: piles = [3, 6, 7, 11], h = 8
输出: 4  # 速度4：ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4)=1+2+2+3=8 小时

输入: piles = [30, 11, 23, 4, 20], h = 5
输出: 30  # 堆数等于h，每堆至少花1小时，所以必须能每堆1小时内吃完

约束
------
- 1 <= len(piles) <= 10^4
- len(piles) <= h <= 10^9
- 1 <= piles[i] <= 10^9

TL;DR（30秒速览）
- 二分答案：在 [1, max(piles)] 上二分吃香蕉的速度k
- check：以速度k能否在h小时内吃完所有香蕉
- 时间 O(n log M)，M=max(piles)

详细解析
---------
每堆香蕉需要 ceil(piles[i] / k) 小时
check(k) = sum(ceil(p/k) for p in piles) <= h
二分最小可行的k
"""

import math
from typing import List


def min_eating_speed(piles: List[int], h: int) -> int:
    def can_finish(k):
        return sum(math.ceil(p / k) for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([1, 1, 1, 999999999], 10) == 142857143
    print("All tests passed.")
