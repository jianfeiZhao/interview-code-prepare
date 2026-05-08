"""
题目：旋转数组
难度：Medium | 高频出现：字节/阿里/腾讯/美团/百度（全系）
标签：数组、双指针、原地算法
LeetCode：#189


题目描述
---------
给定一个整数数组 nums，将数组中的元素向右轮转 k 个位置，其中 k 是非负数。
要求原地修改数组，只允许使用 O(1) 额外空间。

示例
------
输入: nums = [1,2,3,4,5,6,7], k = 3
输出: [5,6,7,1,2,3,4]

输入: nums = [-1,-100,3,99], k = 2
输出: [3,99,-1,-100]

约束
------
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= k <= 10^5

TL;DR（30秒速览）
- 思路：三次翻转法——翻转全部 → 翻转前k个 → 翻转后n-k个
- 时间：O(n)  空间：O(1)
- 陷阱：k 可能大于 n，需取 k %= n；k=0 时无需操作

详细解析
---------
方法1：额外数组 O(n) 空间
  新数组 new[i] = nums[(i - k) % n]，简单直接但用了额外空间。

方法2：环状替换 O(n) 时间 O(1) 空间
  从位置 0 出发，把 nums[i] 移到 nums[(i+k)%n]，沿环走一圈。
  当 gcd(n,k)>1 时需要从多个起点出发，实现较繁琐。

方法3：三次翻转（最优，推荐）：
  右移 k 步等价于：
    [1,2,3,4,5,6,7] k=3
  → 翻转全部：[7,6,5,4,3,2,1]
  → 翻转前k=3：[5,6,7,4,3,2,1]
  → 翻转后n-k=4：[5,6,7,1,2,3,4]  ✓

  每次翻转 O(n)，共 O(n)，原地 O(1)。
"""

from typing import List


def rotate(nums: List[int], k: int) -> None:
    """原地旋转，不返回值。"""
    n = len(nums)
    k %= n
    if k == 0:
        return

    def reverse(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse(0, n - 1)       # 翻转全部
    reverse(0, k - 1)       # 翻转前 k 个
    reverse(k, n - 1)       # 翻转后 n-k 个


# 纯函数版，方便测试
def rotate_pure(nums: List[int], k: int) -> List[int]:
    nums = nums[:]
    rotate(nums, k)
    return nums


if __name__ == "__main__":
    assert rotate_pure([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
    assert rotate_pure([-1, -100, 3, 99], 2) == [3, 99, -1, -100]
    assert rotate_pure([1, 2], 3) == [2, 1]       # k > n
    assert rotate_pure([1], 0) == [1]              # k = 0
    assert rotate_pure([1, 2, 3], 6) == [1, 2, 3]  # k = n
    print("All tests passed.")
