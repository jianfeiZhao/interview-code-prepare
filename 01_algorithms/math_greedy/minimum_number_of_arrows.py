"""
题目：用最少数量的箭刺破气球
难度：Medium | 高频出现：字节/阿里
标签：贪心、区间、排序
LeetCode：#452

题目描述
---------
在二维空间中有若干个气球，每个气球的水平范围为闭区间 [x_start, x_end]。
从 x 轴任意位置垂直向上射出一支箭，能刺破所有水平范围覆盖该 x 坐标的气球。
给定所有气球的区间列表 points，返回刺破全部气球所需的最少箭数。

示例
------
输入: points = [[10,16],[2,8],[1,6],[7,12]]
输出: 2（在 x=6 射一箭刺破 [2,8][1,6]，在 x=11 射一箭刺破 [10,16][7,12]）

输入: points = [[1,2],[3,4],[5,6],[7,8]]
输出: 4（4个区间互不重叠，各需一箭）

约束
------
- 1 <= points.length <= 10^5
- points[i].length == 2，-2^31 <= x_start <= x_end <= 2^31 - 1

TL;DR（30秒速览）
- 按区间右端点排序，贪心：每次在右端点射箭，尽可能多刺穿后续气球
- 时间 O(n log n)，空间 O(1)
- 关键陷阱：气球区间 [x_start, x_end] 是闭区间（端点也算爆破），注意边界判断

详细解析
---------
贪心策略：
  按右端点从小到大排序。
  维护当前箭的位置 arrow = -inf（初始未射箭）。
  对每个气球 [start, end]：
    若 start > arrow（当前箭无法刺破此气球）：
      必须在此气球右端点射一箭：arrow = end，arrows += 1
    否则，当前箭已可刺破此气球（start <= arrow <= end），不需要新箭。

为什么选右端点？
  尽可能靠右射箭，使得更多后续气球（左端点更靠右）也能被这支箭刺破。
  这是区间调度问题的经典贪心。

与 #435（无重叠区间）的关系：
  #452 的答案 = n - (#435 中保留的不重叠区间数)
  实际上两题的贪心逻辑几乎完全相同。
"""

from typing import List


def find_min_arrow_shots(points: List[List[int]]) -> int:
    if not points:
        return 0

    # 按右端点排序
    points.sort(key=lambda x: x[1])

    arrows = 1
    arrow_pos = points[0][1]   # 第一箭射在第一个气球右端点

    for start, end in points[1:]:
        if start > arrow_pos:      # 当前箭无法刺破此气球
            arrows += 1
            arrow_pos = end        # 新箭射在此气球右端点
        # else: 当前箭已能刺破（start <= arrow_pos <= end），不需要新箭

    return arrows


# 方法二：按左端点排序（等价，但逻辑需略作调整）
def find_min_arrow_shots_v2(points: List[List[int]]) -> int:
    """按左端点排序，维护当前可被同一箭刺穿区间的最小右端点"""
    if not points:
        return 0

    points.sort(key=lambda x: x[0])

    arrows = 1
    min_right = points[0][1]   # 当前箭能覆盖的最小右端点（即公共交集右边界）

    for start, end in points[1:]:
        if start > min_right:      # 与已有区间无交集，需要新箭
            arrows += 1
            min_right = end
        else:
            min_right = min(min_right, end)   # 缩小公共交集

    return arrows


if __name__ == "__main__":
    assert find_min_arrow_shots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert find_min_arrow_shots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
    assert find_min_arrow_shots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
    assert find_min_arrow_shots([[1, 2]]) == 1
    assert find_min_arrow_shots([[-2147483646, -2147483645], [2147483646, 2147483647]]) == 2

    assert find_min_arrow_shots_v2([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert find_min_arrow_shots_v2([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
    assert find_min_arrow_shots_v2([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2

    print("All tests passed.")
