"""
题目：最长湍流子数组
难度：Medium | 高频出现：字节/阿里
标签：动态规划、滑动窗口、数组
LeetCode：#978

题目描述
---------
给定整数数组 arr，如果一个子数组是湍流子数组，则相邻元素的比较符号严格交替（大于和小于交替出现）。
返回 arr 中最大的湍流子数组的长度。
单个元素的子数组视为长度为 1 的湍流子数组。

示例
------
输入: arr = [9, 4, 2, 10, 7, 8, 8, 1, 9]
输出: 5  # 子数组 [4, 2, 10, 7, 8]（4>2<10>7<8，符号严格交替）

输入: arr = [4, 8, 12, 16]
输出: 2  # 全部单调递增，相邻任意两个元素构成长度2的湍流子数组

约束
------
- 1 <= len(arr) <= 4 * 10^4
- 0 <= arr[i] <= 10^9

TL;DR（30秒速览）
- DP 双状态：inc[i] 以 i 结尾且最后一步上升，dec[i] 以 i 结尾且最后一步下降
- 时间 O(n)，空间 O(1)（滚动变量）
- 关键陷阱：相邻元素相等时两个状态都重置为 1

详细解析
---------
湍流子数组：相邻元素的比较符号严格交替（> < > < 或 < > < >）。

DP 定义：
  inc = 以当前位置结尾、且最后一步是"上升"（arr[i] > arr[i-1]）的最长湍流子数组长度
  dec = 以当前位置结尾、且最后一步是"下降"（arr[i] < arr[i-1]）的最长湍流子数组长度

转移：
  若 arr[i] > arr[i-1]：inc = dec + 1，dec = 1（上升不能跟上升）
  若 arr[i] < arr[i-1]：dec = inc + 1，inc = 1
  若 arr[i] == arr[i-1]：inc = dec = 1（中断）

答案 = 遍历过程中 max(inc, dec) 的最大值。
"""

from typing import List


def max_turbulence_size(arr: List[int]) -> int:
    n = len(arr)
    if n < 2:
        return n

    inc = 1   # 以当前位置结尾、最后一步上升的最长长度
    dec = 1   # 以当前位置结尾、最后一步下降的最长长度
    ans = 1

    for i in range(1, n):
        if arr[i] > arr[i - 1]:
            inc = dec + 1
            dec = 1
        elif arr[i] < arr[i - 1]:
            dec = inc + 1
            inc = 1
        else:
            inc = 1
            dec = 1
        ans = max(ans, inc, dec)

    return ans


# 方法二：滑动窗口（双指针，更直观）
def max_turbulence_size_sliding(arr: List[int]) -> int:
    n = len(arr)
    ans = 1
    left = 0

    for right in range(1, n):
        if right >= 2:
            cmp_prev = (arr[right - 1] > arr[right - 2]) - (arr[right - 1] < arr[right - 2])
            cmp_curr = (arr[right] > arr[right - 1]) - (arr[right] < arr[right - 1])
            # 湍流被破坏：相同方向或相等
            if cmp_prev * cmp_curr >= 0:
                left = right - 1 if arr[right] != arr[right - 1] else right
        ans = max(ans, right - left + 1)

    return ans


if __name__ == "__main__":
    assert max_turbulence_size([9, 4, 2, 10, 7, 8, 8, 1, 9]) == 5   # [4,2,10,7,8]
    assert max_turbulence_size([4, 8, 12, 16]) == 2
    assert max_turbulence_size([100]) == 1
    assert max_turbulence_size([0, 1, 1]) == 2

    assert max_turbulence_size_sliding([9, 4, 2, 10, 7, 8, 8, 1, 9]) == 5
    assert max_turbulence_size_sliding([4, 8, 12, 16]) == 2

    print("All tests passed.")
