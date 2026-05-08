"""
题目：组合总和III
难度：Medium | 高频出现：字节/阿里
标签：回溯
LeetCode：#216

题目描述
---------
找出所有相加之和为 n 的 k 个数的组合，其中每个数字只能使用 1~9 且不重复。
所有可能的有效组合以列表形式返回，答案不含重复的组合，组合中的数字按升序排列。

示例
------
输入: k = 3, n = 7
输出: [[1,2,4]]

输入: k = 3, n = 9
输出: [[1,2,6],[1,3,5],[2,3,4]]

约束
------
- 2 <= k <= 9
- 1 <= n <= 60

TL;DR（30秒速览）
- 回溯：从1~9中选k个不重复数字，和为n
- 每次从start开始选，避免重复
- 时间 O(C(9,k))，空间 O(k)

详细解析
---------
与 #39 组合总和类似，但：
  - 数字来自 1~9，每个只能用一次
  - 组合中恰好有 k 个数
"""

from typing import List


def combination_sum3(k: int, n: int) -> List[List[int]]:
    result = []

    def backtrack(start, remaining, path):
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return
        if len(path) == k or remaining <= 0:
            return
        for num in range(start, 10):
            if num > remaining:  # 剪枝
                break
            path.append(num)
            backtrack(num + 1, remaining - num, path)
            path.pop()

    backtrack(1, n, [])
    return result


if __name__ == "__main__":
    assert sorted(combination_sum3(3, 7)) == sorted([[1,2,4]])
    assert sorted(combination_sum3(3, 9)) == sorted([[1,2,6],[1,3,5],[2,3,4]])
    assert combination_sum3(4, 1) == []
    assert sorted(combination_sum3(2, 18)) == sorted([[9, 9]]) or combination_sum3(2, 18) == []  # 9+9=18但不重复
    # 实际上1-9不重复，9+9不合法
    assert combination_sum3(2, 18) == []
    print("All tests passed.")
