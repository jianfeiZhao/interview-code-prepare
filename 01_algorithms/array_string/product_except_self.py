"""
题目：除自身以外数组的乘积
难度：Medium | 高频出现：字节/腾讯/亚马逊/微软
标签：数组、前缀积、后缀积
LeetCode：#238


题目描述
---------
给你一个整数数组 nums，返回数组 answer，其中 answer[i] 等于 nums 中除
nums[i] 之外其余各元素的乘积。保证数组中任何前缀或后缀的乘积都在 32 位
整数范围内。不能使用除法，且在 O(n) 时间复杂度内完成。

示例
------
输入: nums = [1, 2, 3, 4]
输出: [24, 12, 8, 6]

输入: nums = [-1, 1, 0, -3, 3]
输出: [0, 0, 9, 0, 0]

约束
------
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- 题目保证 answer[i] 不会溢出 32 位整数

TL;DR（30秒速览）
- 思路：前缀积 × 后缀积，answer[i] = left_product[i] * right_product[i]
- 时间：O(n)  空间：O(1)（输出数组不计入额外空间）
- 陷阱：题目要求不使用除法；处理含 0 的情况时除法更麻烦，前后缀积天然正确

详细解析
---------
暴力法：对每个位置计算其余所有元素的乘积，O(n²)，不可接受。

除法法：总乘积除以 nums[i]，但题目明确禁止，且需特判 0。

前缀积 + 后缀积（标准解）：
  - left[i]  = nums[0] * nums[1] * ... * nums[i-1]（i 左侧所有元素乘积）
  - right[i] = nums[i+1] * ... * nums[n-1]（i 右侧所有元素乘积）
  - answer[i] = left[i] * right[i]

空间优化：
  - 先用 answer 数组存前缀积（从左向右），
    再用一个变量 R 从右向右遍历，边累积后缀积边乘进 answer。
  - 额外空间 O(1)（不含输出数组）。
"""

from typing import List


def product_except_self(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = [1] * n

    # 第一步：answer[i] 存 i 左侧所有元素的乘积
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # 第二步：从右向左，用 suffix 累积右侧乘积并乘进 answer
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert product_except_self([2, 3]) == [3, 2]
    assert product_except_self([0, 0]) == [0, 0]
    assert product_except_self([1, 0]) == [0, 1]
    print("All tests passed.")
