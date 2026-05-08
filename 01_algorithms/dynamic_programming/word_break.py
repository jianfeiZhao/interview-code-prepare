"""
单词拆分
LeetCode #139 (Medium) + #140 (Hard, 返回所有方案)
高频考点: 字节跳动 / 阿里巴巴 / 腾讯

============================================================

题目描述
---------
给你一个字符串 s 和一个字符串列表 wordDict 作为字典，判断是否可以利用字典中出现的
单词拼接出 s。注意：不要求字典中出现的单词全部都使用，且字典中的单词可以重复使用。

扩展 #140：返回所有可以拼出 s 的方案（以空格分割的句子）。

示例
------
输入: s = "leetcode", wordDict = ["leet","code"]
输出: True

输入: s = "applepenapple", wordDict = ["apple","pen"]
输出: True

约束
------
- 1 <= s.length <= 300，1 <= wordDict.length <= 1000
- s 和 wordDict[i] 仅由小写英文字母组成

TL;DR
============================================================
状态: dp[i] = 字符串 s[:i] 能否被词典中的单词完全拆分
初始: dp[0] = True（空字符串）
转移: dp[i] = any(dp[j] and s[j:i] in word_set)  for j in [0, i)
答案: dp[len(s)]

优化思路：
  - 内层枚举只走词典中存在的长度（而非枚举所有 j），减少无效检查
  - 用 set 使 s[j:i] in word_set 达到 O(1) 均摊

#140 变体：返回所有拆分方案 → 记忆化回溯（DFS + memo）
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：DP（判断能否拆分）
# ─────────────────────────────────────────────
def word_break(s: str, word_dict: List[str]) -> bool:
    """
    时间: O(n^2)，空间: O(n + |word_dict|)
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break  # 一旦找到就跳出内层，提前终止
    return dp[n]


# ─────────────────────────────────────────────
# 方法2：优化版（只枚举词典长度）
# ─────────────────────────────────────────────
def word_break_optimized(s: str, word_dict: List[str]) -> bool:
    """
    内层只枚举词典中存在的单词长度作为分割点，减少无效子串检查。
    当词典远小于 n 时更优。
    """
    word_set = set(word_dict)
    word_lens = set(len(w) for w in word_set)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for length in word_lens:
            j = i - length
            if j >= 0 and dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]


# ─────────────────────────────────────────────
# 方法3：#140 返回所有拆分方案（记忆化 DFS）
# ─────────────────────────────────────────────
def word_break_ii(s: str, word_dict: List[str]) -> List[str]:
    """
    LeetCode #140 Hard.
    记忆化 DFS：memo[start] 缓存从 start 开始能拆分出的所有句子列表。
    时间: O(n^2 * 结果数)，空间: O(n * 结果数)
    """
    word_set = set(word_dict)
    memo = {}

    def dfs(start: int) -> List[str]:
        if start in memo:
            return memo[start]
        if start == len(s):
            return [""]  # 返回空串作为拼接终止符
        results = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for rest in dfs(end):
                    sentence = word + (" " + rest if rest else "")
                    results.append(sentence)
        memo[start] = results
        return results

    return dfs(0)


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_word_break():
    # 基本用例
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert word_break("", ["a"]) is True          # 空串可拆分
    assert word_break("a", ["a"]) is True
    assert word_break("ab", ["a", "b"]) is True
    assert word_break("ab", ["a", "c"]) is False
    print("word_break (DP): all passed")

    # 优化版结果一致
    assert word_break_optimized("leetcode", ["leet", "code"]) is True
    assert word_break_optimized("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print("word_break_optimized: all passed")

    # #140 所有方案
    res = word_break_ii("catsanddog", ["cat", "cats", "and", "sand", "dog"])
    assert sorted(res) == ["cat sand dog", "cats and dog"]

    res2 = word_break_ii("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"])
    assert sorted(res2) == sorted(["pine apple pen apple", "pineapple pen apple", "pine applepen apple"])

    res3 = word_break_ii("catsandog", ["cats", "dog", "sand", "and", "cat"])
    assert res3 == []
    print("word_break_ii: all passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_word_break()
