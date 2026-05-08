"""
题目：直线上最多的点数
难度：Hard | 高频出现：字节/阿里
标签：哈希表、数学、几何
LeetCode：#149


题目描述
---------
给你一个数组 points，其中 points[i] = [xi, yi] 表示 X-Y 平面上的一个点。
求最多有多少个点在同一条直线上。

示例
------
输入: points = [[1,1],[2,2],[3,3]]
输出: 3

输入: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
输出: 4

约束
------
- 1 <= points.length <= 300
- points[i].length == 2，-10^4 <= xi, yi <= 10^4
- 所有点互不相同

TL;DR（30秒速览）
- 枚举每个点作为基准点，用斜率哈希统计共线最多点数
- 时间 O(n^2)，空间 O(n)
- 关键陷阱：斜率用最简分数 (dy/gcd, dx/gcd) 表示避免浮点误差；重合点单独计数

详细解析
---------
对每个基准点 i，遍历 j > i 的所有点：
  若重合（同一坐标），overlap += 1
  否则计算斜率 (dy, dx)，化简为最简形式后作为哈希 key
    - 约定 dx >= 0（统一方向），dx == 0 时 dy = 1
    - slope_dict[key] += 1

以 i 为基准时最多共线点数 = max(slope_dict.values()) + overlap + 1（+1 是基准点本身）
全局答案取最大值。

时间分析：外层 O(n)，内层 O(n)，gcd O(log max_val)，总体 O(n^2 log C)。
"""

from typing import List
from collections import defaultdict
from math import gcd


def max_points(points: List[List[int]]) -> int:
    n = len(points)
    if n <= 2:
        return n

    ans = 2

    for i in range(n):
        slope_dict: dict = defaultdict(int)
        overlap = 0   # 与基准点 i 重合的点数

        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]

            if dx == 0 and dy == 0:
                overlap += 1
                continue

            # 化简为最简分数，统一符号（dx >= 0）
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0:          # 统一方向：让分母非负
                dx, dy = -dx, -dy
            elif dx == 0:
                dy = abs(dy)    # 垂直线统一为正方向

            slope_dict[(dx, dy)] += 1

        local_max = max(slope_dict.values(), default=0)
        ans = max(ans, local_max + overlap + 1)

    return ans


if __name__ == "__main__":
    assert max_points([[1, 1], [2, 2], [3, 3]]) == 3
    assert max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4
    assert max_points([[0, 0]]) == 1
    assert max_points([[0, 0], [1, 1]]) == 2
    # 重合点测试
    assert max_points([[0, 0], [0, 0], [1, 1]]) == 3

    print("All tests passed.")
