"""
LeetCode #136 - 只出现一次的数字 (Single Number)
难度: Easy | 频率: 全系必考

=== 题目描述 ===
给你一个非空整数数组 nums，除了某个元素只出现一次以外，其余每个元素均出现两次。
找出那个只出现了一次的元素。
要求: 线性时间复杂度，不使用额外空间。

示例 1: 输入: nums = [2,2,1]        输出: 1
示例 2: 输入: nums = [4,1,2,1,2]    输出: 4
示例 3: 输入: nums = [1]             输出: 1

=== TL;DR ===
核心思路: 利用异或（XOR）的性质: a^a=0，0^a=a，且满足交换律和结合律。
  将所有数字全部异或，出现两次的互相抵消，最终剩下只出现一次的数字。
时间复杂度: O(n)
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. XOR 性质: 任何数与自身异或得 0；任何数与 0 异或得自身
2. 交换律+结合律: 顺序不影响结果，成对的数字最终消为 0
3. Python 用 functools.reduce(operator.xor, nums) 一行实现
4. 进阶 #137（只出现一次 II，其余出现三次）: 用位运算统计每位上 1 的个数，模3取余
5. 进阶 #260（只出现一次 III，两个不同数各出现一次）: 先 XOR 全部，找到区分两数的位，再分组
"""

from functools import reduce
from operator import xor


# ===== 方法1: 遍历异或（面试推荐）=====
def single_number_xor(nums: list) -> int:
    result = 0
    for num in nums:
        result ^= num
    return result


# ===== 方法2: reduce（Python 简洁写法）=====
def single_number_reduce(nums: list) -> int:
    return reduce(xor, nums)


# ===== 方法3: 数学（2*sum(set) - sum(all)）=====
def single_number_math(nums: list) -> int:
    return 2 * sum(set(nums)) - sum(nums)


# ===== 进阶: #137 只出现一次，其余出现三次 =====
def single_number_ii(nums: list) -> int:
    """每个元素除了一个出现一次，其余出现三次。O(n) 时间，O(1) 空间"""
    ones, twos = 0, 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones


# ===== 进阶: #260 两个数各出现一次，其余出现两次 =====
def single_number_iii(nums: list) -> list:
    """找出两个只出现一次的数字"""
    xor_all = 0
    for num in nums:
        xor_all ^= num
    # xor_all = a ^ b，找到任意一位不同（两个数该位不同）
    diff_bit = xor_all & (-xor_all)  # 取最低位的1
    a = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
    return sorted([a, xor_all ^ a])


# ===== 测试 =====
if __name__ == "__main__":
    for func in [single_number_xor, single_number_reduce, single_number_math]:
        assert func([2, 2, 1]) == 1
        assert func([4, 1, 2, 1, 2]) == 4
        assert func([1]) == 1
        assert func([0, 0, 5]) == 5

    # #137 测试
    assert single_number_ii([2, 2, 3, 2]) == 3
    assert single_number_ii([0, 1, 0, 1, 0, 1, 99]) == 99

    # #260 测试
    assert single_number_iii([1, 2, 1, 3, 2, 5]) == [3, 5]
    assert single_number_iii([-1, 0]) == [-1, 0]
    assert single_number_iii([0, 1]) == [0, 1]

    print("All tests passed!")
