"""
题目：子集
难度：Medium | 高频出现：字节/阿里
标签：回溯、位运算
LeetCode：#78

题目描述
---------
给定一个不含重复元素的整数数组 nums，返回其所有可能的子集（幂集）。
解集中不能包含重复的子集，返回的结果集可以按任意顺序排列。
共有 2ⁿ 个子集，包含空集和数组本身。

示例
------
输入: nums = [1, 2, 3]
输出: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

输入: nums = [0]
输出: [[], [0]]

约束
------
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- nums 中的所有元素互不相同

TL;DR（30秒速览）
- 思路：回溯，每步选择从 start 开始的元素，每次进入函数都收集当前路径
- 时间：O(n × 2ⁿ)  空间：O(n)
- 关键：与全排列区别在于：每次从 i+1 开始（避免重复），且每层都收集答案

详细解析
---------
方法1 - 回溯（推荐）：
  start 控制遍历起点，避免重复组合
  每进入一次 backtrack 即收集当前 path（包括空集）

方法2 - 位运算：
  n 个元素 → 2ⁿ 个子集
  用 0 到 2ⁿ-1 的二进制数，第 i 位为 1 表示选第 i 个元素

方法3 - 迭代：
  初始 [[]]，逐个添加新元素时，对已有所有子集各复制一份并加入新元素
"""

from typing import List


def subsets_backtrack(nums: List[int]) -> List[List[int]]:
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result


def subsets_bitmask(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


def subsets_iterative(nums: List[int]) -> List[List[int]]:
    result = [[]]
    for num in nums:
        result += [sub + [num] for sub in result]
    return result


if __name__ == "__main__":
    expected = sorted([[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]])
    assert sorted(subsets_backtrack([1,2,3])) == expected
    assert sorted(subsets_bitmask([1,2,3])) == expected
    assert sorted(subsets_iterative([1,2,3])) == expected
    print("All tests passed.")
