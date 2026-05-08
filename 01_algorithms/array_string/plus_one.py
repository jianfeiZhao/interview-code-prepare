"""
题目：加一 / 二进制求和
难度：Easy | 高频出现：字节/阿里/腾讯
标签：数组、数学、进位
LeetCode：#66 Plus One / #67 Add Binary


题目描述
---------
给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。
最高位数字存放在数组的首位，数组中每个元素只存储单个数字，且不含前导零。

示例
------
输入: digits = [1, 2, 3]
输出: [1, 2, 4]  （123 + 1 = 124）

输入: digits = [9]
输出: [1, 0]  （9 + 1 = 10）

约束
------
- 1 <= digits.length <= 100
- 0 <= digits[i] <= 9

TL;DR（30秒速览）
- #66：从末位向前模拟进位，遇到非9直接+1返回，全9则首位补1
- #67：双指针从末位对齐，逐位异或+进位，最终进位多补'1'
- 时间 O(n)，空间 O(1)（#66原地）/ O(n)（#67需新字符串）
- 关键陷阱：全为9时数组长度会+1（如 [9,9] -> [1,0,0]）

详细解析
---------
#66 加一：
  方法：从最后一位向前扫描
    - 当前位 < 9：直接 +1，返回
    - 当前位 == 9：置0，继续向前进位
    - 循环结束仍有进位：在头部插入 1（原数组全为9）

#67 二进制加法：
  方法：双指针 i/j 从末尾对齐，carry 记录进位
    - 每轮：sum = int(a[i]) + int(b[j]) + carry
    - 当前位 = sum % 2，carry = sum // 2
    - 最后若 carry == 1，拼 '1' 在最前面
"""

from typing import List


# ─── #66 加一 ──────────────────────────────────────────────

def plus_one(digits: List[int]) -> List[int]:
    """从末位向前模拟进位，O(n) 时间，O(1) 额外空间（最坏 O(n) 新数组）"""
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0  # 当前位是9，置0并继续进位
    # 走到这里说明全是9，例如 [9,9,9] -> [1,0,0,0]
    return [1] + digits


# ─── #67 二进制求和 ────────────────────────────────────────

def add_binary(a: str, b: str) -> str:
    """双指针从末位对齐逐位相加，O(max(m,n)) 时间，O(max(m,n)) 空间"""
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    result = []

    while i >= 0 or j >= 0 or carry:
        bit_a = int(a[i]) if i >= 0 else 0
        bit_b = int(b[j]) if j >= 0 else 0
        total = bit_a + bit_b + carry
        result.append(str(total % 2))
        carry = total // 2
        i -= 1
        j -= 1

    return ''.join(reversed(result))


# ─── 另一种写法：Python int 转换（面试中可快速写出但需说明局限）──

def add_binary_pythonic(a: str, b: str) -> str:
    """利用 Python 大整数：bin(int(a,2)+int(b,2))[2:]，O(n) 但不展示位操作思维"""
    return bin(int(a, 2) + int(b, 2))[2:]


if __name__ == "__main__":
    # #66 加一
    assert plus_one([1, 2, 3]) == [1, 2, 4]
    assert plus_one([1, 2, 9]) == [1, 3, 0]
    assert plus_one([9, 9, 9]) == [1, 0, 0, 0]
    assert plus_one([0]) == [1]

    # #67 二进制求和
    assert add_binary("11", "1") == "100"
    assert add_binary("1010", "1011") == "10101"
    assert add_binary("0", "0") == "0"

    # pythonic 版结果一致
    assert add_binary_pythonic("11", "1") == "100"

    print("All tests passed.")
