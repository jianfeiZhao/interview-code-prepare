"""
题目: 括号生成
LeetCode: #22 (Medium)
高频公司: 字节跳动、阿里巴巴、腾讯（必考）

题目描述:
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且有效的括号组合。

示例 1: n = 3 ->
  ["((()))","(()())","(())()","()(())","()()()"]
示例 2: n = 1 -> ["()"]

================================================================================
TL;DR（核心思路）:
- 回溯：open < n 可加 '('；close < open 可加 ')'
- 两个限制天然保证所有结果合法，无需额外校验
- 时间 O(4^n / sqrt(n))（Catalan数），空间 O(n)

递归状态: (当前路径, 已用左括号数, 已用右括号数)
终止条件: 路径长度 == 2n
================================================================================"""

from typing import List


def generate_parenthesis(n: int) -> List[str]:
    result = []
    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(path)
            return
        if open_count < n:
            backtrack(path + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(path + ')', open_count, close_count + 1)
    backtrack('', 0, 0)
    return result


if __name__ == "__main__":
    res = sorted(generate_parenthesis(3))
    assert res == sorted(["((()))","(()())","(())()","()(())","()()()"])
    assert generate_parenthesis(1) == ["()"]
    assert len(generate_parenthesis(4)) == 14  # 第4个Catalan数
    assert len(generate_parenthesis(5)) == 42  # 第5个Catalan数

    # 验证所有结果有效（括号合法性检验）
    def is_valid(s):
        count = 0
        for c in s:
            if c == '(': count += 1
            else: count -= 1
            if count < 0: return False
        return count == 0

    for n in range(1, 6):
        for combo in generate_parenthesis(n):
            assert is_valid(combo), f"无效括号: {combo}"

    print("所有测试通过!")
    print(f"\nn=3 的所有合法括号:")
    for p in generate_parenthesis(3):
        print(f"  {p}")
