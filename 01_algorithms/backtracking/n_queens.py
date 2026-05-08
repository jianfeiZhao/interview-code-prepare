"""
题目: N 皇后（经典回溯）
LeetCode: #51 (Hard)
高频公司: 字节跳动、阿里巴巴

题目描述:
按照国际象棋的规则，皇后可以攻击与之处在同一行、列或斜线上的棋子。
n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
给你一个整数 n，返回所有不同的 n 皇后问题的解决方案。

每一种解法包含一个不同的 n 皇后问题的棋子放置方案，
该方案中 'Q' 和 '.' 分别代表皇后和空位。

示例: n = 4 ->
  [[".Q..","...Q","Q...","..Q."],
   ["..Q.","Q...","...Q",".Q.."]]

================================================================================
TL;DR（核心思路）:
- 逐行放置皇后（行自动不冲突），用集合记录已占用的列和对角线
- 对角线检测：主对角线 row-col 相同，副对角线 row+col 相同
- 每行尝试每列，合法则放置并递归下一行，回溯时撤销
- 时间 O(n!)，空间 O(n)
================================================================================"""

from typing import List


def solve_n_queens(n: int) -> List[List[str]]:
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            board[row][col] = 'Q'
            backtrack(row + 1)
            board[row][col] = '.'
            cols.discard(col); diag1.discard(row - col); diag2.discard(row + col)

    backtrack(0)
    return result


def total_n_queens(n: int) -> int:
    """#52：只返回方案数"""
    return len(solve_n_queens(n))


if __name__ == "__main__":
    solutions = solve_n_queens(4)
    assert len(solutions) == 2, f"n=4 应有2个解，got {len(solutions)}"

    # 验证解的合法性
    for sol in solutions:
        n = len(sol)
        cols_used = set()
        d1_used = set()
        d2_used = set()
        for r, row in enumerate(sol):
            c = row.index('Q')
            assert c not in cols_used, "列冲突"
            assert (r - c) not in d1_used, "主对角线冲突"
            assert (r + c) not in d2_used, "副对角线冲突"
            cols_used.add(c)
            d1_used.add(r - c)
            d2_used.add(r + c)

    assert total_n_queens(1) == 1
    assert total_n_queens(4) == 2
    assert total_n_queens(5) == 10
    assert total_n_queens(6) == 4
    assert total_n_queens(8) == 92

    print("所有测试通过!")
    print(f"\nn=4 的两个解:")
    for sol in solve_n_queens(4):
        for row in sol:
            print(f"  {row}")
        print()
