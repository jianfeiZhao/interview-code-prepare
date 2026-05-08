"""
LeetCode #224 + #227 - 基本计算器 I + II (Basic Calculator I + II)
难度: Hard(#224) + Medium(#227) | 频率: 字节/阿里

=== 题目描述 ===
【#227 基本计算器 II】
给你一个字符串表达式 s，请你实现一个基本计算器来计算并返回它的值。
整数除法仅保留整数部分。s 包含整数和 '+'、'-'、'*'、'/' 四种运算符及空格，不含括号。

示例: "3+2*2" -> 7；" 3/2 " -> 1；" 3+5 / 2 " -> 5

【#224 基本计算器 I】
实现一个基本计算器来计算并返回它的值。表达式包含整数、'+'、'-'、'(' 和 ')'。

示例: "1 + 1" -> 2；" 2-1 + 2 " -> 3；"(1+(4+5+2)-3)+(6+8)" -> 23

=== TL;DR ===
#227 核心思路: 遇到 '+'/'-' 将当前数（带符号）入栈；遇到 '*'/'/' 弹出栈顶立即计算；
  最后对栈中所有数求和 — 利用栈延迟处理低优先级运算
#224 核心思路: 用栈维护括号内的符号上下文（符号继承），递归或栈处理括号嵌套

时间复杂度: O(n)
空间复杂度: O(n)

=== 详细解析 ===
#227 关键技巧:
1. 遍历时维护 sign（上一个运算符）和 num（当前数）
2. 遇到非数字字符（或末尾）时根据 sign 决定如何处理 num:
   - '+': 入栈 +num
   - '-': 入栈 -num
   - '*': 弹出栈顶，乘以 num 后入栈
   - '/': 弹出栈顶，除以 num（向零取整）后入栈
3. 末尾没有运算符触发，需在遍历结束时或 i == len(s)-1 时处理最后一个 num

#224 关键技巧:
1. 遇到 '(' 时将当前 result 和 sign 压栈，重置 result=0, sign=1
2. 遇到 ')' 时: result = result * sign_from_stack + result_from_stack
3. 最外层循环处理 +/- 运算（无 */，所以不需要优先级栈）
"""


# ===== #227 基本计算器 II（含 +-*/ 无括号）=====
def calculate_ii(s: str) -> int:
    stack = []
    num = 0
    sign = '+'
    s = s.replace(' ', '')

    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if (not c.isdigit()) or i == len(s) - 1:
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack.append(stack.pop() * num)
            elif sign == '/':
                stack.append(int(stack.pop() / num))  # 向零取整
            sign = c
            num = 0

    return sum(stack)


# ===== #224 基本计算器 I（含 +- 和括号）=====
def calculate_i(s: str) -> int:
    stack = []   # 存 (result_before_paren, sign_before_paren)
    result = 0
    num = 0
    sign = 1     # +1 或 -1

    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '+':
            result += sign * num
            num = 0
            sign = 1
        elif c == '-':
            result += sign * num
            num = 0
            sign = -1
        elif c == '(':
            # 保存当前 result 和 sign，重新开始
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif c == ')':
            result += sign * num
            num = 0
            result *= stack.pop()    # 乘以括号外的符号
            result += stack.pop()    # 加上括号外的 result

    result += sign * num
    return result


# ===== 进阶: 通用计算器（支持 +-*/ 和括号）=====
def calculate_full(s: str) -> int:
    """支持加减乘除和括号的完整计算器（递归解法）"""
    def parse(i: int):
        stack = []
        num = 0
        sign = '+'

        while i < len(s):
            c = s[i]
            if c.isdigit():
                num = num * 10 + int(c)
            if c == '(':
                num, i = parse(i + 1)  # 递归处理括号内
            if (not c.isdigit() and c != ' ') or i == len(s) - 1:
                if sign == '+':
                    stack.append(num)
                elif sign == '-':
                    stack.append(-num)
                elif sign == '*':
                    stack.append(stack.pop() * num)
                elif sign == '/':
                    stack.append(int(stack.pop() / num))
                sign = c
                num = 0
                if c == ')':
                    return sum(stack), i
            i += 1

        return sum(stack), i

    result, _ = parse(0)
    return result


# ===== 测试 =====
if __name__ == "__main__":
    # #227 测试
    cases_ii = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("14-3/2", 13),
        ("1+1", 2),
        ("100", 100),
        ("0-2147483647", -2147483647),
    ]
    for expr, expected in cases_ii:
        result = calculate_ii(expr)
        assert result == expected, f"calculate_ii({expr!r}) = {result}, expected {expected}"

    # #224 测试
    cases_i = [
        ("1 + 1", 2),
        (" 2-1 + 2 ", 3),
        ("(1+(4+5+2)-3)+(6+8)", 23),
        ("- (3 + (4 + 5))", -12),
        ("1-(     -2)", 3),
    ]
    for expr, expected in cases_i:
        result = calculate_i(expr)
        assert result == expected, f"calculate_i({expr!r}) = {result}, expected {expected}"

    # 通用计算器测试（#224 + #227）
    cases_full = [
        ("3+2*2", 7),
        ("(1+2)*3", 9),
        ("2*(3+4)", 14),
        ("(2+3)*(4-1)", 15),
    ]
    for expr, expected in cases_full:
        result = calculate_full(expr)
        assert result == expected, f"calculate_full({expr!r}) = {result}, expected {expected}"

    print("All tests passed!")
