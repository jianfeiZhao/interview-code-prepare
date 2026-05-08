"""
题目: 电话号码的字母组合
LeetCode: #17 (Medium)
高频公司: 全系（字节、阿里、腾讯、百度等）

题目描述:
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按任意顺序返回。
数字到字母的映射（与电话按键相同）：
  2 -> abc, 3 -> def, 4 -> ghi, 5 -> jkl, 6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz

示例 1: digits = "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
示例 2: digits = "" -> []
示例 3: digits = "2" -> ["a","b","c"]

================================================================================
TL;DR（核心思路）:
- 回溯：依次处理每个数字，对应字母逐一加入路径
- 状态: 当前已处理到 digits[idx]，路径 path
- 终止: idx == len(digits)，记录结果
- 每层分支数 = 当前数字对应字母数（3 或 4）

时间复杂度: O(4^n * n)，n 为数字个数，4 为最多字母数
空间复杂度: O(n)，递归栈深度
================================================================================
"""

from typing import List


PHONE_MAP = {
    '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
    '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
}


def letterCombinations(digits: str) -> List[str]:
    """
    回溯：每次选当前数字对应的一个字母，递归处理下一个数字。
    """
    if not digits:
        return []

    result = []

    def backtrack(idx: int, path: List[str]):
        if idx == len(digits):
            result.append("".join(path))
            return

        for char in PHONE_MAP[digits[idx]]:
            path.append(char)
            backtrack(idx + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def letterCombinations_iterative(digits: str) -> List[str]:
    """
    迭代版（BFS 层序扩展）：
    初始化结果为 [""]，每次处理一个数字，将结果中每个字符串与新字母组合。
    """
    if not digits:
        return []

    result = [""]

    for digit in digits:
        new_result = []
        for combo in result:
            for char in PHONE_MAP[digit]:
                new_result.append(combo + char)
        result = new_result

    return result


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    r1 = sorted(letterCombinations("23"))
    expected = sorted(["ad","ae","af","bd","be","bf","cd","ce","cf"])
    assert r1 == expected, f"got {r1}"

    assert sorted(letterCombinations("2")) == ["a","b","c"]
    assert letterCombinations("") == []

    # 包含 7 和 9（4个字母）
    r2 = letterCombinations("79")
    assert len(r2) == 16  # 4 * 4 = 16

    # 三位数字
    r3 = letterCombinations("234")
    assert len(r3) == 3 * 3 * 3  # = 27

    # 两种实现结果一致
    for digits in ["23", "2", "79", "234", "2345"]:
        assert sorted(letterCombinations(digits)) == sorted(letterCombinations_iterative(digits)), \
            f"两种实现不一致: {digits}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"'23' -> {letterCombinations('23')}")
    print(f"'2'  -> {letterCombinations('2')}")
    print(f"''   -> {letterCombinations('')}")
    print(f"'79' -> {letterCombinations('79')} (共{len(letterCombinations('79'))}个)")
