"""
LeetCode #20 - 有效的括号 (Valid Parentheses)
难度: Easy | 频率: 全系必考

=== 题目描述 ===
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s，判断字符串是否有效。
有效字符串需满足:
  1. 左括号必须用相同类型的右括号闭合。
  2. 左括号必须以正确的顺序闭合。
  3. 每个右括号都有一个对应的相同类型的左括号。

示例 1: 输入: s = "()"      输出: true
示例 2: 输入: s = "()[]{}"  输出: true
示例 3: 输入: s = "(]"      输出: false
示例 4: 输入: s = "([)]"    输出: false
示例 5: 输入: s = "{[]}"    输出: true

=== TL;DR ===
核心思路: 用栈（stack）模拟括号匹配。遇到左括号入栈，遇到右括号时检查栈顶是否匹配。
时间复杂度: O(n)，n 为字符串长度
空间复杂度: O(n)，最坏情况全是左括号

=== 详细解析 ===
关键技巧:
1. 用字典 mapping = {')':'(', ']':'[', '}':'{'} 存储匹配关系，避免 if-elif 链
2. 遇到右括号时: 若栈为空 或 stack.pop() != mapping[c]，直接返回 False
3. 最后检查栈是否为空（确保所有左括号都被匹配）
4. 一个简化技巧: 入栈时直接存对应的右括号，遇到右括号直接 pop 比较
5. 长度为奇数可以直接返回 False（剪枝）
"""


# ===== 标准栈解法（面试推荐）=====
def is_valid(s: str) -> bool:
    if len(s) % 2 == 1:
        return False  # 奇数长度必然不合法

    # 右括号 -> 对应左括号
    mapping = {')': '(', ']': '[', '}': '{'}
    stack = []

    for c in s:
        if c in mapping:
            # 右括号: 检查栈顶
            if not stack or stack[-1] != mapping[c]:
                return False
            stack.pop()
        else:
            # 左括号: 入栈
            stack.append(c)

    return len(stack) == 0


# ===== 变体: 入栈存对应右括号 =====
def is_valid_v2(s: str) -> bool:
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for c in s:
        if c in pairs:
            stack.append(pairs[c])  # 存期望的右括号
        elif not stack or stack.pop() != c:
            return False

    return not stack


# ===== 测试 =====
if __name__ == "__main__":
    for func in [is_valid, is_valid_v2]:
        assert func("()") == True
        assert func("()[]{}") == True
        assert func("(]") == False
        assert func("([)]") == False
        assert func("{[]}") == True
        assert func("") == True          # 空字符串合法
        assert func("(") == False        # 单个左括号
        assert func(")") == False        # 单个右括号
        assert func("((()))") == True
        assert func("(((") == False
        assert func("]") == False
        assert func("([{}])") == True
        assert func("([{]})") == False

    print("All tests passed!")
