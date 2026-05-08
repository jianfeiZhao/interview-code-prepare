"""
题目：数组中重复的数据 + 消失的数字
难度：Medium | 高频出现：字节/阿里
标签：数组、原地哈希
LeetCode：#442 数组中重复的数据，#448 找到所有数组中消失的数字


题目描述
---------
给你一个长度为 n 的整数数组 nums，其中 nums 的所有整数都在范围 [1, n] 内，
且每个整数出现最多两次。找出所有出现两次的整数，并以数组形式返回。
要求 O(n) 时间复杂度，O(1) 额外空间（不包括返回值）。

示例
------
输入: nums = [4,3,2,7,8,2,3,1]
输出: [2,3]

输入: nums = [1,1,2]
输出: [1]

约束
------
- n == nums.length，1 <= n <= 10^5
- 1 <= nums[i] <= n
- 每个元素出现一次或两次

TL;DR（30秒速览）
- 利用数组下标作为哈希：将 nums[i] 对应位置的数取负，第二次遇到时说明重复
- 时间 O(n)，空间 O(1)（不含输出）

详细解析
---------
原地标记法：
  遍历每个 num，将 nums[abs(num)-1] 取负
  若该位置已为负，说明 abs(num) 重复出现

#448 消失的数字：
  同理，标记后扫描正数位置，其下标+1即为消失的数字
"""

from typing import List


def find_duplicates(nums: List[int]) -> List[int]:
    result = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] = -nums[idx]
    return result


def find_disappeared_numbers(nums: List[int]) -> List[int]:
    for num in nums:
        idx = abs(num) - 1
        nums[idx] = -abs(nums[idx])
    return [i + 1 for i, v in enumerate(nums) if v > 0]


if __name__ == "__main__":
    assert sorted(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1])) == [2, 3]
    assert sorted(find_duplicates([1, 1, 2])) == [1]

    assert sorted(find_disappeared_numbers([4, 3, 2, 7, 8, 2, 3, 1])) == [5, 6]
    assert sorted(find_disappeared_numbers([1, 1])) == [2]
    print("All tests passed.")
