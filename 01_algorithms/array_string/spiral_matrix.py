"""
题目：螺旋矩阵
难度：Medium | 高频出现：字节/腾讯/微软/亚马逊
标签：数组、矩阵、模拟
LeetCode：#54（顺时针读取）、#59（生成螺旋矩阵）

题目描述
---------
给定一个 m×n 的矩阵，按照顺时针螺旋顺序，返回矩阵中的所有元素。
即从左上角出发，依次向右、向下、向左、向上循环遍历，逐层向内收缩直到访问完所有元素。
扩展题 #59 要求生成一个填入 1~n² 的 n×n 螺旋矩阵。

示例
------
输入: matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出: [1,2,3,6,9,8,7,4,5]

输入: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出: [1,2,3,4,8,12,11,10,9,5,6,7]

约束
------
- m == matrix.length，n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

TL;DR（30秒速览）
- 思路：维护四条边界（top/bottom/left/right），每遍历一条边就收缩对应边界
- 时间：O(m*n)  空间：O(1)（输出不计）
- 陷阱：收缩边界后需判断是否越界，防止单行/单列被重复遍历

详细解析
---------
方法1：方向数组模拟
  维护方向 (dr, dc) 依次为右/下/左/上，遇边界或已访问则转向。
  需要额外 visited 数组，O(m*n) 空间。

方法2：四边界收缩（最优，推荐）：
  top=0, bottom=m-1, left=0, right=n-1。
  循环：
    ① 向右遍历 top 行：left→right，然后 top += 1
    ② 向下遍历 right 列：top→bottom，然后 right -= 1
    ③ 若 top <= bottom：向左遍历 bottom 行：right→left，然后 bottom -= 1
    ④ 若 left <= right：向上遍历 left 列：bottom→top，然后 left += 1
  步骤③④需判断，防止单行或单列被重复走。

#59 生成螺旋矩阵：逻辑相同，改为写入数字（1..n²）。
"""

from typing import List


# ---- #54 螺旋顺序读取矩阵 ----
def spiral_order(matrix: List[List[int]]) -> List[int]:
    result = []
    if not matrix:
        return result

    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # 向右
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # 向下
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # 向左（需判断是否还有行）
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # 向上（需判断是否还有列）
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


# ---- #59 生成 n×n 螺旋矩阵 ----
def generate_matrix(n: int) -> List[List[int]]:
    matrix = [[0] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            matrix[top][col] = num; num += 1
        top += 1

        for row in range(top, bottom + 1):
            matrix[row][right] = num; num += 1
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                matrix[bottom][col] = num; num += 1
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                matrix[row][left] = num; num += 1
            left += 1

    return matrix


if __name__ == "__main__":
    # #54 读取
    assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == \
           [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral_order([[1]]) == [1]
    assert spiral_order([[1, 2], [3, 4]]) == [1, 2, 4, 3]
    assert spiral_order([]) == []

    # #59 生成
    assert generate_matrix(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    assert generate_matrix(1) == [[1]]
    assert generate_matrix(4) == [
        [1,  2,  3,  4],
        [12, 13, 14,  5],
        [11, 16, 15,  6],
        [10,  9,  8,  7],
    ]

    print("All tests passed.")
