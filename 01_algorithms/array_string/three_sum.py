"""
题目：三数之和
难度：Medium | 高频出现：字节/阿里/腾讯
标签：数组、双指针、排序
LeetCode：#15


题目描述
---------
给你一个整数数组 nums，判断是否存在三元组 [nums[i], nums[j], nums[k]]
满足 i != j、i != k 且 j != k，同时还满足 nums[i] + nums[j] + nums[k] == 0。
返回所有和为 0 且不重复的三元组（顺序不限，但结果不能有重复三元组）。

示例
------
输入: nums = [-1, 0, 1, 2, -1, -4]
输出: [[-1, -1, 2], [-1, 0, 1]]

输入: nums = [0, 1, 1]
输出: []

约束
------
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

TL;DR（30秒速览）
- 思路：排序后，固定一个数 nums[i]，对右侧区间用双指针夹逼
- 时间：O(n²)  空间：O(1)（不计返回值）
- 陷阱：结果去重——固定数跳过重复，双指针收缩后也要跳过重复

详细解析
---------
暴力法：三重循环 O(n³)，加 set 去重，面试不可接受。

排序 + 双指针（最优）：
  1. 先排序，使相同元素相邻，便于跳过重复。
  2. 外层枚举 i（0 ~ n-3）；若 nums[i] > 0 则后续不可能凑成 0，直接 break。
  3. 若 nums[i] == nums[i-1]（i>0），跳过，避免重复三元组。
  4. 内层：left=i+1, right=n-1，计算 s = nums[i]+nums[left]+nums[right]：
       - s == 0：记录，然后 left 右移跳重复，right 左移跳重复；
       - s < 0：left 右移（需要更大值）；
       - s > 0：right 左移（需要更小值）。

哈希表法：外层两重循环枚举两数，第三数查哈希 O(n²) 但常数更大，且去重较复杂，不推荐。
"""

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # 最小值已大于 0，不可能凑成 0
        if nums[i] > 0:
            break
        # 跳过重复的固定数
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                # 跳过左侧重复
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # 跳过右侧重复
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1

    return result


if __name__ == "__main__":
    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == sorted([[-1, -1, 2], [-1, 0, 1]])
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([]) == []
    assert three_sum([-2, 0, 1, 1, 2]) == [[-2, 0, 2], [-2, 1, 1]]
    print("All tests passed.")
