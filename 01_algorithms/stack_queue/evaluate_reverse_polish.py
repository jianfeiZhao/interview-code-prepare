"""
LeetCode #150 - 逆波兰表达式求值 (Evaluate Reverse Polish Notation)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
给你一个字符串数组 tokens，表示一个根据逆波兰表示法表示的算术表达式。
请你计算该表达式。返回一个表示表达式值的整数。
有效的算符为 '+'、'-'、'*' 和 '/'。每个操作数（运算对象）都可以是一个整数或者另一个表达式。
注意：两个整数之间的除法只保留整数部分，可以假设给定的逆波兰表达式总是有效的。

示例 1: tokens = ["2","1","+","3","*"]  输出: 9   (( 2 + 1 ) * 3 = 9)
示例 2: tokens = ["4","13","5","/","+"] 输出: 6   (4 + (13 / 5) = 6)
示例 3: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]  输出: 22

=== TL;DR ===
核心思路: 用栈模拟。遇到数字入栈，遇到运算符弹出两个操作数计算后将结果入栈。
时间复杂度: O(n)
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. 遇到运算符时，先弹 b（右操作数），再弹 a（左操作数），注意顺序（减法和除法不满足交换律）
2. Python 除法截断: int(a / b) 处理负数时向零截断（与 C++ 一致），而 a // b 是向下取整
   例: int(-7 / 2) = -3，但 -7 // 2 = -4；题目要求向零截断，所以用 int(a / b)
3. 用字典 {'+': lambda a,b: a+b, ...} 简化运算符分支
4. 逆波兰表达式的求值顺序与栈结构天然契合
"""

import operator


# ===== 方法1: 字典映射运算符（推荐）=====
def eval_rpn(tokens: list) -> int:
    stack = []
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': lambda a, b: int(a / b),  # 向零截断
    }
    for token in tokens:
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]


# ===== 方法2: if-elif 分支（更直白）=====
def eval_rpn_v2(tokens: list) -> int:
    stack = []
    for token in tokens:
        if token == '+':
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif token == '-':
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif token == '*':
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif token == '/':
            b, a = stack.pop(), stack.pop()
            stack.append(int(a / b))  # 向零截断
        else:
            stack.append(int(token))
    return stack[0]


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        (["2", "1", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
        (["3"], 3),
        (["3", "4", "+"], 7),
        (["5", "1", "2", "+", "4", "*", "+", "3", "-"], 14),
        # 负数除法向零截断
        (["-1", "2", "/"], 0),      # -1/2 = 0（截断）
        (["7", "-2", "/"], -3),     # 7 / -2 = -3（截断）
    ]
    for func in [eval_rpn, eval_rpn_v2]:
        for tokens, expected in cases:
            result = func(list(tokens))
            assert result == expected, \
                f"{func.__name__}({tokens}) = {result}, expected {expected}"

    print("All tests passed!")
