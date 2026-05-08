"""
LeetCode #735 - 行星碰撞 (Asteroid Collision)
难度: Medium | 频率: 字节/腾讯

=== 题目描述 ===
给定一个整数数组 asteroids，表示在同一行的行星。
对于数组中的每一个元素，其绝对值表示行星的大小，正负表示行星的移动方向（正 = 向右移动，负 = 向左移动）。
每一颗行星以相同的速度移动。
找出碰撞后剩下的所有行星。碰撞规则：两个行星相互碰撞，较小的行星会爆炸。
如果两颗行星大小相同，则两颗行星都会爆炸。两颗移动方向相同的行星，永远不会发生碰撞。

示例 1: 输入: asteroids = [5,10,-5]    输出: [5,10]（-5 被 10 摧毁）
示例 2: 输入: asteroids = [8,-8]       输出: []（大小相同，同归于尽）
示例 3: 输入: asteroids = [10,2,-5]    输出: [10]（2 被 -5 摧毁，-5 被 10 摧毁）
示例 4: 输入: asteroids = [-2,-1,1,2]  输出: [-2,-1,1,2]（无碰撞）

=== TL;DR ===
核心思路: 用栈模拟碰撞。遇到向左飞的行星（负数）时，与栈中向右飞的行星（正数）发生碰撞。
  碰撞分三种情况：① 右星更大 → 左星消亡；② 左星更大 → 弹出右星继续；③ 同大 → 两者消亡
时间复杂度: O(n)，每颗行星最多入栈出栈各一次
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. 碰撞发生条件: 当前行星向左（负）且 栈顶行星向右（正）
2. 向左飞的负数行星与向右飞正数行星的碰撞处理循环:
   - 若 stack[-1] < abs(asteroid): 右星爆炸，弹出，继续碰撞下一个
   - 若 stack[-1] == abs(asteroid): 两星同归于尽，弹出，当前星也不入栈
   - 若 stack[-1] > abs(asteroid): 左星爆炸，当前星不入栈
3. 两个向左的行星不会相遇（方向相同）；两个向右的行星也不会
4. 负数行星只与紧邻的正数行星碰撞，不会越过负数行星去碰撞更远的正数行星
"""


# ===== 标准栈解法 =====
def asteroid_collision(asteroids: list) -> list:
    stack = []

    for asteroid in asteroids:
        # 判断是否发生碰撞：当前向左（负）且栈顶向右（正）
        alive = True  # 当前行星是否存活
        while alive and asteroid < 0 and stack and stack[-1] > 0:
            if stack[-1] < -asteroid:
                stack.pop()          # 栈顶右星更小，爆炸，继续碰撞
            elif stack[-1] == -asteroid:
                stack.pop()          # 大小相等，同归于尽
                alive = False
            else:
                alive = False        # 当前左星更小，左星爆炸

        if alive:
            stack.append(asteroid)

    return stack


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([5, 10, -5], [5, 10]),
        ([8, -8], []),
        ([10, 2, -5], [10]),
        ([-2, -1, 1, 2], [-2, -1, 1, 2]),
        ([1, -1, 1, -1], []),
        ([-1, -2, 1, 2], [-1, -2, 1, 2]),    # 均向同方向
        ([1, 2, 3, -1, -2, -3], [1, 2]),       # 3 挡住了 -1, -2, -3 接连消灭 2,1
        ([], []),
        ([1], [1]),
        ([-1], [-1]),
        ([-1, 1], [-1, 1]),                    # 反向不碰撞
        ([1, -2, -3], [-2, -3]),               # 1 被 -2 消灭，-3 无碰撞
    ]
    for asteroids, expected in cases:
        result = asteroid_collision(list(asteroids))
        assert result == expected, \
            f"asteroid_collision({asteroids}) = {result}, expected {expected}"

    print("All tests passed!")
