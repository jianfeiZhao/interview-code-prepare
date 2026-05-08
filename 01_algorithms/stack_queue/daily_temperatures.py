"""
LeetCode #739 - 每日温度 (Daily Temperatures)
难度: Medium | 频率: 字节/腾讯/阿里

=== 题目描述 ===
给定一个整数数组 temperatures，表示每天的温度，返回一个数组 answer，
其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。
如果气温在这之后都不会升高，请在该位置用 0 来代替。

示例 1: 输入: temperatures = [73,74,75,71,69,72,76,73]
       输出: [1,1,4,2,1,1,0,0]

示例 2: 输入: temperatures = [30,40,50,60]  输出: [1,1,1,0]
示例 3: 输入: temperatures = [30,60,90]     输出: [1,1,0]

=== TL;DR ===
核心思路（单调栈）: 维护一个单调递减栈（存下标），遇到更高温度时弹栈并计算天数差。
  - 遍历每个温度，若当前温度 > 栈顶对应温度，弹出栈顶，记录天数差
  - 循环弹出直到栈为空或栈顶温度 >= 当前温度
  - 最后将当前下标入栈
时间复杂度: O(n)，每个元素最多入栈出栈各一次
空间复杂度: O(n)，栈最大存储 n 个元素

=== 详细解析 ===
单调栈关键技巧:
1. 栈中存下标而非值，方便计算天数差 answer[i] = j - i
2. 单调递减栈: 栈中保持从底到顶温度递减，一旦遇到更高温度就弹出
3. 典型单调栈问题: "下一个更大元素"系列（#739, #496, #503, #84, #85）
4. 正向/反向遍历都可以，正向更直观
5. 单调栈模板:
   stack = []  # 存下标
   for i, val in enumerate(arr):
       while stack and arr[stack[-1]] < val:  # 找到了栈顶的"下一个更大"
           idx = stack.pop()
           result[idx] = i - idx
       stack.append(i)
"""


# ===== 方法1: 单调栈（标准解法）=====
def daily_temperatures(temperatures: list) -> list:
    n = len(temperatures)
    answer = [0] * n
    stack = []  # 单调递减栈，存下标

    for i, temp in enumerate(temperatures):
        # 当前温度比栈顶温度高，弹出栈顶并记录结果
        while stack and temperatures[stack[-1]] < temp:
            idx = stack.pop()
            answer[idx] = i - idx
        stack.append(i)

    # 栈中剩余的下标对应的 answer 已经是 0（默认值）
    return answer


# ===== 方法2: 暴力（O(n^2) 对比）=====
def daily_temperatures_brute(temperatures: list) -> list:
    n = len(temperatures)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    return answer


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 60, 90], [1, 1, 0]),
        ([90, 80, 70, 60], [0, 0, 0, 0]),  # 纯下降
        ([60, 70, 80, 90], [1, 1, 1, 0]),  # 纯上升
        ([1], [0]),
        ([2, 1, 2], [0, 1, 0]),
    ]
    for func in [daily_temperatures, daily_temperatures_brute]:
        for temps, expected in cases:
            result = func(list(temps))
            assert result == expected, \
                f"{func.__name__}({temps}) = {result}, expected {expected}"

    print("All tests passed!")
