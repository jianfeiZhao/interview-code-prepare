"""
LeetCode #232 - 用栈实现队列 (Implement Queue using Stacks)
难度: Easy | 频率: 全系

=== 题目描述 ===
请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（push、pop、peek、empty）。
实现 MyQueue 类：
  - void push(int x)    将元素 x 推到队列的末尾
  - int pop()           从队列的开头移除并返回元素
  - int peek()          返回队列开头的元素
  - boolean empty()     如果队列为空，返回 true；否则，返回 false

说明：只能使用标准的栈操作，即只有 push to top, peek/pop from top, size 和 is empty 操作。

进阶：能否实现每个操作均摊 O(1) 的时间复杂度？

=== TL;DR ===
核心思路: 用两个栈（in_stack 和 out_stack）模拟队列的先进先出。
  - push: 始终压入 in_stack
  - pop/peek: 若 out_stack 为空，将 in_stack 所有元素倒入 out_stack，再操作 out_stack
  - 倒转操作使先进的元素变成 out_stack 的栈顶

时间复杂度: 均摊 O(1)（每个元素最多入栈出栈各两次）
空间复杂度: O(n)

=== 详细解析 ===
关键技巧:
1. "懒惰转移": 只有当 out_stack 为空时才将 in_stack 全部倒入，而不是每次 pop 都倒
2. 这样每个元素只会被倒转一次，均摊时间 O(1)
3. 对比 #225（用队列实现栈）: 该题反过来，每次 push 时通过旋转队列保持新元素在队首
"""


class MyQueue:
    def __init__(self):
        self.in_stack = []   # 入队栈（新元素压入这里）
        self.out_stack = []  # 出队栈（pop/peek 从这里取）

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _transfer(self) -> None:
        """当 out_stack 为空时，将 in_stack 全部倒入 out_stack"""
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack


# ===== 测试 =====
if __name__ == "__main__":
    q = MyQueue()
    assert q.empty() == True

    q.push(1)
    q.push(2)
    q.push(3)

    assert q.peek() == 1   # 队首是1
    assert q.pop() == 1
    assert q.peek() == 2
    assert q.empty() == False
    assert q.pop() == 2
    assert q.pop() == 3
    assert q.empty() == True

    # 交替 push 和 pop 测试（验证均摊 O(1)）
    q2 = MyQueue()
    for i in range(5):
        q2.push(i)
    for i in range(5):
        assert q2.pop() == i  # 保证 FIFO

    # push 和 pop 交替
    q3 = MyQueue()
    q3.push(1)
    assert q3.pop() == 1
    q3.push(2)
    q3.push(3)
    assert q3.pop() == 2
    q3.push(4)
    assert q3.pop() == 3
    assert q3.pop() == 4

    print("All tests passed!")
