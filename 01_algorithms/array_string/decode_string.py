"""
题目：字符串解码
难度：Medium | 高频出现：字节/阿里
标签：栈、字符串
LeetCode：#394

题目描述
---------
给定一个经过编码的字符串，返回它解码后的字符串。
编码规则为 k[encoded_string]，表示方括号内的字符串重复 k 次，k 为正整数。
编码可以嵌套，例如 3[a2[c]] 解码后为 accaccacc。

示例
------
输入: s = "3[a]2[bc]"
输出: "aaabcbc"

输入: s = "3[a2[c]]"
输出: "accaccacc"

约束
------
- 1 <= s.length <= 30
- s 只含小写字母、数字和方括号，数字范围 [1, 300]
- 输入保证合法，括号均匹配，不含多余空格

TL;DR（30秒速览）
- 思路：用两个栈分别存倍数和字符串，遇到 '[' 压栈，遇到 ']' 弹栈展开
- 时间：O(n × max_k)  空间：O(n)
- 陷阱：数字可能多位（如 100[a]），用变量累积 num 而非单字符

详细解析
---------
遍历每个字符：
  - 数字：累积 num（可多位）
  - 字母：追加到当前字符串 cur_str
  - '[' ：将 (num, cur_str) 压栈，重置 num=0, cur_str=""
  - ']' ：弹出 (k, prev_str)，cur_str = prev_str + cur_str * k
"""

def decode_string(s: str) -> str:
    num_stack = []   # 存重复次数
    str_stack = []   # 存 '[' 之前的字符串
    cur_str = ""
    num = 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '[':
            num_stack.append(num)
            str_stack.append(cur_str)
            num = 0
            cur_str = ""
        elif c == ']':
            k = num_stack.pop()
            prev = str_stack.pop()
            cur_str = prev + cur_str * k
        else:
            cur_str += c
    return cur_str


if __name__ == "__main__":
    assert decode_string("3[a]2[bc]") == "aaabcbc"
    assert decode_string("3[a2[c]]") == "accaccacc"
    assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decode_string("100[a]") == "a" * 100
    print("All tests passed.")
