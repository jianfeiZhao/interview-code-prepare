"""
题目：石子游戏 I & II
难度：Medium | 高频出现：字节/阿里
标签：动态规划、数学、博弈论
LeetCode：#877 石子游戏 / #1140 石子游戏 II


题目描述
---------
Alice 和 Bob 用几堆石子在做游戏。共有偶数堆石子，排成一行，每堆都有正整数颗石子。
石子的总数是奇数，所以没有平局。Alice 和 Bob 轮流进行，Alice 先开始。
每回合，玩家从行的开始或结束处取走整堆石子，游戏结束后，石子最多的人获胜。
假设 Alice 和 Bob 都发挥最佳，请你判断 Alice 是否能赢（#877）。

示例
------
输入: piles = [5,3,4,5]
输出: True  （Alice 总能赢）

约束
------
- 2 <= piles.length <= 500，piles.length 为偶数
- 1 <= piles[i] <= 500，sum(piles) 为奇数

TL;DR（30秒速览）
- #877：先手必胜（数学结论），因为总堆数为偶数，先手可控制选奇/偶位
- #1140：区间 DP，dp[i][m] 表示从第 i 堆开始、当前 M=m 时先手能多拿的最大值
- 时间 O(n^2)，空间 O(n^2)
- 关键陷阱：#1140 中 dp 表示"差值"（先手 - 后手），而非先手绝对得分

详细解析
---------
#877 数学分析：
  piles 长度为偶数。先手可以选择只取所有奇数位或所有偶数位的石子。
  Alice 先手，她可以根据奇偶位总和大小决定策略，因此先手必胜。
  → 直接 return True。

#877 DP 验证（区间 DP）：
  dp[i][j] = 在 piles[i..j] 中先手能比后手多拿的最大值。
  dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1])

#1140 变体（M 可变）：
  dp[i][m] = 从 piles[i..] 开始，当前 M=m，先手能比后手多拿多少。
  suffix[i] = piles[i..n-1] 的后缀和。
  若 2*m >= n-i（能取完剩余所有堆），dp[i][m] = suffix[i]。
  否则：dp[i][m] = max(suffix[i] - dp[i+x][max(m, x)]) for x in 1..2m。
"""

from typing import List
from functools import lru_cache


# ─────────────────────────────────────────
# #877  石子游戏 I
# ─────────────────────────────────────────
def stone_game(piles: List[int]) -> bool:
    """数学结论：先手必胜，直接返回 True"""
    return True   # 偶数堆，先手可控制奇/偶位


def stone_game_dp(piles: List[int]) -> bool:
    """DP 版本：验证先手得分 > 总分一半"""
    n = len(piles)
    # dp[i][j] = 先手在 piles[i..j] 中能获得的最大石子数
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] + (sum(piles[i+1:j+1]) - dp[i+1][j]),
                           piles[j] + (sum(piles[i:j]) - dp[i][j-1]))
    total = sum(piles)
    return dp[0][n - 1] > total // 2


# ─────────────────────────────────────────
# #1140  石子游戏 II（M 可变）
# ─────────────────────────────────────────
def stone_game_ii(piles: List[int]) -> int:
    """返回 Alice（先手）能获得的最多石子数"""
    n = len(piles)
    # 后缀和
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + piles[i]

    @lru_cache(maxsize=None)
    def dp(i: int, m: int) -> int:
        """从 piles[i..] 开始，M=m，先手能比后手多拿的最大差值"""
        if 2 * m >= n - i:
            return suffix[i]   # 能取完剩余所有
        best = 0
        for x in range(1, 2 * m + 1):
            best = max(best, suffix[i] - dp(i + x, max(m, x)))
        return best

    return dp(0, 1)


if __name__ == "__main__":
    # #877
    assert stone_game([5, 3, 4, 5]) is True
    assert stone_game([3, 7, 2, 3]) is True
    assert stone_game_dp([5, 3, 4, 5]) is True

    # #1140
    assert stone_game_ii([2, 7, 9, 4, 4]) == 10
    assert stone_game_ii([1, 2, 3, 4, 5, 100]) == 104

    print("All tests passed.")
