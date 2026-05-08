"""
题目: 在D天内送达包裹的能力（二分答案）
LeetCode: #1011 (Medium)
高频公司: 字节跳动、阿里巴巴

题目描述:
传送带上的包裹必须在 days 天内从一个港口运送到另一个港口。
传送带上的第 i 个包裹的重量为 weights[i]。
每一天，我们都会按给出重量（weights）的顺序往传送带上装载包裹。
我们装载的重量不会超过船的最大运载重量。

返回能在 days 天内将传送带上的所有包裹送达的船的最低运载能力。

示例 1: weights = [1,2,3,4,5,6,7,8,9,10], days = 5 -> 15
示例 2: weights = [3,2,2,4,1,4], days = 3 -> 6
示例 3: weights = [1,2,3,1,1], days = 4 -> 3

================================================================================
TL;DR (核心思路):
  - 二分答案：对"船的容量"做二分搜索
  - 答案范围：[max(weights), sum(weights)]
    * 下界：至少能装最重的一个包裹
    * 上界：一天装完所有包裹
  - 判断函数：贪心模拟，检查容量为 cap 时能否在 days 天内送完
    * 逐个累加，超过 cap 则开新的一天
    * 若天数 <= days，则 cap 可行

时间复杂度: O(n * log(sum(weights)))
空间复杂度: O(1)
================================================================================
"""

from typing import List


def shipWithinDays(weights: List[int], days: int) -> int:
    """
    二分答案：在 [max(weights), sum(weights)] 上二分船的容量。
    """
    left = max(weights)      # 最低容量：能装最重的包裹
    right = sum(weights)     # 最高容量：一天装完所有包裹

    while left < right:
        mid = left + (right - left) // 2

        if can_ship(weights, days, mid):
            # mid 容量可行，尝试更小
            right = mid
        else:
            # mid 容量不够，需要更大
            left = mid + 1

    return left  # left == right，即最小可行容量


def can_ship(weights: List[int], days: int, capacity: int) -> bool:
    """
    贪心判断：容量为 capacity 时，能否在 days 天内送完所有包裹。
    策略：每天尽量多装（贪心），看最少需要多少天。
    """
    days_needed = 1
    current_load = 0

    for w in weights:
        if current_load + w > capacity:
            # 当前船装不下，开启新的一天
            days_needed += 1
            current_load = 0
        current_load += w

    return days_needed <= days


def shipWithinDays_verbose(weights: List[int], days: int) -> int:
    """带详细注释的版本，便于理解二分过程。"""
    # 确定二分范围
    # 下界：单个最重包裹（船必须能装下每个包裹）
    # 上界：所有包裹总重（一天全装完，必然满足任意 days）
    lo, hi = max(weights), sum(weights)

    print(f"二分范围: [{lo}, {hi}]")

    while lo < hi:
        mid = lo + (hi - lo) // 2
        needed_days = 0
        curr = 0
        for w in weights:
            if curr + w > mid:
                needed_days += 1
                curr = 0
            curr += w
        needed_days += 1  # 最后一组也是一天

        print(f"  capacity={mid}, needed_days={needed_days}, days={days}", end="")
        if needed_days <= days:
            print(f" -> 可行，hi={mid}")
            hi = mid
        else:
            print(f" -> 不足，lo={mid+1}")
            lo = mid + 1

    print(f"最小容量: {lo}")
    return lo


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    assert shipWithinDays([1,2,3,4,5,6,7,8,9,10], 5) == 15, "示例1"
    assert shipWithinDays([3,2,2,4,1,4], 3) == 6, "示例2"
    assert shipWithinDays([1,2,3,1,1], 4) == 3, "示例3"
    assert shipWithinDays([1,2,3,4,5,6,7,8,9,10], 1) == 55, "1天，需全部容量"
    assert shipWithinDays([1,2,3,4,5,6,7,8,9,10], 10) == 10, "10天，每天最多一个，最大单重=10"
    assert shipWithinDays([5], 1) == 5, "单个包裹"
    assert shipWithinDays([1, 1, 1, 1], 2) == 2, "均等分"

    # 验证辅助函数
    assert can_ship([1,2,3,4,5,6,7,8,9,10], 5, 15) == True
    assert can_ship([1,2,3,4,5,6,7,8,9,10], 5, 14) == False

    print("所有测试通过!")

    print("\n=== 详细过程（示例1）===")
    shipWithinDays_verbose([1,2,3,4,5,6,7,8,9,10], 5)

    print(f"\n示例结果:")
    print(f"[1..10], days=5: {shipWithinDays([1,2,3,4,5,6,7,8,9,10], 5)}")  # 15
    print(f"[3,2,2,4,1,4], days=3: {shipWithinDays([3,2,2,4,1,4], 3)}")     # 6
    print(f"[1,2,3,1,1], days=4: {shipWithinDays([1,2,3,1,1], 4)}")          # 3
