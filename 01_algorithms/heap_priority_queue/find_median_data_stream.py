"""
题目: 数据流的中位数（双堆）
LeetCode: #295 (Hard)
高频公司: 字节跳动、腾讯、阿里巴巴（必考）

题目描述:
中位数是有序整数列表中间的数字。如果列表的大小是偶数，则没有中间值，
中位数是两个中间值的平均值。

实现 MedianFinder 类:
- MedianFinder()：初始化 MedianFinder 对象
- void addNum(int num)：从数据流中添加一个整数到数据结构中
- double findMedian()：返回目前数据流的中位数（精确值）

示例:
MedianFinder mf; mf.addNum(1); mf.addNum(2); mf.findMedian() -> 1.5
mf.addNum(3); mf.findMedian() -> 2.0

================================================================================
TL;DR (核心思路):

双堆维护中位数：
  - max_heap（大顶堆）：存较小的一半，堆顶是较小半部分的最大值
  - min_heap（小顶堆）：存较大的一半，堆顶是较大半部分的最小值
  - 维护不变量：max_heap（左半）<= min_heap（右半）
  - 维护大小：len(max_heap) == len(min_heap) 或 len(max_heap) == len(min_heap) + 1
  - 中位数 = 奇数时 max_heap 堆顶，偶数时 (max_heap顶 + min_heap顶) / 2

addNum 步骤（3步法）：
  1. 先入 max_heap
  2. 平衡大小关系：若 max_heap 顶 > min_heap 顶，则移到 min_heap
  3. 平衡数量：保证 max_heap 不超过 min_heap 超过1个；min_heap 不超过 max_heap

Python 只有最小堆：最大堆存负数模拟

时间复杂度: addNum O(log n)，findMedian O(1)
空间复杂度: O(n)
================================================================================
"""

import heapq
import random


class MedianFinder:
    """
    双堆数据结构，动态维护数据流中位数。

    不变量：
    - max_heap（大顶堆，存负值）：较小的一半
    - min_heap（小顶堆）：较大的一半
    - max_heap 中所有元素 <= min_heap 中所有元素
    - len(max_heap) >= len(min_heap)，差值最多为 1
    """

    def __init__(self):
        self.max_heap = []  # 左半（存负数模拟最大堆）
        self.min_heap = []  # 右半（最小堆）

    def add_num(self, num: int) -> None:
        # 先推入最大堆
        heapq.heappush(self.max_heap, -num)
        # 平衡：最大堆顶不能大于最小堆顶
        if self.min_heap and -self.max_heap[0] > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        # 维持大小：max_heap 多 0 或 1 个
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    # 兼容 LeetCode 接口命名
    def addNum(self, num: int) -> None:
        self.add_num(num)

    def find_median(self) -> float:
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2
        return float(-self.max_heap[0])

    def findMedian(self) -> float:
        return self.find_median()


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 测试用例1：题目示例
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5, f"expected 1.5, got {mf.find_median()}"
    mf.add_num(3)
    assert mf.find_median() == 2.0, f"expected 2.0, got {mf.find_median()}"

    # 测试用例2：较多数据
    mf2 = MedianFinder()
    for n in [6, 10, 2, 6, 5, 0, 6, 3, 1, 0, 0]:
        mf2.add_num(n)
    assert mf2.find_median() == 3.0

    # 测试用例3：单元素
    mf3 = MedianFinder()
    mf3.add_num(5)
    assert mf3.find_median() == 5.0

    # 测试用例4：逆序插入
    mf4 = MedianFinder()
    for num in [5, 4, 3, 2, 1]:
        mf4.add_num(num)
    assert mf4.find_median() == 3.0

    # 测试用例5：包含负数
    mf5 = MedianFinder()
    for num in [-1, -2, -3]:
        mf5.add_num(num)
    assert mf5.find_median() == -2.0

    # 测试用例6：随机大量数据，与排序结果比较
    nums = [random.randint(-100, 100) for _ in range(200)]
    mf6 = MedianFinder()
    for i, num in enumerate(nums):
        mf6.add_num(num)
        sorted_so_far = sorted(nums[:i+1])
        n = len(sorted_so_far)
        if n % 2 == 1:
            expected = float(sorted_so_far[n // 2])
        else:
            expected = (sorted_so_far[n // 2 - 1] + sorted_so_far[n // 2]) / 2.0
        assert abs(mf6.find_median() - expected) < 1e-9, \
            f"i={i}, num={num}, got={mf6.find_median()}, expected={expected}"

    print("所有测试通过!")

    # 演示过程
    print("\n=== 详细演示 ===")
    mfd = MedianFinder()
    for num in [1, 2, 3, 4, 5]:
        mfd.add_num(num)
        lo_vals = sorted([-x for x in mfd.max_heap], reverse=True)
        hi_vals = sorted(mfd.min_heap)
        print(f"  addNum({num}): max_heap={lo_vals}, min_heap={hi_vals} -> median={mfd.find_median()}")
