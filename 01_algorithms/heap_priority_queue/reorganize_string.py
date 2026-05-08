"""
题目: 重构字符串（最大堆）
LeetCode: #767 (Medium)
高频公司: 字节跳动

题目描述:
给定一个字符串 s，检验是否能重新排布其中的字母，使得两相邻的字符不同。
返回满足条件的任意可能的结果字符串。若不可能，则返回空字符串 ""。

示例 1: s = "aab" -> "aba"
示例 2: s = "aaab" -> ""   (a 太多，无法避免相邻)

================================================================================
TL;DR (核心思路):

方法1 - 大顶堆（贪心）:
  - 每次从堆中取频率最高的字符放入结果
  - 若与上一个字符相同，则取第二高频字符，将最高频暂存后再放回
  - 不可能时：最高频字符出现次数 > (len(s) + 1) // 2

方法2 - 间隔填充（更优雅）:
  - 按频率排序，先填偶数位 0,2,4,...，再填奇数位 1,3,5,...
  - 频率最高的字符先填，天然保证相邻不同

不可能条件: max_freq > (n + 1) // 2（鸽巢原理）

时间复杂度: O(n log k)，k 为字符种类数（最多 26）
空间复杂度: O(k)
================================================================================
"""

import heapq
from collections import Counter


def reorganizeString_heap(s: str) -> str:
    """
    大顶堆贪心：每次优先放频率最高的字符，若与前一个相同则放第二高频的。
    """
    count = Counter(s)
    n = len(s)

    # 不可能的情况：最高频字符超过一半（向上取整）
    if max(count.values()) > (n + 1) // 2:
        return ""

    # 大顶堆（用负值模拟）
    max_heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(max_heap)

    result = []
    prev_freq, prev_char = 0, ""  # 上一个放入的字符（及其剩余频率）

    while max_heap:
        freq, char = heapq.heappop(max_heap)

        result.append(char)

        # 将上一个暂存的字符放回堆（冷却结束）
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))

        # 更新 prev：当前字符下次不能立刻使用
        prev_freq, prev_char = freq + 1, char  # freq 是负值，+1 表示用了一次

    return "".join(result)


def reorganizeString_interleave(s: str) -> str:
    """
    间隔填充法：
    将字符按频率降序排列，依次填入偶数位 (0,2,4,...) 再填奇数位 (1,3,5,...)。
    频率最高的字符先填偶数位，自然不会相邻。
    """
    count = Counter(s)
    n = len(s)

    # 不可能的情况
    if max(count.values()) > (n + 1) // 2:
        return ""

    # 按频率降序排列字符
    sorted_chars = sorted(count.keys(), key=lambda c: -count[c])

    result = [""] * n
    idx = 0  # 当前填写位置

    for char in sorted_chars:
        for _ in range(count[char]):
            # 先填偶数位，填满后填奇数位
            if idx >= n:
                idx = 1  # 切换到奇数位
            result[idx] = char
            idx += 2

    return "".join(result)


def reorganizeString_check(s: str) -> bool:
    """验证重构结果是否合法（相邻字符不同）。"""
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            return False
    return True


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 可能的情况：验证结果合法性（答案不唯一，只验证合法性）
    possible_cases = ["aab", "abc", "aabc", "aabb", "a", "ab", "vvvlo"]
    for s in possible_cases:
        r1 = reorganizeString_heap(s)
        r2 = reorganizeString_interleave(s)

        # 结果不空
        assert r1 != "", f"heap: 不应返回空: {s}"
        assert r2 != "", f"interleave: 不应返回空: {s}"

        # 包含相同字符集
        assert Counter(r1) == Counter(s), f"heap: 字符集不匹配: {s} -> {r1}"
        assert Counter(r2) == Counter(s), f"interleave: 字符集不匹配: {s} -> {r2}"

        # 相邻字符不同
        assert reorganizeString_check(r1), f"heap: 相邻字符重复: {r1}"
        assert reorganizeString_check(r2), f"interleave: 相邻字符重复: {r2}"

    # 不可能的情况
    impossible_cases = ["aaab", "aaa", "aaaa", "aaabc"]
    for s in impossible_cases:
        assert reorganizeString_heap(s) == "", f"heap: 应返回空: {s}"
        assert reorganizeString_interleave(s) == "", f"interleave: 应返回空: {s}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"'aab' -> '{reorganizeString_heap('aab')}'")     # 'aba' 或其他合法答案
    print(f"'aaab' -> '{reorganizeString_heap('aaab')}'")   # ''
    print(f"'vvvlo' -> '{reorganizeString_heap('vvvlo')}'") # 合法的如 'vlvov'

    print(f"\n两种方法对比（'aabbc'）:")
    print(f"  堆方法:     '{reorganizeString_heap('aabbc')}'")
    print(f"  间隔填充:   '{reorganizeString_interleave('aabbc')}'")
