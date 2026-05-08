"""
LeetCode #268 - 缺失数字 (Missing Number)
难度: Easy | 频率: 全系

=== 题目描述 ===
给定一个包含 [0, n] 中 n 个数的数组 nums，找出 [0, n] 这个范围内没有出现在数组中的那个数。

示例 1: 输入: nums = [3,0,1]    输出: 2
示例 2: 输入: nums = [0,1]      输出: 2
示例 3: 输入: nums = [9,6,4,2,3,5,7,0,1]  输出: 8

进阶: 实现线性时间复杂度、仅用额外常数空间的算法解决此问题。

=== TL;DR ===
核心思路:
  方法1（数学）: 利用等差数列求和公式，期望总和 - 实际总和 = 缺失的数
    期望总和 = n*(n+1)/2 — O(n) 时间，O(1) 空间
  方法2（异或）: 利用 a^a=0，将索引和值全部异或，剩余值即缺失数 — O(n) 时间，O(1) 空间
  方法3（哈希/集合）: O(n) 时间，O(n) 空间
  方法4（排序）: O(n log n) 时间，O(1) 空间

时间复杂度: O(n)
空间复杂度: O(1)

=== 详细解析 ===
关键技巧:
1. 数学法: missing = n*(n+1)//2 - sum(nums)，利用高斯求和公式
2. 异或法: 将 0,1,...,n 与 nums 中每个元素全部异或，相同元素两两抵消，剩下缺失的
   missing = 0 ^ 1 ^ 2 ^ ... ^ n ^ nums[0] ^ nums[1] ^ ... ^ nums[n-1]
3. 异或法初始化 missing = n（最后一个索引），然后从 0 到 n-1 依次对 i 和 nums[i] 异或
4. 数学法需注意大数溢出（Python不需要，Java/C++需要用long）
"""


# ===== 方法1: 数学（高斯求和）=====
def missing_number_math(nums: list) -> int:
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)


# ===== 方法2: 异或（位运算）=====
def missing_number_xor(nums: list) -> int:
    missing = len(nums)  # 先初始化为 n（代表下标 n）
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing


# ===== 方法3: 集合 =====
def missing_number_set(nums: list) -> int:
    s = set(nums)
    for i in range(len(nums) + 1):
        if i not in s:
            return i
    return -1


# ===== 方法4: 排序 =====
def missing_number_sort(nums: list) -> int:
    nums.sort()
    for i, num in enumerate(nums):
        if i != num:
            return i
    return len(nums)


# ===== 测试 =====
if __name__ == "__main__":
    funcs = [
        missing_number_math,
        missing_number_xor,
        missing_number_set,
        missing_number_sort,
    ]
    cases = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        ([0], 1),
        ([1], 0),
        ([0, 2, 3], 1),
    ]
    for func in funcs:
        for nums, expected in cases:
            assert func(list(nums)) == expected, \
                f"{func.__name__}({nums}) = {func(list(nums))}, expected {expected}"

    print("All tests passed!")
