"""
买卖股票最佳时机 I ~ VI
LeetCode #121 (Easy) / #122 (Medium) / #123 (Hard) /
         #188 (Hard) / #309 (Medium) / #714 (Medium)
高频考点: 全系大厂必考系列

题目描述
---------
股票买卖系列：给定股票每天价格数组 prices，在不同交易次数限制下求最大利润。
#121 最多 1 次；#122 不限次数；#123 最多 2 次；#188 最多 k 次；
#309 不限次数但卖后有 1 天冷冻期；#714 不限次数但每笔交易需支付手续费 fee。
每次买入前必须卖出（不能同时持有多只股票）。

示例
------
输入: prices = [7, 1, 5, 3, 6, 4]  (#121, 最多1次)
输出: 5  # 第2天买入(1)，第5天卖出(6)，利润=5

输入: prices = [1, 3, 2, 8, 4, 9], fee = 2  (#714)
输出: 8  # 两笔交易扣除手续费后最大利润

约束
------
- 1 <= len(prices) <= 10^5
- 0 <= prices[i] <= 10^4
- #188: 0 <= k <= 10^9；#714: 0 <= fee <= 5 * 10^4

============================================================
TL;DR
============================================================
通用 DP 状态机框架:
  dp[i][k][hold] = 第 i 天，已完成交易 k 次，是否持有股票时的最大利润
  hold=0（不持有）: dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
  hold=1（持有）:   dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])

各变体化简:
  #121 k=1:      买入时 dp[i-1][k-1][0]=dp[i-1][0][0]=0，可化简为贪心
  #122 k=∞:      k 约束消失，等价于每涨必吃
  #123 k=2:      状态压缩到 buy1,sell1,buy2,sell2 四变量
  #188 k=任意:   k >= n/2 时等价于 k=∞；否则用二维 DP
  #309 冷冻期:   卖出后下一天不能买入 → dp[i][1] 依赖 dp[i-2][0]
  #714 手续费:   卖出时扣 fee，等价于降低卖出所得
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# #121 最多 1 次交易（贪心）
# ─────────────────────────────────────────────
def max_profit_i(prices: List[int]) -> int:
    """
    贪心：枚举卖出点，记录到当前为止的最低买入价。
    时间: O(n)，空间: O(1)
    """
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit


# ─────────────────────────────────────────────
# #122 不限次数交易（贪心）
# ─────────────────────────────────────────────
def max_profit_ii(prices: List[int]) -> int:
    """
    贪心：每段上涨区间都吃进（相邻两天差值为正就累加）。
    等价于：持有时每天都"卖出再买入"的虚拟操作。
    时间: O(n)，空间: O(1)
    """
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))


# ─────────────────────────────────────────────
# #123 最多 2 次交易（状态压缩 DP）
# ─────────────────────────────────────────────
def max_profit_iii(prices: List[int]) -> int:
    """
    四个状态变量模拟两笔交易的最优决策。
    buy1  = 第一次买入后的最大利润（负值）
    sell1 = 第一次卖出后的最大利润
    buy2  = 第二次买入后的最大利润（利用 sell1 的收益）
    sell2 = 第二次卖出后的最大利润 = 最终答案
    时间: O(n)，空间: O(1)
    """
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    for p in prices:
        buy1 = max(buy1, -p)                # 第一次买：付出 p
        sell1 = max(sell1, buy1 + p)        # 第一次卖：收回 p
        buy2 = max(buy2, sell1 - p)         # 第二次买：利用第一笔利润
        sell2 = max(sell2, buy2 + p)        # 第二次卖：最终收益
    return sell2


# ─────────────────────────────────────────────
# #188 最多 k 次交易
# ─────────────────────────────────────────────
def max_profit_iv(k: int, prices: List[int]) -> int:
    """
    k >= n//2 时等同于无限次交易（一次交易至少需要 2 天）。
    否则用二维 DP：dp[t][i] = 最多 t 次交易、第 i 天结束时的最大利润。
    时间: O(k * n)，空间: O(k * n)（可压缩至 O(n)）
    """
    n = len(prices)
    if not prices or k == 0:
        return 0
    if k >= n // 2:
        return max_profit_ii(prices)

    dp = [[0] * n for _ in range(k + 1)]
    for t in range(1, k + 1):
        max_so_far = -prices[0]  # 等价于 dp[t-1][i-1] - prices[i] 的最大值
        for i in range(1, n):
            dp[t][i] = max(dp[t][i - 1], prices[i] + max_so_far)
            max_so_far = max(max_so_far, dp[t - 1][i] - prices[i])
    return dp[k][n - 1]


# ─────────────────────────────────────────────
# #309 含冷冻期（不限次数）
# ─────────────────────────────────────────────
def max_profit_with_cooldown(prices: List[int]) -> int:
    """
    三状态 DP：
      hold  = 当前持有股票的最大利润
      sold  = 当天刚卖出（明天进入冷冻）的最大利润
      rest  = 冷冻/空仓状态的最大利润

    转移:
      sold  = hold + p          （今天卖出）
      hold  = max(hold, rest-p) （今天买入 or 继续持有）
      rest  = max(rest, prev_sold)  （今天冷冻 or 继续空仓）
    时间: O(n)，空间: O(1)
    """
    if len(prices) <= 1:
        return 0
    hold = -prices[0]
    sold = 0
    rest = 0
    for p in prices[1:]:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)


# ─────────────────────────────────────────────
# #714 含手续费（不限次数）
# ─────────────────────────────────────────────
def max_profit_with_fee(prices: List[int], fee: int) -> int:
    """
    两状态 DP：
      cash = 不持有股票时的最大利润
      hold = 持有股票时的最大利润

    卖出时扣除手续费 fee。
    时间: O(n)，空间: O(1)
    """
    cash = 0
    hold = -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_stock_problems():
    # #121
    assert max_profit_i([7, 1, 5, 3, 6, 4]) == 5    # 1买6卖
    assert max_profit_i([7, 6, 4, 3, 1]) == 0        # 只跌，不交易
    assert max_profit_i([1]) == 0
    print("#121 max_profit_i: all passed")

    # #122
    assert max_profit_ii([7, 1, 5, 3, 6, 4]) == 7   # (5-1)+(6-3)=7
    assert max_profit_ii([1, 2, 3, 4, 5]) == 4
    assert max_profit_ii([7, 6, 4, 3, 1]) == 0
    print("#122 max_profit_ii: all passed")

    # #123
    assert max_profit_iii([3, 3, 5, 0, 0, 3, 1, 4]) == 6
    assert max_profit_iii([1, 2, 3, 4, 5]) == 4      # 1买5卖=4，或1买3卖+2买5卖=2+3=5？
    # 注：最多2次，[1,2,3,4,5] → 两次交易最优：1买5卖=4（一次）或1买中间卖+再买再卖
    # 实际最优：1笔 1->5 = 4，或2笔 1->5（一笔也是4，两次共计max=4）
    assert max_profit_iii([1, 2, 3, 4, 5]) == 4
    assert max_profit_iii([3, 2, 6, 5, 0, 3]) == 7
    print("#123 max_profit_iii: all passed")

    # #188
    assert max_profit_iv(2, [3, 2, 6, 5, 0, 3]) == 7
    assert max_profit_iv(2, [1, 2, 3, 4, 5]) == 4
    assert max_profit_iv(0, [1, 2]) == 0
    assert max_profit_iv(1, [1, 2]) == 1
    # k 足够大时等价于 #122
    assert max_profit_iv(100, [7, 1, 5, 3, 6, 4]) == max_profit_ii([7, 1, 5, 3, 6, 4])
    print("#188 max_profit_iv: all passed")

    # #309
    assert max_profit_with_cooldown([1, 2, 3, 0, 2]) == 3   # 1买2卖→冷冻→0买2卖
    assert max_profit_with_cooldown([1]) == 0
    assert max_profit_with_cooldown([1, 2]) == 1
    print("#309 max_profit_with_cooldown: all passed")

    # #714
    assert max_profit_with_fee([1, 3, 2, 8, 4, 9], 2) == 8
    assert max_profit_with_fee([1, 3, 7, 5, 10, 3], 3) == 6
    print("#714 max_profit_with_fee: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_stock_problems()
