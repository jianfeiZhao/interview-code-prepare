"""
题目：买卖股票的最佳时机
难度：Easy | 高频出现：字节/阿里/腾讯/美团
标签：动态规划、贪心、数组
LeetCode：#121


题目描述
---------
给定一个数组 prices，其中 prices[i] 是一支给定股票第 i 天的价格。
#121：只能进行一笔交易（买入+卖出各一次），求最大利润。
#122：可进行多笔交易（不能同时持有多只股票），求最大利润。
#123：最多完成两笔交易，求最大利润。
#188：最多完成 k 笔交易，求最大利润。

示例
------
#121 输入: prices = [7,1,5,3,6,4]  输出: 5（第2天买，第5天卖）
#122 输入: prices = [7,1,5,3,6,4]  输出: 7

约束
------
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4

TL;DR（30秒速览）
- 维护历史最低价 min_price，对每个价格计算利润 price - min_price
- 时间 O(n)，空间 O(1)
- 关键陷阱：只能买卖一次；若全程下跌则利润为 0

详细解析
---------
一遍扫描：
  min_price = 当前遇到的最低价（买入点）
  max_profit = max(max_profit, price - min_price)

等价 DP 视角：
  dp[i][0] = max(dp[i-1][0], -prices[i])   # 持有股票的最大收益
  dp[i][1] = max(dp[i-1][1], dp[i-1][0] + prices[i])  # 不持有的最大收益
  初始 dp[0][0] = -prices[0], dp[0][1] = 0
"""

from typing import List


# 方法一：贪心（推荐，最简洁）
def max_profit(prices: List[int]) -> int:
    min_price = float('inf')
    max_profit_val = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit_val:
            max_profit_val = price - min_price
    return max_profit_val


# 方法二：DP（便于扩展到多次交易）
def max_profit_dp(prices: List[int]) -> int:
    hold = -prices[0]   # 持有股票的最大收益（买入成本取负）
    cash = 0            # 不持有股票的最大收益
    for price in prices[1:]:
        cash = max(cash, hold + price)   # 今天卖出
        hold = max(hold, -price)         # 今天买入（只能买一次，不能用 cash+(-price)）
    return cash


if __name__ == "__main__":
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5   # 1 买，6 卖
    assert max_profit([7, 6, 4, 3, 1]) == 0       # 全程下跌
    assert max_profit([1]) == 0
    assert max_profit([2, 4, 1]) == 2

    assert max_profit_dp([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit_dp([7, 6, 4, 3, 1]) == 0

    print("All tests passed.")
