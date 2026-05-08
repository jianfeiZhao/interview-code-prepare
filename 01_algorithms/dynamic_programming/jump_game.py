"""
题目：跳跃游戏 I & II
难度：Medium | 高频出现：字节/阿里/腾讯
标签：贪心、动态规划、数组
LeetCode：#55 跳跃游戏 / #45 跳跃游戏 II


题目描述
---------
给定一个非负整数数组 nums（与 array_string/jump_game.py 同题，DP 视角实现）。
#55：初始位于第一个下标，数组每个元素代表该位置最大跳跃长度，判断能否到达最后位置。
#45：返回到达最后位置所需的最少跳跃次数，保证可以到达。

示例
------
#55 输入: nums = [2,3,1,1,4]  输出: True
#45 输入: nums = [2,3,1,1,4]  输出: 2  （0→1→4）

约束
------
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

TL;DR（30秒速览）
- #55：维护当前能到达的最远下标 max_reach；若当前位置超出则不可达
- #45：贪心 BFS 分层，每层内取能到达的最远点，层数即跳数
- 时间 O(n)，空间 O(1)
- 关键陷阱：#45 注意最后一步可能恰好落在终点，避免多计一跳

详细解析
---------
#55 可达性判断：
  遍历数组，维护 max_reach = max(max_reach, i + nums[i])。
  若 i > max_reach 说明位置 i 无法到达，返回 False。
  遍历完成返回 True。

#45 最少跳数（贪心分层）：
  把问题看作 BFS 按层扩展：当前层范围 [cur_start, cur_end]，
  遍历这一层中所有格子，记录下一层能到达的最远下标 next_end。
  当 cur_end 到达终点时停止，跳数 +1 的时机是"进入新层"。
  循环内一旦 next_end >= n-1 即可提前终止。
"""

from typing import List


# ─────────────────────────────────────────
# #55  跳跃游戏 I —— 能否到达终点
# ─────────────────────────────────────────
def can_jump(nums: List[int]) -> bool:
    max_reach = 0
    for i, v in enumerate(nums):
        if i > max_reach:       # 当前位置已无法到达
            return False
        max_reach = max(max_reach, i + v)
    return True


# ─────────────────────────────────────────
# #45  跳跃游戏 II —— 到达终点的最少跳数
# ─────────────────────────────────────────
def jump(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    cur_end = 0     # 当前层（跳数 = jumps）能到达的最远下标
    next_end = 0    # 下一层能到达的最远下标

    for i in range(n - 1):      # 最后一格不需要再跳
        next_end = max(next_end, i + nums[i])
        if i == cur_end:        # 遍历完当前层，必须起跳
            jumps += 1
            cur_end = next_end
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
    assert jump([0]) == 0
    assert jump([1, 2, 3]) == 2

    print("All tests passed.")
