"""
题目：最小栈
难度：Easy | 高频出现：全系大厂
标签：栈、设计题
LeetCode：#155


题目描述
---------
设计一个支持 push、pop、top 操作，并能在常数时间内检索到最小元素的栈。
实现 MinStack 类：
  - push(val)：将元素 val 推入栈中
  - pop()：删除栈顶的元素
  - top()：获取栈顶元素
  - getMin()：检索栈中的最小元素

示例
------
输入: ["MinStack","push","push","push","getMin","pop","top","getMin"]
      [[],[-2],[0],[-3],[],[],[],[]]
输出: [null,null,null,null,-3,null,0,-2]

约束
------
- pop、top 和 getMin 操作总是在非空栈上调用
- 所有操作的时间复杂度为 O(1)

TL;DR（30秒速览）
- 思路：辅助栈同步维护当前最小值，push 时同时更新辅助栈
- 时间：O(1) 所有操作  空间：O(n)
- 陷阱：辅助栈每次 push 都要 push（哪怕比当前最小值大），与主栈对齐

详细解析
---------
辅助栈 min_stack：
  push(val)：min_stack push min(val, min_stack[-1])
  pop()：主栈 pop，min_stack 也 pop
  getMin()：返回 min_stack[-1]

这样 min_stack[i] 始终是主栈前 i 个元素中的最小值。
"""


class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # 辅助栈，存当前最小值

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(min_val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


if __name__ == "__main__":
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2
    print("All tests passed.")
