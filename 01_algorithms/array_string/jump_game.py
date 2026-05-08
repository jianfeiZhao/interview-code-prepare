"""
题目：跳跃游戏 I & II
难度：Medium | 高频出现：字节/阿里/腾讯
标签：数组、贪心、动态规划
LeetCode：#55（能否到达）、#45（最少跳跃次数）


题目描述
---------
给你一个非负整数数组 nums，你最初位于数组的第一个下标。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
判断你是否能够到达最后一个下标（#55），或返回到达最后一个下标所需的最小跳跃次数（#45）。

示例
------
#55 输入: nums = [2,3,1,1,4]  输出: True（0→1→4）
#55 输入: nums = [3,2,1,0,4]  输出: False
#45 输入: nums = [2,3,1,1,4]  输出: 2
#45 输入: nums = [2,3,0,1,4]  输出: 2

约束
------
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

TL;DR（30秒速览）
- #55 思路：维护「能到达的最远位置」max_reach，若当前下标超出则 False
- #45 思路：贪心 BFS 分层——每一跳尽量跳最远，记录「当前跳能到的边界」
- 时间：O(n)  空间：O(1)

详细解析
---------
=== #55 跳跃游戏 ===
DP 解：dp[i] = 能否到达 i，dp[i] = any(dp[j] and j+nums[j]>=i for j<i)，O(n²)。

贪心（最优）：
  维护 max_reach = 当前能到达的最远下标。
  遍历每个下标 i：
    - 若 i > max_reach，说明 i 不可达，返回 False。
    - 否则更新 max_reach = max(max_reach, i + nums[i])。
  遍历结束返回 True。

=== #45 跳跃游戏 II ===
贪心 BFS 分层（最优 O(n) O(1)）：
  把每次跳跃看作 BFS 的一层：
    cur_end   = 当前跳的边界（这一跳内最远能到哪）
    farthest  = 遍历当前层时能到达的最远位置
    jumps     = 跳跃次数
  遍历 i（不含最后一个元素）：
    - 更新 farthest = max(farthest, i + nums[i])
    - 当 i == cur_end 时，说明当前层走完，必须跳一次，
      jumps += 1，cur_end = farthest。
    - 若 cur_end >= n-1 可提前 break。
"""

from typing import List


# ---- #55 跳跃游戏：能否到达终点 ----
def can_jump(nums: List[int]) -> bool:
    max_reach = 0
    for i, v in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + v)
    return True


# ---- #45 跳跃游戏 II：最少跳跃次数 ----
def jump(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    cur_end = 0    # 当前跳的最远边界
    farthest = 0   # 遍历中能到达的最远位置

    for i in range(n - 1):  # 最后一个位置不需要从这里出发
        farthest = max(farthest, i + nums[i])
        if i == cur_end:   # 当前跳走完，必须发起下一跳
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break

    return jumps


if __name__ == "__main__":
    # #55 测试
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    assert can_jump([0]) is True
    assert can_jump([1, 0]) is True

    # #45 测试
    assert jump([2, 3, 1, 1, 4]) == 2
    assert jump([2, 3, 0, 1, 4]) == 2
    assert jump([1]) == 0
    assert jump([1, 2, 3]) == 2
    assert jump([0]) == 0

    print("All tests passed.")
