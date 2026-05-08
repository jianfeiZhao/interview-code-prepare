"""
题目: 搜索二维矩阵 I + II
LeetCode: #74 (Medium) + #240 (Medium)
高频公司: 字节跳动、腾讯

========== 题目 I (#74) ==========
编写一个高效的算法来判断 m x n 矩阵中，是否存在一个目标值。该矩阵具有如下特性：
- 每行中的整数从左到右按升序排列
- 每行的第一个整数大于前一行的最后一个整数（即整个矩阵展开是一个有序数组）

示例: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3 -> True

========== 题目 II (#240) ==========
编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target。该矩阵具有以下特性：
- 每行的元素从左到右升序排列
- 每列的元素从上到下升序排列
（注意：不保证行末 < 下行行首，条件比 #74 更弱）

示例: matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 5 -> True

================================================================================

题目描述
---------
#74：编写一个高效算法搜索 m x n 矩阵 matrix 中的一个目标值 target。
矩阵特性：每行从左到右升序，每行第一个数大于上一行最后一个数（展开后是有序数组）。

#240：搜索 m x n 矩阵，矩阵特性更弱：
  - 每行的元素从左到右升序
  - 每列的元素从上到下升序
  - 不保证行末 < 下行行首

示例
------
#74 输入: matrix=[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3  输出: True
#240 输入: matrix=[[1,4,7,11],[2,5,8,12],[3,6,9,16]], target=5       输出: True

约束
------
- m == matrix.length，n == matrix[i].length
- 1 <= m, n <= 300，-10^9 <= matrix[i][j], target <= 10^9

TL;DR:

#74 核心思路: 将矩阵映射为一维有序数组做二分
  - index -> (index // n, index % n)，在 [0, m*n) 上做标准二分
  时间: O(log(m*n))，空间: O(1)

#240 核心思路: 从右上角（或左下角）出发，利用双向有序性剪枝
  - 从右上角 (0, n-1) 开始：
    * 当前值 > target：左移（列--）排除整列
    * 当前值 < target：下移（行++）排除整行
    * 当前值 == target：找到
  时间: O(m+n)，空间: O(1)
================================================================================
"""

from typing import List


# ===================== 题目 I: #74 =====================

def searchMatrix_74(matrix: List[List[int]], target: int) -> bool:
    """
    矩阵 I：每行有序且行末 < 下行行首，等价于一维有序数组。
    用整数二分直接映射。
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        # 将一维下标映射回二维坐标
        row, col = mid // n, mid % n
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


# ===================== 题目 II: #240 =====================

def searchMatrix_240(matrix: List[List[int]], target: int) -> bool:
    """
    矩阵 II：每行、每列分别有序，从右上角出发利用双向单调性。

    为什么选右上角？
    - 它是当前行最大值（向左减小）
    - 它是当前列最小值（向下增大）
    - 因此可以根据与 target 的比较唯一决定移动方向
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # 从右上角开始

    while row < m and col >= 0:
        val = matrix[row][col]
        if val == target:
            return True
        elif val > target:
            col -= 1  # 当前值太大，左移排除整列
        else:
            row += 1  # 当前值太小，下移排除整行

    return False


def searchMatrix_240_bottomleft(matrix: List[List[int]], target: int) -> bool:
    """
    同样从左下角出发（等价思路）。
    - 左下角是当前列最大值（向上减小）
    - 左下角是当前行最小值（向右增大）
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = m - 1, 0  # 从左下角开始

    while row >= 0 and col < n:
        val = matrix[row][col]
        if val == target:
            return True
        elif val > target:
            row -= 1  # 当前值太大，上移排除整行
        else:
            col += 1  # 当前值太小，右移排除整列

    return False


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # ---- 题目 I 测试 ----
    mat74 = [
        [1,  3,  5,  7],
        [10, 11, 16, 20],
        [23, 30, 34, 60]
    ]
    assert searchMatrix_74(mat74, 3) == True
    assert searchMatrix_74(mat74, 13) == False
    assert searchMatrix_74([[1]], 1) == True
    assert searchMatrix_74([[1]], 2) == False
    assert searchMatrix_74([], 1) == False
    assert searchMatrix_74([[1, 3, 5]], 5) == True   # 单行
    assert searchMatrix_74([[1], [3], [5]], 3) == True  # 单列

    # ---- 题目 II 测试 ----
    mat240 = [
        [1,  4,  7,  11, 15],
        [2,  5,  8,  12, 19],
        [3,  6,  9,  16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    assert searchMatrix_240(mat240, 5) == True
    assert searchMatrix_240(mat240, 20) == False
    assert searchMatrix_240(mat240, 1) == True    # 左上角
    assert searchMatrix_240(mat240, 30) == True   # 右下角
    assert searchMatrix_240(mat240, 15) == True   # 右上角
    assert searchMatrix_240(mat240, 18) == True   # 左下角
    assert searchMatrix_240([[1]], 1) == True
    assert searchMatrix_240([[1]], 2) == False

    # 两种 #240 实现结果一致
    test_targets = [5, 20, 1, 30, 15, 18, 100]
    for t in test_targets:
        r1 = searchMatrix_240(mat240, t)
        r2 = searchMatrix_240_bottomleft(mat240, t)
        assert r1 == r2, f"两种实现结果不一致: target={t}"

    print("所有测试通过!")

    print(f"\n=== 题目 I 示例 ===")
    print(f"matrix74, target=3: {searchMatrix_74(mat74, 3)}")    # True
    print(f"matrix74, target=13: {searchMatrix_74(mat74, 13)}")  # False

    print(f"\n=== 题目 II 示例 ===")
    print(f"matrix240, target=5: {searchMatrix_240(mat240, 5)}")   # True
    print(f"matrix240, target=20: {searchMatrix_240(mat240, 20)}") # False
