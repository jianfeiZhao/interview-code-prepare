"""
题目: 寻找旋转排序数组的最小值
LeetCode: #153 (Medium)
高频公司: 字节跳动、阿里巴巴

题目描述:
已知一个长度为 n 的数组，预先按照升序排列，经由 1 到 n 次旋转后，得到输入数组。
例如，原数组 nums = [0,1,2,4,5,6,7] 在变化后可能得到：
  - 若旋转 4 次，则可以得到 [4,5,6,7,0,1,2]
  - 若旋转 7 次，则可以得到 [0,1,2,4,5,6,7]

给你一个元素值互不相同的数组 nums，它原来是一个升序排列的数组，并按上述情形进行了多次旋转。
请你找出并返回数组中的最小元素。你必须设计一个时间复杂度为 O(log n) 的算法解决此问题。

示例 1: nums = [3,4,5,1,2] -> 1
示例 2: nums = [4,5,6,7,0,1,2] -> 0
示例 3: nums = [11,13,15,17] -> 17

================================================================================
TL;DR (核心思路):
  - 二分搜索：比较 mid 和右边界 right 的大小关系
  - 若 nums[mid] > nums[right]：最小值在右半部分，left = mid + 1
  - 若 nums[mid] < nums[right]：最小值在左半部分（含 mid），right = mid
  - 循环直到 left == right，此时 nums[left] 即为最小值

时间复杂度: O(log n)
空间复杂度: O(1)
================================================================================
"""

from typing import List


def findMin(nums: List[int]) -> int:
    """
    二分搜索寻找旋转数组最小值。

    关键洞察：旋转数组可分为两段有序子数组，最小值是右段的起点。
    通过比较 mid 和 right 来缩小范围：
    - 若 nums[mid] > nums[right]：mid 在左段，最小值在 [mid+1, right]
    - 若 nums[mid] < nums[right]：mid 在右段（或数组未旋转），最小值在 [left, mid]
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2  # 防溢出写法

        if nums[mid] > nums[right]:
            # mid 落在左段（较大的那段），最小值必在 mid 右侧
            left = mid + 1
        else:
            # mid 落在右段（较小的那段），最小值在 mid 或其左侧
            right = mid

    return nums[left]


def findMin_verbose(nums: List[int]) -> int:
    """带详细注释的版本，便于理解每一步决策。"""
    left, right = 0, len(nums) - 1

    # 如果数组没有旋转（或旋转了一整圈），第一个元素最小
    # 这个条件可以省略，但有助于理解
    # if nums[left] <= nums[right]:
    #     return nums[left]

    while left < right:
        mid = left + (right - left) // 2

        # 例: [4,5,6,7,0,1,2], left=0, right=6, mid=3
        # nums[3]=7 > nums[6]=2，说明最小值在 [4,6] 即 [0,1,2] 部分
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            # 例: [4,5,6,7,0,1,2], left=4, right=6, mid=5
            # nums[5]=1 < nums[6]=2，说明最小值在 [4,5] 部分
            right = mid

    return nums[left]


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试用例
    assert findMin([3, 4, 5, 1, 2]) == 1, "旋转3次"
    assert findMin([4, 5, 6, 7, 0, 1, 2]) == 0, "旋转4次"
    assert findMin([11, 13, 15, 17]) == 11, "未旋转（或旋转n次）"
    assert findMin([1]) == 1, "单元素"
    assert findMin([2, 1]) == 1, "两元素旋转"
    assert findMin([1, 2]) == 1, "两元素未旋转"
    assert findMin([5, 1, 2, 3, 4]) == 1, "旋转到第2位"
    assert findMin([2, 3, 4, 5, 1]) == 1, "旋转到末尾"

    # 两种版本结果一致
    test_cases = [
        [3, 4, 5, 1, 2],
        [4, 5, 6, 7, 0, 1, 2],
        [11, 13, 15, 17],
        [5, 1, 2, 3, 4],
    ]
    for tc in test_cases:
        assert findMin(tc) == findMin_verbose(tc), f"两版本结果不一致: {tc}"

    print("所有测试通过!")

    # 打印示例结果，直观验证
    print(f"[3,4,5,1,2] 最小值: {findMin([3,4,5,1,2])}")          # 1
    print(f"[4,5,6,7,0,1,2] 最小值: {findMin([4,5,6,7,0,1,2])}")  # 0
    print(f"[11,13,15,17] 最小值: {findMin([11,13,15,17])}")       # 11
