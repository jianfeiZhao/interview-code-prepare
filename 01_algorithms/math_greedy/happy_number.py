"""
LeetCode #202 - 快乐数 (Happy Number)
难度: Easy | 频率: 字节/阿里

=== 题目描述 ===
编写一个算法来判断一个数 n 是不是快乐数。
「快乐数」定义为: 对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，
然后重复这个过程直到这个数变为 1，也可能是无限循环但始终变不到 1。
如果可以变为 1，那么这个数就是快乐数。

示例 1: 输入: n = 19  输出: true
  19 -> 1^2 + 9^2 = 82 -> 64 -> 52 -> 29 -> 85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89 (循环)
  不对，19是快乐数: 19->82->68->100->1

示例 2: 输入: n = 2   输出: false

=== TL;DR ===
核心思路:
  方法1（哈希集合）: 将每次计算结果存入集合，若重复出现则必然循环，不是快乐数 — O(log n) 时间
  方法2（Floyd 判圈，快慢指针）: 快指针每次走两步，慢指针走一步，若有环则相遇
    — O(log n) 时间，O(1) 空间

时间复杂度: O(log n)（每次运算结果快速收敛到个位数）
空间复杂度: O(1)（Floyd）/ O(log n)（哈希）

=== 详细解析 ===
关键技巧:
1. 核心辅助函数: 计算各位数字的平方和
2. 不快乐数必然进入含 4 的循环: 4->16->37->58->89->145->42->20->4
   所以可以特判: 若出现 4 或 89 则返回 False
3. Floyd 判圈（龟兔赛跑）: slow = get_next(n)，fast = get_next(get_next(n))
   循环直到 slow == fast（相遇）或 fast == 1
4. 此算法与链表判环完全一致，是同一思路的不同应用
"""


def get_next(n: int) -> int:
    """计算各位数字的平方和"""
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total


# ===== 方法1: 哈希集合 =====
def is_happy_hash(n: int) -> bool:
    seen = set()
    while n != 1:
        if n in seen:
            return False
        seen.add(n)
        n = get_next(n)
    return True


# ===== 方法2: Floyd 判圈（O(1) 空间）=====
def is_happy_floyd(n: int) -> bool:
    slow = n
    fast = get_next(n)
    while fast != 1 and slow != fast:
        slow = get_next(slow)           # 走1步
        fast = get_next(get_next(fast)) # 走2步
    return fast == 1


# ===== 方法3: 特判已知循环（最快）=====
def is_happy_shortcut(n: int) -> bool:
    # 不是快乐数时必然经过 4
    while n != 1 and n != 4:
        n = get_next(n)
    return n == 1


# ===== 测试 =====
if __name__ == "__main__":
    # 验证 get_next
    assert get_next(19) == 82   # 1^2 + 9^2 = 1 + 81 = 82
    assert get_next(1) == 1
    assert get_next(100) == 1

    # 快乐数
    happy_numbers = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 91, 94, 97, 100]
    # 非快乐数
    unhappy_numbers = [2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15, 16, 17, 18, 20, 21, 22]

    for func in [is_happy_hash, is_happy_floyd, is_happy_shortcut]:
        for n in happy_numbers:
            assert func(n) == True, f"{func.__name__}({n}) should be True"
        for n in unhappy_numbers:
            assert func(n) == False, f"{func.__name__}({n}) should be False"

    print("All tests passed!")
