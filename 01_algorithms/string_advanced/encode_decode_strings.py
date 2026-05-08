"""
题目：字符串的编码与解码
难度：Medium | 高频出现：字节/阿里
标签：字符串、设计
LeetCode：#271 (Premium)

题目描述
---------
设计一个算法，将字符串列表编码为单个字符串，再将该字符串解码还原为原始列表。
编码后的字符串可在网络上传输，解码后需完全还原原始字符串列表（包括含特殊字符的字符串）。
需保证任意字符串（含空字符串、含 '#' 等特殊字符）均能正确处理。

示例
------
输入: strs = ["hello", "world"]
输出: decode(encode(["hello","world"])) == ["hello","world"]

输入: strs = ["", "abc", "3#def", "hello world"]
输出: decode(encode(strs)) == strs（含空串和含 '#' 的字符串均能正确还原）

约束
------
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200
- strs[i] 可包含任意 256 个 ASCII 字符

TL;DR（30秒速览）
- 编码：每个字符串加前缀 "长度#"，如 "hello" → "5#hello"
- 解码：读取数字直到 '#'，再读对应长度的字符串
- 时间 O(n)，空间 O(n)

详细解析
---------
关键：分隔符不能出现在字符串内容中
使用 "长度#" 前缀完全避免了这个问题：
  任何字符（包括#）都可以安全存储
  解码时先读数字再读内容，不会误判
"""

from typing import List


def encode(strs: List[str]) -> str:
    return ''.join(f"{len(s)}#{s}" for s in strs)


def decode(s: str) -> List[str]:
    result = []
    i = 0
    while i < len(s):
        j = s.index('#', i)
        length = int(s[i:j])
        result.append(s[j+1:j+1+length])
        i = j + 1 + length
    return result


if __name__ == "__main__":
    strs = ["hello", "world"]
    assert decode(encode(strs)) == strs

    strs2 = ["", "abc", "3#def", "hello world"]
    assert decode(encode(strs2)) == strs2

    strs3 = []
    assert decode(encode(strs3)) == strs3

    strs4 = ["a"]
    assert decode(encode(strs4)) == strs4
    print("All tests passed.")
