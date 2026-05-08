"""
题目：全排列
难度：Medium | 高频出现：字节/腾讯
标签：回溯、递归
LeetCode：#46


题目描述
---------
给定一个不含重复数字的数组 nums，返回其所有可能的全排列，顺序不限。

示例
------
输入: nums = [1,2,3]
输出: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

输入: nums = [0,1]
输出: [[0,1],[1,0]]

约束
------
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10，nums 中所有整数互不相同

TL;DR（30秒速览）
- 思路：回溯模板，used 数组标记已选元素，path 满了则收集结果
- 时间：O(n × n!)  空间：O(n)（递归栈+used数组）
- 陷阱：回溯时务必撤销选择（used[i]=False, path.pop()）

详细解析
---------
回溯通用模板：
  做选择 → 递归 → 撤销选择

全排列：每次从未使用的元素中选一个加入 path
  path 长度 == n 时收集答案

有重复元素版本 (LeetCode #47)：
  先排序，再加 if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(num)
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


def permute_swap(nums: List[int]) -> List[List[int]]:
    """交换法：通过交换位置实现，不需要 used 数组"""
    result = []
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    backtrack(0)
    return result


if __name__ == "__main__":
    res = permute([1, 2, 3])
    assert len(res) == 6
    assert sorted(res) == sorted([[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]])

    res = permute_swap([1, 2, 3])
    assert len(res) == 6
    print("All tests passed.")
