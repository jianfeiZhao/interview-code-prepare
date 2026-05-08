"""
题目：搜索插入位置
难度：Easy | 高频出现：字节/阿里/腾讯
标签：数组、二分查找
LeetCode：#35 Search Insert Position


题目描述
---------
给定一个排序数组和一个目标值，在数组中找到目标值并返回其索引。
如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
请使用时间复杂度为 O(log n) 的算法。

示例
------
输入: nums = [1,3,5,6], target = 5
输出: 2

输入: nums = [1,3,5,6], target = 2
输出: 1

输入: nums = [1,3,5,6], target = 7
输出: 4

约束
------
- 1 <= nums.length <= 10^4，-10^4 <= nums[i] <= 10^4
- nums 为无重复元素的升序排列数组

TL;DR（30秒速览）
- 核心思路：标准二分，找第一个 >= target 的下标（lower_bound 模板）
- 时间 O(log n)，空间 O(1)
- 关键陷阱：循环结束时 left 即为答案，无需额外判断；右边界取 n（不是 n-1）

详细解析
---------
lower_bound 模板（左闭右开 [left, right)）：
  - 初始化：left=0, right=len(nums)（开区间上界）
  - 循环条件：left < right
  - 中间值：mid = (left + right) // 2
  - 收缩：
    - nums[mid] < target：left = mid + 1
    - nums[mid] >= target：right = mid
  - 终止时 left == right，即为插入位置

为什么 right=n 而非 n-1？
  target 大于所有元素时，插入位置为 n，需要右边界能覆盖到 n。

扩展：
  - upper_bound（第一个 > target 的位置）：将 < 改为 <=
  - Python 标准库：bisect.bisect_left(nums, target) 等价本题
"""

from typing import List
import bisect


def search_insert(nums: List[int], target: int) -> int:
    """
    方法一：手写 lower_bound，O(log n) 时间，O(1) 空间。
    返回第一个 >= target 的下标，即插入位置。
    """
    left, right = 0, len(nums)          # 右边界为 n（开区间）

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1              # target 在右半段
        else:
            right = mid                 # nums[mid] >= target，收缩右边界

    return left                         # 终止时 left == right == 插入位置


def search_insert_bisect(nums: List[int], target: int) -> int:
    """
    方法二：利用 Python 标准库 bisect_left，面试中可提但需会手写。
    bisect_left 等价 lower_bound：找第一个 >= target 的位置。
    """
    return bisect.bisect_left(nums, target)


def search_insert_verbose(nums: List[int], target: int) -> int:
    """
    方法三：普通二分（更直观，适合初学），找到直接返回，找不到返回 left。
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # 循环结束：left > right，left 即为插入位置
    return left


if __name__ == "__main__":
    # 目标值存在
    assert search_insert([1, 3, 5, 6], 5) == 2
    assert search_insert([1, 3, 5, 6], 1) == 0
    assert search_insert([1, 3, 5, 6], 6) == 3

    # 目标值不存在
    assert search_insert([1, 3, 5, 6], 2) == 1   # 插入在 index 1
    assert search_insert([1, 3, 5, 6], 7) == 4   # 插入在末尾
    assert search_insert([1, 3, 5, 6], 0) == 0   # 插入在头部

    # 验证三种方法结果一致
    for nums, target in [([1,3,5,6], 5), ([1,3,5,6], 2), ([1,3,5,6], 7)]:
        assert search_insert(nums, target) == search_insert_bisect(nums, target) \
               == search_insert_verbose(nums, target)

    # 单元素
    assert search_insert([1], 0) == 0
    assert search_insert([1], 1) == 0
    assert search_insert([1], 2) == 1

    print("All tests passed.")
