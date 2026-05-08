"""
题目: 解数独
LeetCode: #37 (Hard)
高频公司: 字节跳动

题目描述:
编写一个程序，通过填充空格来解决数独问题。
数独的解法需 遵循如下规则：
1. 数字 1-9 在每一行只能出现一次。
2. 数字 1-9 在每一列只能出现一次。
3. 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
空白格用 '.' 表示。

注意：题目保证输入数独仅有一个解。

================================================================================
TL;DR（核心思路）:
- 回溯：逐格遍历，遇到 '.' 尝试填入 1-9
- 合法性检查：行、列、3x3 宫内无重复
- 用三组集合预先记录已用数字，O(1) 检查
- 填入后递归下一格，失败则撤销（回溯）
- 剪枝优化：可优先选约束最多（候选数最少）的格子（MRV 启发式）

时间复杂度: O(9^m)，m 为空格数，实际因约束极小
空间复杂度: O(81) = O(1)
================================================================================
"""

from typing import List


def solveSudoku(board: List[List[str]]) -> None:
    """
    原地修改数独棋盘。
    使用行/列/宫三组集合加速合法性检验。
    """
    rows  = [set() for _ in range(9)]   # rows[i]: 第 i 行已有数字
    cols  = [set() for _ in range(9)]   # cols[j]: 第 j 列已有数字
    boxes = [set() for _ in range(9)]   # boxes[k]: 第 k 个 3x3 宫已有数字

    empty_cells = []  # 待填空格列表

    # 初始化：读取已有数字
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != '.':
                box_idx = (r // 3) * 3 + (c // 3)
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_idx].add(val)
            else:
                empty_cells.append((r, c))

    def backtrack(idx: int) -> bool:
        """
        尝试填写 empty_cells[idx] 位置。
        返回 True 表示找到合法解。
        """
        if idx == len(empty_cells):
            return True  # 所有空格填完，找到解

        r, c = empty_cells[idx]
        box_idx = (r // 3) * 3 + (c // 3)

        for digit in "123456789":
            # 合法性检查：行、列、宫均未使用
            if digit in rows[r] or digit in cols[c] or digit in boxes[box_idx]:
                continue

            # 填入数字
            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box_idx].add(digit)

            if backtrack(idx + 1):
                return True  # 后续均成功，直接返回

            # 回溯：撤销填入
            board[r][c] = '.'
            rows[r].discard(digit)
            cols[c].discard(digit)
            boxes[box_idx].discard(digit)

        return False  # 所有数字都不合法

    backtrack(0)


def is_valid_sudoku(board: List[List[str]]) -> bool:
    """验证数独棋盘是否合法（用于测试验证解的正确性）。"""
    for i in range(9):
        row_vals = [board[i][j] for j in range(9) if board[i][j] != '.']
        col_vals = [board[j][i] for j in range(9) if board[j][i] != '.']
        if len(row_vals) != len(set(row_vals)):
            return False
        if len(col_vals) != len(set(col_vals)):
            return False

    for br in range(3):
        for bc in range(3):
            box_vals = [
                board[br*3+r][bc*3+c]
                for r in range(3) for c in range(3)
                if board[br*3+r][bc*3+c] != '.'
            ]
            if len(box_vals) != len(set(box_vals)):
                return False

    # 所有格子已填满
    return all(board[r][c] != '.' for r in range(9) for c in range(9))


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 标准测试用例
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]

    solveSudoku(board)

    assert is_valid_sudoku(board), "解不合法"

    expected = [
        ["5","3","4","6","7","8","9","1","2"],
        ["6","7","2","1","9","5","3","4","8"],
        ["1","9","8","3","4","2","5","6","7"],
        ["8","5","9","7","6","1","4","2","3"],
        ["4","2","6","8","5","3","7","9","1"],
        ["7","1","3","9","2","4","8","5","6"],
        ["9","6","1","5","3","7","2","8","4"],
        ["2","8","7","4","1","9","6","3","5"],
        ["3","4","5","2","8","6","1","7","9"]
    ]
    assert board == expected, f"答案不正确"

    print("所有测试通过!")
    print("\n解题结果:")
    for row in board:
        print("  " + " ".join(row))
