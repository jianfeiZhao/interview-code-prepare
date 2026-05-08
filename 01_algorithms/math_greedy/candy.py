"""
LeetCode #135 - 分发糖果 (Candy)
难度: Hard | 频率: 字节/腾讯

=== 题目描述 ===
n 个孩子站成一排。给你一个整数数组 ratings 表示每个孩子的评分。
你需要按下面的要求，给这些孩子分发糖果:
  - 每个孩子至少分配到 1 块糖果。
  - 相邻两个孩子评分更高的孩子会获得更多的糖果。
请你给每个孩子分发糖果，计算并返回需要准备的最少糖果数目。

示例 1: 输入: ratings = [1,0,2]  输出: 5   (1+1+2 或 2+1+2)
示例 2: 输入: ratings = [1,2,2]  输出: 4   (1+2+1)

=== TL;DR ===
核心思路（两遍贪心）:
  1. 从左到右: 若 ratings[i] > ratings[i-1]，则 candy[i] = candy[i-1] + 1
  2. 从右到左: 若 ratings[i] > ratings[i+1]，则 candy[i] = max(candy[i], candy[i+1] + 1)
  两遍扫描保证每个孩子的左右约束都满足。
  — O(n) 时间，O(n) 空间

时间复杂度: O(n)
空间复杂度: O(n)（O(1) 优化见下方）

=== 详细解析 ===
关键技巧:
1. 初始化所有孩子糖果数为 1（满足最少 1 块的约束）
2. 左扫: 只考虑右比左高的情况
3. 右扫: 只考虑左比右高的情况，用 max 保留已有的较大值
4. 两次扫描互不干扰，最终结果同时满足两个方向的约束
5. O(1) 空间解法（数学）: 统计上升/下降坡段长度，用公式计算
   - 上升坡贡献: 1+2+...+len_up = len_up*(len_up+1)//2
   - 下降坡贡献: 类似，峰值取 max(up, down) 而非重复计数
"""


# ===== 方法1: 两遍贪心（面试推荐）=====
def candy_two_pass(ratings: list) -> int:
    n = len(ratings)
    candies = [1] * n

    # 从左到右: 右边评分更高则糖果 +1
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # 从右到左: 左边评分更高则糖果取 max
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


# ===== 方法2: O(1) 空间（坡度数学法）=====
def candy_math(ratings: list) -> int:
    n = len(ratings)
    if n <= 1:
        return n

    result = 1
    up = 0    # 当前上升坡长度
    down = 0  # 当前下降坡长度
    peak = 0  # 上一个峰值时的上升坡长度

    def triangle(x: int) -> int:
        return x * (x + 1) // 2

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            up += 1
            down = 0
            peak = up
            result += up + 1
        elif ratings[i] == ratings[i - 1]:
            up = down = peak = 0
            result += 1
        else:
            down += 1
            up = 0
            # 若下降坡超过峰值，需要把峰值再加一个（峰值要高于两侧）
            result += down + 1
            if peak >= down:
                result -= 1  # 峰值已经够高，不需要额外加

    return result


# ===== 测试 =====
if __name__ == "__main__":
    cases = [
        ([1, 0, 2], 5),
        ([1, 2, 2], 4),
        ([1], 1),
        ([1, 2], 3),
        ([2, 1], 3),
        ([1, 3, 2, 2, 1], 7),
        ([1, 2, 3, 4, 5], 15),         # 纯上升: 1+2+3+4+5=15
        ([5, 4, 3, 2, 1], 15),         # 纯下降: 5+4+3+2+1=15
        ([1, 3, 4, 5, 2], 11),
        ([1, 2, 3, 1, 0], 11),
    ]
    for func in [candy_two_pass, candy_math]:
        for ratings, expected in cases:
            result = func(list(ratings))
            assert result == expected, \
                f"{func.__name__}({ratings}) = {result}, expected {expected}"

    print("All tests passed!")
