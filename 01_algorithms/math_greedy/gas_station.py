"""
LeetCode #134 - 加油站 (Gas Station)
难度: Medium | 频率: 字节/阿里

=== 题目描述 ===
在一条环路上有 n 个加油站，其中第 i 个加油站有汽油 gas[i] 升。
你有一辆油箱容量无限的汽车，从第 i 个加油站开往第 i+1 个加油站需要消耗汽油 cost[i] 升。
你从其中的一个加油站出发，开始时油箱为空。
给定两个整数数组 gas 和 cost，如果你能绕环路行驶一周，则返回出发加油站的编号，否则返回 -1。
如果存在解，则保证它是唯一的。

示例 1:
  输入: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
  输出: 3

示例 2:
  输入: gas = [2,3,4], cost = [3,4,3]
  输出: -1

=== TL;DR ===
核心思路（贪心）:
  1. 若总油量 >= 总消耗，必然存在解（可行性判断）
  2. 从 0 出发，若在某站 i 油箱变为负数，说明 0..i 的任意站都不能作为起点，更新起点为 i+1
  — O(n) 时间，O(1) 空间

时间复杂度: O(n)
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. 全局检验: sum(gas) < sum(cost) 则返回 -1
2. 贪心选起点: 维护 tank（当前油量）和 start（候选起点）
   - 从左到右: tank += gas[i] - cost[i]
   - 若 tank < 0: 说明从 start 到 i 都不能作为起点（因为若从中间某点出发，到 i 时更早就缺油了）
   - 更新 start = i+1，重置 tank = 0
3. 此贪心的正确性: 若总油量 >= 总消耗，从贪心得到的 start 出发一定可以绕一圈
4. 经典结论: 若 [a..b] 段油量和为负，则此段中任一点作起点都无法通过 b 站
"""


# ===== 方法1: 贪心（O(n) O(1) 面试推荐）=====
def can_complete_circuit(gas: list, cost: list) -> int:
    # 全局检验: 总油量不足则无解
    if sum(gas) < sum(cost):
        return -1

    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0

    return start


# ===== 方法2: 暴力验证（O(n^2) 用于对比）=====
def can_complete_circuit_brute(gas: list, cost: list) -> int:
    n = len(gas)
    for start in range(n):
        tank = 0
        ok = True
        for step in range(n):
            i = (start + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return start
    return -1


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
        ([2, 3, 4], [3, 4, 3], -1),
        ([5], [4], 0),
        ([1, 2], [2, 1], 1),
        ([2], [2], 0),
        ([4, 5, 2, 6, 5, 3], [3, 2, 7, 3, 2, 9], -1),
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),  # 标准例子再验一次
    ]
    for func in [can_complete_circuit, can_complete_circuit_brute]:
        for gas, cost, expected in cases:
            result = func(list(gas), list(cost))
            assert result == expected, \
                f"{func.__name__}({gas}, {cost}) = {result}, expected {expected}"

    print("All tests passed!")
