"""
题目：重新安排行程
难度：Hard | 高频出现：字节/阿里
标签：DFS、Hierholzer算法（欧拉路径）
LeetCode：#332

题目描述
---------
给定一组机票列表 tickets，每张机票是 [出发地, 目的地] 的形式。必须使用所有机票恰好一次，
从 "JFK" 出发，重新安排行程。如果存在多种合法路线，返回字典序最小的那一条。
保证输入数据所有机票至少存在一条合法路线。

示例
------
输入: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
输出: ["JFK","MUC","LHR","SFO","SJC"]

输入: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
输出: ["JFK","ATL","JFK","SFO","ATL","SFO"]

约束
------
- 1 <= tickets.length <= 300
- tickets[i].length == 2，出发地和目的地均为大写英文字母组成的3字母机场代码
- 保证至少存在一条合法路线

TL;DR（30秒速览）
- 欧拉路径：从 JFK 出发找经过所有边的路径
- 字典序最小：邻居按字母序排序，DFS + 后序插入结果
- 时间 O(E log E)，空间 O(E)

详细解析
---------
Hierholzer算法（欧拉路径）：
  将邻居列表排序（字典序）
  DFS：每次选最小的邻居，走完后将当前节点加入结果头部
  因为欧拉路径中，无法继续走的节点一定是终点
"""

from typing import List
from collections import defaultdict


def find_itinerary(tickets: List[List[str]]) -> List[str]:
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)

    result = []

    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        result.append(airport)

    dfs("JFK")
    return result[::-1]


if __name__ == "__main__":
    assert find_itinerary([["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]) == \
        ["JFK","MUC","LHR","SFO","SJC"]
    assert find_itinerary([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]) == \
        ["JFK","ATL","JFK","SFO","ATL","SFO"]
    print("All tests passed.")
