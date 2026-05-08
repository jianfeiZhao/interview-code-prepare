"""
题目：最小栈
难度：Medium | 高频出现：字节/阿里/腾讯/微软
标签：栈、设计
LeetCode：#155 Min Stack


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
- 每次操作时间复杂度为 O(1)

TL;DR（30秒速览）
- 核心思路：辅助栈同步维护每个状态下的最小值，push/pop/getMin 全 O(1)
- 时间 O(1) 所有操作，空间 O(n)
- 关键陷阱：辅助栈要与主栈同步 push/pop（即使最小值未变也要压入），保证状态一致

详细解析
---------
方法一：辅助栈（推荐，最清晰）
  - 主栈 stack：正常存储元素
  - 辅助栈 min_stack：每次 push 时记录当前最小值
    push(x): min_stack.push(min(x, min_stack.top()))
    pop():   两栈同步 pop
    getMin(): min_stack.top()
  - 关键：辅助栈大小与主栈相同，确保每个状态都有对应最小值

方法二：差值法（节省空间，但有溢出风险）
  - 仅用一个栈，存储 diff = val - current_min
  - push: 若 diff < 0，更新 min；存入 diff
  - pop:  若栈顶 diff < 0，说明 min 是当前最小，pop 后还原 min = min - diff
  - getMin: 直接返回 self.min
  - 缺点：diff 可能超出 int 范围（Python 无溢出，Java/C++ 需注意）

方法三：存 (val, min) 对
  - 主栈存 (元素值, 当前最小值) 的元组，直接从元组第二项取最小值
  - 空间略大（每个元素存两份），但实现最简单
"""


class MinStack:
    """
    方法一：辅助栈，所有操作 O(1)，空间 O(n)。
    """

    def __init__(self):
        self.stack = []        # 主栈
        self.min_stack = []    # 辅助栈，每个位置存当前最小值

    def push(self, val: int) -> None:
        self.stack.append(val)
        # 辅助栈：取当前 val 与已有最小值中的较小值
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()   # 同步弹出

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


class MinStackDiff:
    """
    方法二：差值法，O(1) 时间，O(n) 空间（只用一个栈）。
    注意：Python 整数无溢出，若用 Java/C++ 需注意 long 类型。
    """

    def __init__(self):
        self.stack = []        # 存 diff = val - self.min
        self.min = float('inf')

    def push(self, val: int) -> None:
        diff = val - self.min
        self.stack.append(diff)
        if diff < 0:           # val 比当前 min 更小，更新 min
            self.min = val

    def pop(self) -> None:
        diff = self.stack.pop()
        if diff < 0:           # 弹出的是最小值，还原上一个最小值
            # min 当时被更新为 val，即 min = val，diff = val - prev_min
            # => prev_min = val - diff = min - diff
            self.min = self.min - diff

    def top(self) -> int:
        diff = self.stack[-1]
        if diff < 0:
            return self.min       # 当时 val == min
        return self.min + diff    # val = min + diff

    def getMin(self) -> int:
        return self.min


class MinStackPair:
    """
    方法三：存 (val, min) 对，实现最直观。
    """

    def __init__(self):
        self.stack = []  # 存 (val, current_min)

    def push(self, val: int) -> None:
        curr_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, curr_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


if __name__ == "__main__":
    def test_min_stack(StackClass):
        ms = StackClass()
        ms.push(-2)
        ms.push(0)
        ms.push(-3)
        assert ms.getMin() == -3, f"{StackClass.__name__}: getMin should be -3"
        ms.pop()
        assert ms.top() == 0, f"{StackClass.__name__}: top should be 0"
        assert ms.getMin() == -2, f"{StackClass.__name__}: getMin should be -2"

        # 连续相同最小值
        ms2 = StackClass()
        ms2.push(1)
        ms2.push(1)
        assert ms2.getMin() == 1
        ms2.pop()
        assert ms2.getMin() == 1

        # 递减序列
        ms3 = StackClass()
        for v in [5, 3, 1, 2]:
            ms3.push(v)
        assert ms3.getMin() == 1
        ms3.pop()       # pop 2
        assert ms3.getMin() == 1
        ms3.pop()       # pop 1
        assert ms3.getMin() == 3

    for cls in [MinStack, MinStackDiff, MinStackPair]:
        test_min_stack(cls)

    print("All tests passed.")
