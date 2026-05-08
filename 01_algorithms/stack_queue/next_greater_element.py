"""
LeetCode #496 + #503 - 下一个更大元素 I + II
难度: Easy(#496) + Medium(#503) | 频率: 字节

=== 题目描述 ===
【#496 - 下一个更大元素 I】
给你两个没有重复元素的数组 nums1 和 nums2，其中 nums1 是 nums2 的子集。
请你找出 nums1 中每个元素在 nums2 中的下一个比其大的值。
返回一个长度为 nums1.length 的数组。若没有则填 -1。

示例: nums1 = [4,1,2], nums2 = [1,3,4,2]
     输出: [-1,3,-1]  (4无更大, 1的下一更大是3, 2无更大)

【#503 - 下一个更大元素 II】
给定一个循环数组（最后一个元素的下一个元素是数组的第一个元素），
输出每个元素的下一个更大元素。若不存在则输出 -1。

示例: nums = [1,2,1]  输出: [2,-1,2]

=== TL;DR ===
核心思路（单调栈）:
  #496: 对 nums2 用单调栈求每个元素的下一个更大值，存入哈希表，再查询 nums1 中每个元素
  #503: 对数组遍历两遍（模拟循环），用 i % n 处理索引

时间复杂度: O(m+n)（#496），O(n)（#503）
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. #496: 单调栈只对 nums2 跑一次，结果存到 {val: next_greater} 哈希表，O(1) 查询
2. #503 循环数组: 遍历两遍，i 从 0 到 2n-1，实际下标用 i % n
   第一遍建栈，第二遍用于让第一遍剩余的元素找到答案（模拟"循环"的效果）
3. 初始化 result = [-1] * n，未被更新的保持 -1
4. 单调栈通用模板: 见 daily_temperatures.py
"""


# ===== #496: 下一个更大元素 I =====
def next_greater_element_i(nums1: list, nums2: list) -> list:
    # 对 nums2 建立 val->下一个更大值 的映射
    next_greater = {}
    stack = []  # 单调递减栈

    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    # 栈中剩余元素没有更大值，默认 -1

    return [next_greater.get(x, -1) for x in nums1]


# ===== #503: 下一个更大元素 II（循环数组）=====
def next_greater_element_ii(nums: list) -> list:
    n = len(nums)
    result = [-1] * n
    stack = []  # 存下标

    # 遍历两遍模拟循环
    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        if i < n:
            stack.append(idx)  # 只在第一遍入栈（避免重复入栈）

    return result


# ===== 暴力版（用于对比）=====
def next_greater_element_i_brute(nums1: list, nums2: list) -> list:
    result = []
    for x in nums1:
        idx = nums2.index(x)
        found = -1
        for j in range(idx + 1, len(nums2)):
            if nums2[j] > x:
                found = nums2[j]
                break
        result.append(found)
    return result


def next_greater_element_ii_brute(nums: list) -> list:
    n = len(nums)
    result = []
    for i in range(n):
        found = -1
        for step in range(1, n):
            j = (i + step) % n
            if nums[j] > nums[i]:
                found = nums[j]
                break
        result.append(found)
    return result


# ===== 测试 =====
if __name__ == "__main__":
    # #496 测试
    i_cases = [
        ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
        ([2, 4], [1, 2, 3, 4], [3, -1]),
        ([1], [1, 2], [2]),
        ([1], [1], [-1]),
    ]
    for func in [next_greater_element_i, next_greater_element_i_brute]:
        for nums1, nums2, expected in i_cases:
            result = func(list(nums1), list(nums2))
            assert result == expected, \
                f"{func.__name__}({nums1}, {nums2}) = {result}, expected {expected}"

    # #503 测试
    ii_cases = [
        ([1, 2, 1], [2, -1, 2]),
        ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]),
        ([5, 4, 3, 2, 1], [-1, 5, 5, 5, 5]),
        ([1], [-1]),
        ([1, 1, 1, 1], [-1, -1, -1, -1]),
    ]
    for func in [next_greater_element_ii, next_greater_element_ii_brute]:
        for nums, expected in ii_cases:
            result = func(list(nums))
            assert result == expected, \
                f"{func.__name__}({nums}) = {result}, expected {expected}"

    print("All tests passed!")
