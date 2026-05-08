"""
LeetCode #5 - 最长回文子串 (Longest Palindromic Substring)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
给你一个字符串 s，找到 s 中最长的回文子串。
如果字符串的反序与原始字符串相同，则该字符串称为回文字符串。

示例 1:
  输入: s = "babad"
  输出: "bab"（"aba" 同样是符合题意的答案）

示例 2:
  输入: s = "cbbd"
  输出: "bb"

=== TL;DR ===
核心思路:
  方法1（中心扩展）: 以每个字符（奇数长度）和相邻字符对（偶数长度）为中心向外扩展
    — O(n²) 时间，O(1) 空间（面试最推荐）
  方法2（动态规划）: dp[i][j] = s[i]==s[j] and dp[i+1][j-1]
    — O(n²) 时间，O(n²) 空间
  方法3（Manacher 算法）: 线性时间，在字符间插入'#'统一奇偶
    — O(n) 时间，O(n) 空间（进阶，面试加分）

时间复杂度: O(n²)（中心扩展）/ O(n)（Manacher）
空间复杂度: O(1)（中心扩展）/ O(n)（Manacher）

=== 详细解析 ===
关键技巧:
1. 中心扩展: 共有 2n-1 个中心（n个奇数中心 + n-1个偶数中心）
2. 扩展时同时处理奇偶: expand(l, r) 当 s[l]==s[r] 时继续扩展
3. Manacher: 在字符间插入'#'将所有回文统一为奇数长度，利用已知最右回文加速
4. Manacher核心: 维护最右回文中心c和最右边界r，当 i < r 时可用对称点初始化 p[i]
5. 记录答案时记录起始位置+长度，最后切片取结果
"""


# ===== 方法1: 中心扩展（面试推荐）=====
def longest_palindrome_expand(s: str) -> str:
    if not s:
        return ""

    def expand(l: int, r: int) -> int:
        """从(l,r)向外扩展，返回回文半径（以字符数计）"""
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return r - l - 1  # 回文长度

    start, max_len = 0, 1
    for i in range(len(s)):
        # 奇数长度回文，中心为 s[i]
        odd_len = expand(i, i)
        # 偶数长度回文，中心为 s[i] 和 s[i+1] 之间
        even_len = expand(i, i + 1)
        best = max(odd_len, even_len)
        if best > max_len:
            max_len = best
            # 反推起始位置
            start = i - (best - 1) // 2
    return s[start:start + max_len]


# ===== 方法2: 动态规划 =====
def longest_palindrome_dp(s: str) -> str:
    n = len(s)
    if n == 0:
        return ""
    # dp[i][j] 表示 s[i..j] 是否为回文
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # 长度为1的子串
    for i in range(n):
        dp[i][i] = True

    # 长度为2的子串
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2

    # 长度 >= 3 的子串
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length

    return s[start:start + max_len]


# ===== 方法3: Manacher 算法（O(n)，面试加分）=====
def longest_palindrome_manacher(s: str) -> str:
    # 在字符间插入'#'，首尾插入'^'和'$'防止越界
    t = '^#' + '#'.join(s) + '#$'
    n = len(t)
    p = [0] * n   # p[i] 表示以t[i]为中心的回文半径
    c = r = 0     # c: 当前最右回文的中心；r: 最右回文的右边界

    for i in range(1, n - 1):
        mirror = 2 * c - i  # i 关于 c 的对称点
        if i < r:
            p[i] = min(r - i, p[mirror])  # 利用对称性初始化
        # 尝试继续扩展
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        # 更新最右回文中心和边界
        if i + p[i] > r:
            c, r = i, i + p[i]

    # 找最大 p[i]，还原在原字符串中的位置
    max_len, center = max((p[i], i) for i in range(1, n - 1))
    start = (center - max_len) // 2  # 还原到原字符串下标
    return s[start:start + max_len]


# ===== 测试 =====
if __name__ == "__main__":
    def check(func, s, expected_len):
        result = func(s)
        assert len(result) == expected_len, f"{func.__name__}({s!r}) = {result!r}, expected len {expected_len}"
        # 验证结果确实是回文
        assert result == result[::-1], f"{result!r} is not a palindrome"

    # "babad" -> "bab" 或 "aba"，长度3
    check(longest_palindrome_expand, "babad", 3)
    check(longest_palindrome_dp, "babad", 3)
    check(longest_palindrome_manacher, "babad", 3)

    # "cbbd" -> "bb"，长度2
    check(longest_palindrome_expand, "cbbd", 2)
    check(longest_palindrome_dp, "cbbd", 2)
    check(longest_palindrome_manacher, "cbbd", 2)

    # 单字符
    check(longest_palindrome_expand, "a", 1)
    check(longest_palindrome_dp, "a", 1)
    check(longest_palindrome_manacher, "a", 1)

    # 全相同字符
    check(longest_palindrome_expand, "aaaa", 4)
    check(longest_palindrome_dp, "aaaa", 4)
    check(longest_palindrome_manacher, "aaaa", 4)

    # 整体就是回文
    check(longest_palindrome_expand, "racecar", 7)
    check(longest_palindrome_dp, "racecar", 7)
    check(longest_palindrome_manacher, "racecar", 7)

    # "ac" -> 单字符，长度1
    check(longest_palindrome_expand, "ac", 1)

    print("All tests passed!")
