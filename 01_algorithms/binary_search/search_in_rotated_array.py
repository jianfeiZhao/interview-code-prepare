"""
题目：搜索旋转排序数组
难度：Medium | 高频出现：字节/阿里
标签：二分查找
LeetCode：#33


题目描述
---------
整数数组 nums 按升序排列，数组中的值互不相同。但在传递给函数之前，
nums 在预先未知的某个下标 k 上进行了旋转（例如 [0,1,2,4,5,6,7] 旋转后得到 [4,5,6,7,0,1,2]）。
给你旋转后的数组 nums 和整数 target，如果 nums 中存在 target 则返回其下标，否则返回 -1。
必须使用时间复杂度 O(log n) 的算法解决此问题。

示例
------
输入: nums = [4,5,6,7,0,1,2], target = 0
输出: 4

输入: nums = [4,5,6,7,0,1,2], target = 3
输出: -1

约束
------
- 1 <= nums.length <= 5000，-10^4 <= nums[i], target <= 10^4

TL;DR（30秒速览）
- 思路：标准二分，每次判断 mid 落在左半段还是右半段有序区域
- 时间：O(log n)  空间：O(1)
- 陷阱：先判断哪半段有序，再判断 target 是否在有序段内，共4种情况

详细解析
---------
旋转数组 [4,5,6,7,0,1,2]，每次 mid 必定有一侧是有序的。
判断逻辑（以 nums[left] <= nums[mid] 为"左侧有序"）：

情况一：左侧有序 nums[left] <= nums[mid]
  若 nums[left] <= target < nums[mid] → 收缩右边界（target在左侧有序区）
  否则 → 收缩左边界（target在右侧）

情况二：右侧有序 nums[mid] < nums[right]
  若 nums[mid] < target <= nums[right] → 收缩左边界（target在右侧有序区）
  否则 → 收缩右边界
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # 左侧有序
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # 右侧有序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


if __name__ == "__main__":
    assert search([4,5,6,7,0,1,2], 0) == 4
    assert search([4,5,6,7,0,1,2], 3) == -1
    assert search([1], 0) == -1
    assert search([1,3], 3) == 1
    print("All tests passed.")
