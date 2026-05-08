"""
LeetCode #225 - 用队列实现栈 (Implement Stack using Queues)
难度: Easy | 频率: 全系

=== 题目描述 ===
请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（push、top、pop 和 empty）。
  - void push(int x)    将元素 x 压入栈顶
  - int pop()           移除并返回栈顶元素
  - int top()           返回栈顶元素
  - boolean empty()     如果栈是空的，返回 true；否则，返回 false

注意：只能使用队列的标准操作（push to back, peek/pop from front, size, is empty）。
进阶：能否实现仅使用一个队列？

=== TL;DR ===
核心思路:
  方法1（两个队列，push O(n)）: push 时先将新元素加入 q2，再将 q1 所有元素转入 q2，最后交换 q1/q2
    — push O(n)，pop/top O(1)
  方法2（一个队列，push O(n)）: push 后将队列中新元素前面的所有元素重新入队（旋转）
    — push O(n)，pop/top O(1)

时间复杂度: push O(n)，pop/top O(1)
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. 方法1: 每次 push 都重建队列，确保最新元素在队首
   步骤: ① 新元素入 q2 ② q1 所有元素依次出队进 q2 ③ 交换 q1 和 q2
2. 方法2（单队列旋转）: push 后将前 n-1 个元素（旧元素）重新加到队尾
   这样新元素永远在队首（即栈顶）
3. 实际中通常选择让 pop 来做 O(n) 的搬运，push 保持 O(1)（取决于应用场景）
"""

from collections import deque


# ===== 方法1: 两个队列（push 保持栈顶在队首）=====
class MyStack_TwoQueues:
    def __init__(self):
        self.q1 = deque()  # 主队列（队首 = 栈顶）
        self.q2 = deque()  # 辅助队列

    def push(self, x: int) -> None:
        self.q2.append(x)          # 新元素先入 q2
        while self.q1:
            self.q2.append(self.q1.popleft())  # q1 全部转入 q2
        self.q1, self.q2 = self.q2, self.q1   # 交换

    def pop(self) -> int:
        return self.q1.popleft()

    def top(self) -> int:
        return self.q1[0]

    def empty(self) -> bool:
        return not self.q1


# ===== 方法2: 单队列旋转（更简洁）=====
class MyStack_OneQueue:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        # 将新元素前面的所有旧元素重新排到新元素后面
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q


# ===== 测试 =====
def run_tests(StackClass):
    name = StackClass.__name__

    s = StackClass()
    assert s.empty() == True

    s.push(1)
    s.push(2)
    s.push(3)

    assert s.top() == 3,      f"{name}: top should be 3"
    assert s.pop() == 3,      f"{name}: pop should return 3"
    assert s.top() == 2,      f"{name}: top should be 2"
    assert s.empty() == False, f"{name}: should not be empty"
    assert s.pop() == 2,      f"{name}: pop should return 2"
    assert s.pop() == 1,      f"{name}: pop should return 1"
    assert s.empty() == True,  f"{name}: should be empty"

    # LIFO 顺序验证
    s2 = StackClass()
    for i in range(5):
        s2.push(i)
    for i in range(4, -1, -1):
        assert s2.pop() == i, f"{name}: LIFO order failed"


if __name__ == "__main__":
    run_tests(MyStack_TwoQueues)
    run_tests(MyStack_OneQueue)
    print("All tests passed!")
