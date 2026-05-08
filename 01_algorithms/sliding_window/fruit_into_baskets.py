"""
题目: 水果成篮（最多 2 种不同字符的最长子数组）
LeetCode: #904 (Medium)
高频公司: 字节跳动

题目描述:
你正在探访一家农场，农场从左到右种植了一排果树。
这些树用一个整数数组 fruits 表示，其中 fruits[i] 是第 i 棵树上的水果种类。
你想要尽可能多地收集水果。然而，农场的主人设定了一些严格的规矩，你必须按照要求采摘水果：
- 你只有两个篮子，并且每个篮子只能装单一类型的水果（不限数量）。
- 采摘的水果必须是连续的。
- 一旦你达到某棵树，你就必须选择采摘或不采摘该树上的水果。

返回你可以收集的水果的最大数目。

示例 1: fruits = [1,2,1] -> 3   (全部采摘)
示例 2: fruits = [0,1,2,2] -> 3  (采摘 [1,2,2])
示例 3: fruits = [1,2,3,2,2] -> 4 (采摘 [2,3,2,2])

本质: 最多包含 2 种不同元素的最长子数组（滑动窗口经典变体）

================================================================================
TL;DR（核心思路）:
- 滑动窗口 + 哈希表：窗口内水果种类不超过 2
- right 不断扩张，用 Counter 记录窗口内各水果数量
- 当种类 > 2 时，left 右移（同时更新 Counter，种类归 0 时删除键）
- 答案 = max(right - left + 1)

时间复杂度: O(n)
空间复杂度: O(1)（篮子种类最多 2，字典大小恒定）
================================================================================
"""

from typing import List
from collections import defaultdict


def totalFruit(fruits: List[int]) -> int:
    """
    滑动窗口：维护窗口内最多 2 种水果的最长子数组。
    """
    basket = defaultdict(int)  # basket[type] = 窗口内该类水果数量
    left = 0
    max_fruits = 0

    for right in range(len(fruits)):
        basket[fruits[right]] += 1

        # 种类超过 2，收缩左边界
        while len(basket) > 2:
            left_fruit = fruits[left]
            basket[left_fruit] -= 1
            if basket[left_fruit] == 0:
                del basket[left_fruit]
            left += 1

        max_fruits = max(max_fruits, right - left + 1)

    return max_fruits


def totalFruit_k_types(fruits: List[int], k: int = 2) -> int:
    """
    通用版：最多 k 种不同元素的最长子数组（#340 变体）。
    k=2 即为本题，k=1 即只允许一种水果。
    """
    basket = defaultdict(int)
    left = 0
    max_len = 0

    for right in range(len(fruits)):
        basket[fruits[right]] += 1

        while len(basket) > k:
            basket[fruits[left]] -= 1
            if basket[fruits[left]] == 0:
                del basket[fruits[left]]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    assert totalFruit([1, 2, 1]) == 3
    assert totalFruit([0, 1, 2, 2]) == 3
    assert totalFruit([1, 2, 3, 2, 2]) == 4
    assert totalFruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]) == 5  # [1,2,1,1,2]

    # 边界
    assert totalFruit([1]) == 1
    assert totalFruit([1, 1, 1, 1]) == 4  # 全相同
    assert totalFruit([1, 2, 1, 2, 1]) == 5  # 只有2种
    assert totalFruit([1, 2, 3, 1, 2, 3]) == 4  # [3,1,2,3] 或 [1,2,3,1]

    # 通用版 k=2 与专用版结果一致
    test_cases = [
        [1, 2, 1],
        [0, 1, 2, 2],
        [1, 2, 3, 2, 2],
        [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4],
    ]
    for fruits in test_cases:
        assert totalFruit(fruits) == totalFruit_k_types(fruits, k=2), \
            f"两版本不一致: {fruits}"

    # k=1 特殊情况（只允许一种水果）
    assert totalFruit_k_types([1, 2, 1, 1, 2], k=1) == 2  # 最多连续2个相同

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"[1,2,1]:       {totalFruit([1,2,1])}")         # 3
    print(f"[0,1,2,2]:     {totalFruit([0,1,2,2])}")       # 3
    print(f"[1,2,3,2,2]:   {totalFruit([1,2,3,2,2])}")     # 4

    print(f"\n通用版 k 种水果:")
    fruits = [1, 2, 3, 1, 2, 3, 1]
    for k in [1, 2, 3]:
        print(f"  k={k}: {totalFruit_k_types(fruits, k)}")
