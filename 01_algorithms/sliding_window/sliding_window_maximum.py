"""
题目: 滑动窗口最大值（单调队列）
LeetCode: #239 (Hard)
高频公司: 字节跳动、阿里巴巴

题目描述:
给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。
你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
返回滑动窗口中的最大值数组。

示例: nums = [1,3,-1,-3,5,3,6,7], k = 3 -> [3,3,5,5,6,7]
  窗口 [1,3,-1] max=3, [3,-1,-3] max=3, [-1,-3,5] max=5,
       [-3,5,3] max=5, [5,3,6] max=6, [3,6,7] max=7

================================================================================
TL;DR（核心思路）:
- 单调递减双端队列（存下标），队头始终是窗口内最大值的下标
- 每次新元素入队：先从队尾弹出所有比当前值小的下标（它们不可能是最大值了）
- 每次移动窗口：若队头下标已超出窗口范围，弹出
- 窗口形成（i >= k-1）后，队头即为当前最大值

时间复杂度: O(n)，每个元素最多入队/出队一次
空间复杂度: O(k)
================================================================================"""

from typing import List
from collections import deque


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    dq = deque()  # 存下标，单调递减
    result = []
    for i, num in enumerate(nums):
        # 弹出过期下标
        while dq and dq[0] <= i - k:
            dq.popleft()
        # 弹出比当前值小的（维持单调递减）
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


if __name__ == "__main__":
    assert max_sliding_window([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
    assert max_sliding_window([1], 1) == [1]
    assert max_sliding_window([1,-1], 1) == [1,-1]
    assert max_sliding_window([1,3,1,2,0,5], 3) == [3,3,2,5]
    assert max_sliding_window([9,8,7,6,5,4,3,2,1], 3) == [9,8,7,6,5,4,3]
    assert max_sliding_window([1,2,3,4,5,6,7,8,9], 3) == [3,4,5,6,7,8,9]
    assert max_sliding_window([4,3,11,2], 4) == [11]  # k==n

    # 与暴力对比
    def brute_force(nums, k):
        return [max(nums[i:i+k]) for i in range(len(nums)-k+1)]

    import random
    nums = [random.randint(-100, 100) for _ in range(200)]
    for k in [1, 3, 10, 50]:
        assert max_sliding_window(nums, k) == brute_force(nums, k), f"k={k}"

    print("所有测试通过!")
    print(f"\n示例结果:")
    print(f"[1,3,-1,-3,5,3,6,7], k=3: {max_sliding_window([1,3,-1,-3,5,3,6,7], 3)}")  # [3,3,5,5,6,7]
