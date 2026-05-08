"""
题目：前 K 个高频元素
难度：Medium | 高频出现：字节/美团
标签：堆、哈希表、排序
LeetCode：#347

题目描述
---------
给定整数数组 nums 和整数 k，返回出现频率前 k 高的元素。
返回结果的顺序不限，题目保证答案唯一。

示例
------
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1, 2]  # 1 出现3次，2 出现2次

输入: nums = [1], k = 1
输出: [1]

约束
------
- 1 <= len(nums) <= 10^5
- k 满足 1 <= k <= 数组中不同元素的个数
- 答案保证唯一

TL;DR（30秒速览）
- 思路：Counter 统计频率，用大小为 k 的最小堆维护 top-k
- 时间：O(n log k)  空间：O(n)
- 陷阱：用最小堆（heapq）而非最大堆，堆顶是最小频率，超出 k 则弹出

详细解析
---------
方法1 - 最小堆（推荐，O(n log k)）：
  Counter 统计频率，遍历频率字典，维护一个大小为 k 的最小堆
  若堆满且当前频率 > 堆顶 → 替换

方法2 - 桶排序（O(n) 最优）：
  频率最大为 n，建 n+1 个桶，freq[i] 存频率为 i 的元素
  从右往左遍历桶，收集 k 个元素
"""

from typing import List
import heapq
from collections import Counter


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)


def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]
    return result


if __name__ == "__main__":
    assert sorted(top_k_frequent_heap([1,1,1,2,2,3], 2)) == [1, 2]
    assert top_k_frequent_heap([1], 1) == [1]
    assert sorted(top_k_frequent_bucket([1,1,1,2,2,3], 2)) == [1, 2]
    print("All tests passed.")
