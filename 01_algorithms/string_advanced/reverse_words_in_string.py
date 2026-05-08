"""
LeetCode #151 - 翻转字符串里的单词 (Reverse Words in a String)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
给你一个字符串 s，请你反转字符串中单词的顺序。
单词是由非空格字符组成的字符串，s 中使用至少一个空格将字符串中的单词分隔开。
返回单词顺序颠倒且单词之间用单个空格连接的结果字符串。

注意: 输入字符串 s 中可能会存在前导空格、尾随空格或者单词间的多个空格。
返回的结果字符串中，单词间应当仅用单个空格分隔，且不包含任何额外的空格。

示例 1:
  输入: s = "the sky is blue"
  输出: "blue is sky the"

示例 2:
  输入: s = "  hello world  "
  输出: "world hello"（去掉首尾空格）

示例 3:
  输入: s = "a good   example"
  输出: "example good a"（单词间多余空格变为单空格）

=== TL;DR ===
核心思路:
  方法1（Python 内置）: s.split() 自动处理多余空格，reverse 后 join — O(n) 时间
  方法2（双端队列）: 从左到右解析单词，每次加到队列头部，最后 join — O(n)
  方法3（原地翻转，O(1)空间进阶）: 先翻转整体，再翻转每个单词（不含多余空格）

时间复杂度: O(n)
空间复杂度: O(n)（方法3 用列表模拟原地时为 O(n)，纯原地 O(1)）

=== 详细解析 ===
关键技巧:
1. Python split() 无参数调用会自动分割所有空白并去除首尾空白，非常方便
2. ' '.join(reversed(words)) 等价于 ' '.join(words[::-1])
3. 进阶原地翻转思路: 先整体 reverse，再对每个单词单独 reverse，得到正序单词逆序排列
4. 双指针扫描单词: i,j 双指针找到每个单词的起止位置
5. 面试中方法1最快写完，方法3展示对字符数组操作的理解
"""

from collections import deque


# ===== 方法1: Python 内置（最简洁，推荐）=====
def reverse_words_builtin(s: str) -> str:
    return ' '.join(reversed(s.split()))


# ===== 方法2: 双端队列 =====
def reverse_words_deque(s: str) -> str:
    dq = deque()
    i, n = 0, len(s)
    while i < n:
        if s[i] != ' ':
            j = i
            while j < n and s[j] != ' ':
                j += 1
            dq.appendleft(s[i:j])  # 加到头部
            i = j
        else:
            i += 1
    return ' '.join(dq)


# ===== 方法3: 原地翻转思路（列表模拟）=====
def reverse_words_inplace(s: str) -> str:
    # 步骤1: 先按空格分词（过滤空串），存入列表
    words = s.split()
    # 步骤2: 原地翻转整个列表
    words.reverse()
    # 步骤3: 用单空格拼接
    return ' '.join(words)


# ===== 方法4: 手动双指针扫描（不使用split）=====
def reverse_words_manual(s: str) -> str:
    result = []
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] == ' ':
            i += 1
        if i == n:
            break
        j = i
        while j < n and s[j] != ' ':
            j += 1
        result.append(s[i:j])
        i = j
    return ' '.join(reversed(result))


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [
        reverse_words_builtin,
        reverse_words_deque,
        reverse_words_inplace,
        reverse_words_manual,
    ]
    for func in funcs:
        assert func("the sky is blue") == "blue is sky the", func.__name__
        assert func("  hello world  ") == "world hello", func.__name__
        assert func("a good   example") == "example good a", func.__name__
        assert func("a") == "a", func.__name__
        assert func("  bob    love  alice  ") == "alice love bob", func.__name__
        assert func("Alice does not even like bob") == "bob like even not does Alice", func.__name__

    print("All tests passed!")
