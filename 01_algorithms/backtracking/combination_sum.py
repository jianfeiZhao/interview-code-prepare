"""
题目: 组合总和 I + II
LeetCode: #39 (Medium) + #40 (Medium)
高频公司: 字节跳动、腾讯

========== 题目 I (#39) ==========
给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target，
找出 candidates 中可以使数字和为目标数 target 的所有不同组合，
并以列表形式返回。candidates 中的同一个数字可以无限制重复被选取。

示例: candidates = [2,3,6,7], target = 7 -> [[2,2,3],[7]]

========== 题目 II (#40) ==========
给定一个候选人编号的集合 candidates 和一个目标数 target，
找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的每个数字在每个组合中只能使用 一次，解集不能包含重复的组合。

示例: candidates = [10,1,2,7,6,1,5], target = 8
     -> [[1,1,6],[1,2,5],[1,7],[2,6]]

================================================================================
TL;DR（核心思路）:
- #39（无重复，可重复使用）：下一次从 i 开始（不是 i+1），允许重复选
- #40（有重复，每数只用一次）：排序后跳重复：同层相同元素跳过
  if i > start and candidates[i] == candidates[i-1]: continue
- 剪枝：当前元素 > remaining 时 break（排序保证后续更大）

时间复杂度: O(N^(T/M)) [#39] / O(2^N) [#40]
空间复杂度: O(T/M) [递归深度]
================================================================================"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """#39：可重复选用"""
    result = []
    def backtrack(start, path, remain):
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            backtrack(i, path, remain - candidates[i])  # 可重复，从 i 开始
            path.pop()
    candidates.sort()
    backtrack(0, [], target)
    return result


def combination_sum_ii(candidates: List[int], target: int) -> List[List[int]]:
    """#40：每个元素只能用一次，数组有重复"""
    candidates.sort()
    result = []
    def backtrack(start, path, remain):
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            if i > start and candidates[i] == candidates[i-1]:  # 跳过同层重复
                continue
            path.append(candidates[i])
            backtrack(i + 1, path, remain - candidates[i])
            path.pop()
    backtrack(0, [], target)
    return result


if __name__ == "__main__":
    def sort_result(res):
        return sorted([sorted(r) for r in res])

    # 题目 I
    res = sort_result(combination_sum([2,3,6,7], 7))
    assert res == [[2,2,3],[7]], f"got {res}"

    res = sort_result(combination_sum([2,3,5], 8))
    assert res == [[2,2,2,2],[2,3,3],[3,5]], f"got {res}"

    assert sort_result(combination_sum([2], 1)) == [], "无解"
    assert sort_result(combination_sum([1], 3)) == [[1,1,1]], "单元素重复"

    # 题目 II
    res = sort_result(combination_sum_ii([10,1,2,7,6,1,5], 8))
    assert res == [[1,1,6],[1,2,5],[1,7],[2,6]], f"got {res}"

    res = sort_result(combination_sum_ii([2,5,2,1,2], 5))
    assert res == [[1,2,2],[5]], f"got {res}"

    assert sort_result(combination_sum_ii([1,1,1,1], 2)) == [[1,1]], "去重"

    print("所有测试通过!")
    print(f"\n[2,3,6,7], target=7: {combination_sum([2,3,6,7], 7)}")
    print(f"[10,1,2,7,6,1,5], target=8: {combination_sum_ii([10,1,2,7,6,1,5], 8)}")
