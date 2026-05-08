"""
编辑距离
LeetCode #72 (Hard)
高频考点: 字节跳动 / 阿里巴巴（字符串 DP 代表题）

============================================================

题目描述
---------
给你两个单词 word1 和 word2，请返回将 word1 转换成 word2 所使用的最少操作数。
允许对一个单词进行以下三种操作：插入一个字符、删除一个字符、替换一个字符。

示例
------
输入: word1 = "horse", word2 = "ros"
输出: 3  （horse→rorse→rose→ros）

输入: word1 = "intention", word2 = "execution"
输出: 5

约束
------
- 0 <= word1.length, word2.length <= 500
- word1 和 word2 由小写英文字母组成

TL;DR
============================================================
状态: dp[i][j] = word1[:i] 转换成 word2[:j] 的最少操作数
初始: dp[i][0] = i（删除 i 次），dp[0][j] = j（插入 j 次）
转移:
  若 word1[i-1] == word2[j-1]:
      dp[i][j] = dp[i-1][j-1]          # 字符相同，无需操作
  否则:
      dp[i][j] = 1 + min(
          dp[i-1][j],    # 删除 word1[i-1]
          dp[i][j-1],    # 插入 word2[j-1] 到 word1
          dp[i-1][j-1]   # 替换 word1[i-1] 为 word2[j-1]
      )

空间优化：滚动一行，O(min(m,n)) 空间

三种操作直觉：
  - 删除 word1[i-1]：word1[:i-1] 已可变成 word2[:j]，再删掉尾部 → dp[i-1][j]+1
  - 插入 word2[j-1]：word1[:i] 已可变成 word2[:j-1]，再插末尾 → dp[i][j-1]+1
  - 替换末位字符：word1[:i-1] 已可变成 word2[:j-1]，末位换一下 → dp[i-1][j-1]+1
============================================================
"""

from typing import List


# ─────────────────────────────────────────────
# 方法1：二维 DP（直观）
# ─────────────────────────────────────────────
def min_distance_2d(word1: str, word2: str) -> int:
    """
    时间: O(m * n)，空间: O(m * n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],     # 删除 word1[i-1]
                    dp[i][j - 1],     # 插入 word2[j-1]
                    dp[i - 1][j - 1]  # 替换
                )
    return dp[m][n]


# 保留原始接口名称，方便直接调用
def min_distance(word1: str, word2: str) -> int:
    return min_distance_2d(word1, word2)


# ─────────────────────────────────────────────
# 方法2：空间优化（滚动一行）
# ─────────────────────────────────────────────
def min_distance_optimized(word1: str, word2: str) -> int:
    """
    只保留一行 + 变量 prev 暂存对角线值。
    时间: O(m * n)，空间: O(min(m,n))
    """
    m, n = len(word1), len(word2)
    # 令较短的串放列，减少空间
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m

    dp = list(range(n + 1))  # 初始化第 0 行

    for i in range(1, m + 1):
        prev = dp[0]     # dp[i-1][j-1] 的暂存（对角线）
        dp[0] = i        # dp[i][0] = i
        for j in range(1, n + 1):
            temp = dp[j]  # 保存 dp[i-1][j]，将被本轮覆盖
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                # prev=dp[i-1][j-1] 替换, dp[j]=dp[i-1][j] 删除, dp[j-1]=dp[i][j-1] 插入
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


# ─────────────────────────────────────────────
# 扩展：输出编辑操作序列（路径回溯）
# ─────────────────────────────────────────────
def min_distance_with_ops(word1: str, word2: str) -> List[str]:
    """
    返回最短编辑操作列表（回溯 DP 表格）。
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ops.append(f"INSERT  pos={i} char='{word2[j-1]}'")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"DELETE  pos={i-1} char='{word1[i-1]}'")
            i -= 1
        else:
            ops.append(f"REPLACE pos={i-1} '{word1[i-1]}'->'{word2[j-1]}'")
            i -= 1
            j -= 1
    ops.reverse()
    return ops


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
def test_edit_distance():
    cases = [
        ("horse", "ros", 3),           # horse→rorse→rose→ros
        ("intention", "execution", 5),
        ("", "", 0),
        ("a", "", 1),
        ("", "a", 1),
        ("abc", "abc", 0),
        ("ab", "ba", 2),
    ]
    for w1, w2, expected in cases:
        r1 = min_distance_2d(w1, w2)
        r2 = min_distance_optimized(w1, w2)
        assert r1 == expected, f"2d: ({w1!r},{w2!r})={r1}, expected {expected}"
        assert r2 == expected, f"opt: ({w1!r},{w2!r})={r2}, expected {expected}"
    print("min_distance_2d & min_distance_optimized: all passed")

    ops = min_distance_with_ops("horse", "ros")
    assert len(ops) == 3
    print(f"edit ops 'horse'->'ros': {ops}")

    # 对称性：d(a,b) == d(b,a)
    assert min_distance_2d("abc", "xyz") == min_distance_2d("xyz", "abc")
    print("symmetry check passed")

    print("\n=== 所有测试通过 ===")


if __name__ == "__main__":
    test_edit_distance()
