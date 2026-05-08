"""
题目：矩阵置零
难度：Medium | 高频出现：字节/阿里/腾讯
标签：数组、矩阵、原地算法
LeetCode：#73


题目描述
---------
给定一个 m x n 的矩阵，如果一个元素为 0，则将其所在行和列的所有元素都设为 0。
请使用原地算法，尽量将空间复杂度降低至 O(1)。

示例
------
输入: matrix = [[1,1,1],[1,0,1],[1,1,1]]
输出: [[1,0,1],[0,0,0],[1,0,1]]

输入: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
输出: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

约束
------
- m == matrix.length，n == matrix[0].length
- 1 <= m, n <= 200
- -2^31 <= matrix[i][j] <= 2^31 - 1

TL;DR（30秒速览）
- 思路：用第一行/第一列作为标记数组，O(1) 额外空间原地完成
- 时间：O(m*n)  空间：O(1)
- 陷阱：第一行/第一列本身是否含 0 需提前单独记录，否则会互相干扰

详细解析
---------
方法1：额外 O(m+n) 空间
  扫描矩阵，记录哪些行/列需要置零，再次扫描置零。简单但不满足 O(1) 要求。

方法2：两次扫描标记 O(1) 空间（原地，推荐）：
  思路：用矩阵的第一行和第一列充当"标记行/列"。
  步骤：
    ① 先判断第一行/第一列自身是否含 0（用两个 bool 变量记录）。
    ② 遍历 matrix[i][j]（i>=1, j>=1），若为 0，则置 matrix[i][0]=0 和 matrix[0][j]=0。
    ③ 再次遍历 matrix[i][j]（i>=1, j>=1），若 matrix[i][0]==0 或 matrix[0][j]==0，置零。
    ④ 根据步骤①的记录，处理第一行和第一列。

  关键顺序：第④步必须在第③步之后，否则第一行/列的标记已被改写。
"""

from typing import List
import copy


def set_zeroes(matrix: List[List[int]]) -> None:
    """原地置零，不返回值。"""
    m, n = len(matrix), len(matrix[0])

    # 提前记录第一行/第一列是否含 0
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # 用第一行/列标记其余行/列
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # 根据标记置零（不含第一行/列）
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # 处理第一行
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    # 处理第一列
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


# 纯函数版方便测试
def set_zeroes_pure(matrix: List[List[int]]) -> List[List[int]]:
    mat = copy.deepcopy(matrix)
    set_zeroes(mat)
    return mat


if __name__ == "__main__":
    assert set_zeroes_pure([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == \
           [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    assert set_zeroes_pure([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]) == \
           [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    assert set_zeroes_pure([[1]]) == [[1]]
    assert set_zeroes_pure([[0]]) == [[0]]

    # 第一行含 0 的边界情况
    assert set_zeroes_pure([[0, 1], [1, 1]]) == [[0, 0], [0, 1]]

    # 第一列含 0 的边界情况
    assert set_zeroes_pure([[1, 1], [0, 1]]) == [[0, 1], [0, 0]]

    print("All tests passed.")
