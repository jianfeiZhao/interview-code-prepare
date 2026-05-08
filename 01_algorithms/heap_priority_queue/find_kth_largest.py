"""
题目: 数组中第K个最大元素（堆 + 快速选择）
LeetCode: #215 (Medium)
高频公司: 字节跳动、腾讯、阿里巴巴（必考）

题目描述:
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

示例 1: nums = [3,2,1,5,6,4], k = 2 -> 5
示例 2: nums = [3,2,3,1,2,4,5,5,6], k = 4 -> 4

================================================================================
TL;DR:

方法1 - 小顶堆（推荐面试）:
  - 维护大小为 k 的小顶堆，遍历数组，堆满后若当前元素 > 堆顶则替换
  - 最终堆顶即为第 k 大元素
  时间: O(n log k)，空间: O(k)

方法2 - 快速选择（最优平均，O(n)）:
  - 基于快排 partition，每次只递归包含目标的一半
  - pivot 落在第 n-k 位时即找到答案（从0开始计数）
  时间: 平均 O(n)，最坏 O(n^2)，空间: O(1) 原地

方法3 - 排序（简单但不满足要求）:
  - 直接排序取 nums[-k]，O(n log n)，仅作对照
================================================================================
"""

import heapq
import random
from typing import List


# ===================== 方法1: 小顶堆（面试首选）=====================

def findKthLargest_heap(nums: List[int], k: int) -> int:
    """
    维护大小为 k 的小顶堆。
    堆中始终保存遍历过的最大的 k 个元素，堆顶是这 k 个中最小的，即第 k 大。
    """
    heap = []  # Python heapq 是小顶堆

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # 弹出最小的，保证堆中只有最大的 k 个

    return heap[0]  # 堆顶即第 k 大


def findKthLargest_heap_nlargest(nums: List[int], k: int) -> int:
    """使用 heapq.nlargest，一行搞定（底层同小顶堆）。"""
    return heapq.nlargest(k, nums)[-1]


# ===================== 方法2: 快速选择（最优平均复杂度）=====================

def findKthLargest_quickselect(nums: List[int], k: int) -> int:
    """
    快速选择算法（基于快排 partition）。
    第 k 大 = 从右往左第 k 个 = 从左往右第 n-k 个（0-indexed: n-k）。
    """
    target = len(nums) - k  # 目标索引（第 k 大 = 倒数第 k 个）

    def quickselect(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        # 随机选 pivot 避免最坏情况（有序数组）
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]

        # partition：将小于 pivot 的元素移到左边
        store = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1

        # pivot 放到最终位置
        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            return quickselect(store + 1, right)  # 目标在右侧
        else:
            return quickselect(left, store - 1)   # 目标在左侧

    return quickselect(0, len(nums) - 1)


def findKthLargest_quickselect_iterative(nums: List[int], k: int) -> int:
    """
    迭代版快速选择（避免递归栈溢出）。
    """
    nums = nums[:]  # 不修改原数组
    target = len(nums) - k
    left, right = 0, len(nums) - 1

    while left < right:
        # 随机 pivot
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]

        store = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            left = store + 1
        else:
            right = store - 1

    return nums[left]


# ===================== 方法3: 排序（对照用）=====================

def findKthLargest_sort(nums: List[int], k: int) -> int:
    """直接排序，O(n log n)，仅作对照。"""
    return sorted(nums, reverse=True)[k - 1]


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([2, 1], 1, 2),
        ([2, 1], 2, 1),
        ([1, 1, 1, 1], 2, 1),
        (list(range(1, 11)), 3, 8),    # [1..10], k=3 -> 8
        (list(range(10, 0, -1)), 5, 6), # 逆序 [10..1], k=5 -> 6
    ]

    for nums, k, expected in test_cases:
        r1 = findKthLargest_heap(nums[:], k)
        r2 = findKthLargest_quickselect(nums[:], k)
        r3 = findKthLargest_sort(nums[:], k)
        r4 = findKthLargest_heap_nlargest(nums[:], k)
        r5 = findKthLargest_quickselect_iterative(nums[:], k)

        assert r1 == expected, f"heap: nums={nums}, k={k}, got={r1}"
        assert r2 == expected, f"quickselect: nums={nums}, k={k}, got={r2}"
        assert r3 == expected, f"sort: nums={nums}, k={k}, got={r3}"
        assert r4 == expected, f"nlargest: nums={nums}, k={k}, got={r4}"
        assert r5 == expected, f"quickselect_iter: nums={nums}, k={k}, got={r5}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"[3,2,1,5,6,4], k=2: {findKthLargest_heap([3,2,1,5,6,4], 2)}")      # 5
    print(f"[3,2,3,1,2,4,5,5,6], k=4: {findKthLargest_heap([3,2,3,1,2,4,5,5,6], 4)}")  # 4

    print(f"\n复杂度对比:")
    print(f"  小顶堆:   时间 O(n log k)，空间 O(k)，稳定")
    print(f"  快速选择: 时间 O(n) 平均，空间 O(1)，最坏 O(n^2)")
    print(f"  排序:     时间 O(n log n)，不满足题目要求")
