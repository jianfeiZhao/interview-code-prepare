"""
LeetCode #6 - Z 字形变换 (Zigzag Conversion)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
将一个给定字符串 s 根据给定的行数 numRows，以从上往下、从左到右进行 Z 字形排列。
比如输入字符串为 "PAYPALISHIRING"，行数为 3 时，排列如下:
  P   A   H   N
  A P L S I I G
  Y   I   R

之后，你的输出需要从左往右逐行读取，产生出一个新的字符串: "PAHNAPLSIIGYIR"

示例 2:
  输入: s = "PAYPALISHIRING", numRows = 4
  输出: "PINALSIGYAHRPI"
  排列:
    P     I    N
    A   L S  I G
    Y A   H R
    P     I

示例 3:
  输入: s = "A", numRows = 1
  输出: "A"

=== TL;DR ===
核心思路: 模拟，用 numRows 个字符串桶分别存放每行的字符。
  用一个变量 direction 控制当前是向下走还是向上走，到达边界时反向。
时间复杂度: O(n)，n 为字符串长度
空间复杂度: O(n)，所有桶合计存储所有字符

=== 详细解析 ===
关键技巧:
1. 用 rows = [''] * numRows 存每行字符
2. cur_row 从 0 到 numRows-1，再从 numRows-1 到 0，交替循环
3. direction 标志: +1 表示向下，-1 表示向上；到达首行或末行时反向
4. 特殊情况: numRows == 1 时直接返回 s（否则 direction 永远不翻转）
5. 数学规律（可不用模拟）: 每个 zigzag 周期长度 cycle = 2*(numRows-1)，
   按列索引公式直接算每行字符下标
"""


# ===== 方法1: 模拟行桶（面试推荐）=====
def convert_simulate(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s

    rows = [''] * numRows
    cur_row = 0
    going_down = False

    for c in s:
        rows[cur_row] += c
        if cur_row == 0 or cur_row == numRows - 1:
            going_down = not going_down
        cur_row += 1 if going_down else -1

    return ''.join(rows)


# ===== 方法2: 数学规律（直接按行输出）=====
def convert_math(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s

    result = []
    cycle = 2 * (numRows - 1)  # 每个周期长度

    for row in range(numRows):
        for j in range(0, len(s), cycle):
            # 每个周期在该行的第一个字符
            if j + row < len(s):
                result.append(s[j + row])
            # 非首尾行还有第二个字符（中间斜线位置）
            if row != 0 and row != numRows - 1:
                second = j + cycle - row
                if second < len(s):
                    result.append(s[second])

    return ''.join(result)


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [convert_simulate, convert_math]

    for func in funcs:
        assert func("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR", func.__name__
        assert func("PAYPALISHIRING", 4) == "PINALSIGYAHRPI", func.__name__
        assert func("A", 1) == "A",                           func.__name__
        assert func("AB", 1) == "AB",                         func.__name__
        assert func("AB", 2) == "AB",                         func.__name__
        assert func("ABCD", 2) == "ACBD",                     func.__name__
        # numRows >= len(s) 时直接返回
        assert func("AB", 3) == "AB",                         func.__name__

    print("All tests passed!")
