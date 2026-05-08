"""
题目: 寻找两个正序数组的中位数
LeetCode: #4 (Hard)
高频公司: 字节跳动、阿里巴巴、腾讯（超高频必考）

题目描述:
给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。
请你找出并返回这两个正序数组的中位数。
算法的时间复杂度应该为 O(log (m+n))。

示例 1: nums1 = [1,3], nums2 = [2] -> 2.0
示例 2: nums1 = [1,2], nums2 = [3,4] -> 2.5
示例 3: nums1 = [], nums2 = [1] -> 1.0

================================================================================
TL;DR (核心思路):

方法1 (O(log(m+n))): 二分切割
  - 在较短数组上二分，找切割点 i，使得 nums1[:i] + nums2[:j] 构成左半部分
  - 切割条件: 满足 nums1[i-1] <= nums2[j] 且 nums2[j-1] <= nums1[i]
  - 中位数 = (max(左半) + min(右半)) / 2

方法2 (O(log(m+n))): 转化为找第 k 小问题
  - findKth(nums1, nums2, k)：每次排除 k//2 个肯定不是第 k 小的元素

时间复杂度: O(log(min(m,n)))  [方法1]
空间复杂度: O(1)
================================================================================
"""

from typing import List


# ===================== 方法1: 二分切割（标准解）=====================

def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    """
    在两个有序数组上做二分切割找中位数。

    核心思想：
    找一个切割位置，将两个数组合并成左右两半，左半部分的最大值 <= 右半部分的最小值。
    设 nums1 切割位置为 i，nums2 切割位置为 j：
      - 左半: nums1[:i] + nums2[:j]，共 (m+n)//2 个元素（向上取整偶数情况）
      - j = half_len - i

    合法切割条件：
      - nums1[i-1] <= nums2[j]（nums1 左半最大 <= nums2 右半最小）
      - nums2[j-1] <= nums1[i]（nums2 左半最大 <= nums1 右半最小）
    """
    # 确保 nums1 是较短的数组，减少二分范围
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2  # 左半部分的元素总数（奇数时多一个）

    left, right = 0, m  # i 的范围 [0, m]，0 表示 nums1 全在右半，m 表示全在左半

    while left <= right:
        i = left + (right - left) // 2  # nums1 的切割点（左半包含 nums1[:i]）
        j = half_len - i                # nums2 的切割点（左半包含 nums2[:j]）

        # 用 -inf/+inf 处理边界
        nums1_left_max  = float('-inf') if i == 0 else nums1[i - 1]
        nums1_right_min = float('inf')  if i == m else nums1[i]
        nums2_left_max  = float('-inf') if j == 0 else nums2[j - 1]
        nums2_right_min = float('inf')  if j == n else nums2[j]

        if nums1_left_max <= nums2_right_min and nums2_left_max <= nums1_right_min:
            # 找到合法切割
            max_left  = max(nums1_left_max, nums2_left_max)
            min_right = min(nums1_right_min, nums2_right_min)

            if (m + n) % 2 == 1:
                return float(max_left)       # 奇数：左半多一个，中位数就是左半最大
            else:
                return (max_left + min_right) / 2.0  # 偶数：两个中间值的平均

        elif nums1_left_max > nums2_right_min:
            # nums1 左半太大，i 需要减小
            right = i - 1
        else:
            # nums2 左半太大，i 需要增大
            left = i + 1

    return 0.0  # 不应到达此处


# ===================== 方法2: 转化为第 k 小问题 =====================

def findMedianSortedArrays_kth(nums1: List[int], nums2: List[int]) -> float:
    """
    将中位数问题转化为"找第 k 小元素"。
    递归每次排除 k//2 个元素。
    """
    m, n = len(nums1), len(nums2)
    total = m + n

    def findKth(a: List[int], b: List[int], k: int) -> int:
        """在两个有序数组 a, b 中找第 k 小的元素（1-indexed）。"""
        if not a:
            return b[k - 1]
        if not b:
            return a[k - 1]
        if k == 1:
            return min(a[0], b[0])

        # 比较两个数组各自第 k//2 小的元素
        half = k // 2
        # 防止越界：取 min(half, len(a/b))
        pa = min(half, len(a))
        pb = min(half, len(b))

        if a[pa - 1] <= b[pb - 1]:
            # a 的前 pa 个元素都不可能是第 k 小，排除
            return findKth(a[pa:], b, k - pa)
        else:
            # b 的前 pb 个元素都不可能是第 k 小，排除
            return findKth(a, b[pb:], k - pb)

    if total % 2 == 1:
        return float(findKth(nums1, nums2, total // 2 + 1))
    else:
        left  = findKth(nums1, nums2, total // 2)
        right = findKth(nums1, nums2, total // 2 + 1)
        return (left + right) / 2.0


# ===================== 方法3: 暴力合并（O(m+n)，用于验证）=====================

def findMedianSortedArrays_brute(nums1: List[int], nums2: List[int]) -> float:
    """合并后取中位数，O(m+n) 时间，仅用于测试验证。"""
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    else:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    test_cases = [
        ([1, 3], [2], 2.0),
        ([1, 2], [3, 4], 2.5),
        ([], [1], 1.0),
        ([2], [], 2.0),
        ([0, 0], [0, 0], 0.0),
        ([1], [2, 3, 4, 5, 6], 3.5),
        ([1, 2], [3], 2.0),
        ([1, 3, 5, 7, 9], [2, 4, 6, 8, 10], 5.5),
        ([1], [1], 1.0),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 3.0),
        ([], [2, 3], 2.5),
        ([1, 2, 3], [4, 5, 6, 7, 8], 4.5),
    ]

    for nums1, nums2, expected in test_cases:
        r1 = findMedianSortedArrays(nums1, nums2)
        r2 = findMedianSortedArrays_kth(nums1, nums2)
        r3 = findMedianSortedArrays_brute(nums1, nums2)

        assert abs(r1 - expected) < 1e-9, f"binary: nums1={nums1}, nums2={nums2}, got={r1}, expected={expected}"
        assert abs(r2 - expected) < 1e-9, f"kth: nums1={nums1}, nums2={nums2}, got={r2}, expected={expected}"
        assert abs(r3 - expected) < 1e-9, f"brute: nums1={nums1}, nums2={nums2}, got={r3}, expected={expected}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"[1,3] + [2]: {findMedianSortedArrays([1,3], [2])}")       # 2.0
    print(f"[1,2] + [3,4]: {findMedianSortedArrays([1,2], [3,4])}")   # 2.5
    print(f"[] + [1]: {findMedianSortedArrays([], [1])}")              # 1.0
    print(f"[1,2,3,4,5] + [1,2,3,4,5]: {findMedianSortedArrays([1,2,3,4,5], [1,2,3,4,5])}")  # 3.0
