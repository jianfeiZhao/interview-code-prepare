"""
题目：实现自定义迭代器
难度：Easy | 高频出现：字节/阿里
标签：迭代器协议、__iter__、__next__


题目描述
---------
实现自定义迭代器（Iterator），理解 Python 迭代协议。
迭代器需实现 __iter__（返回 self）和 __next__（返回下一个元素或抛出 StopIteration）。
可迭代对象（Iterable）只需实现 __iter__ 并返回一个迭代器。

常见面试考点：
  - 自定义范围迭代器
  - 环形迭代器
  - 链式迭代器（itertools.chain 的实现原理）

示例
------
class CountDown:
    def __init__(self, start): ...
    def __iter__(self): return self
    def __next__(self): ...

for i in CountDown(5):
    print(i)  # 5 4 3 2 1

约束
------
- 掌握迭代器（Iterator）与可迭代对象（Iterable）的区别

TL;DR（30秒速览）
- 迭代器协议：实现 __iter__（返回self）和 __next__（返回下一个值或 raise StopIteration）
- 可迭代对象：实现 __iter__（返回一个迭代器），不一定有 __next__
- 迭代器 ≠ 可迭代对象（但迭代器通常也是可迭代对象）

详细解析
---------
for x in obj 背后：
  1. iter(obj) → 调用 obj.__iter__() 获取迭代器
  2. 循环调用 next(iterator) → iterator.__next__()
  3. 捕获 StopIteration → 循环结束
"""


class Range:
    """手动实现 range 行为"""
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return RangeIterator(self.start, self.stop, self.step)

    def __len__(self):
        return max(0, (self.stop - self.start + self.step - 1) // self.step)


class RangeIterator:
    def __init__(self, start, stop, step):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self  # 迭代器本身也是可迭代的

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += self.step
        return val


class InfiniteCounter:
    """可迭代对象（使用 islice 截断）"""
    def __iter__(self):
        n = 0
        while True:
            yield n
            n += 1


if __name__ == "__main__":
    from itertools import islice

    r = Range(0, 10, 2)
    assert list(r) == [0, 2, 4, 6, 8]
    assert list(r) == [0, 2, 4, 6, 8]  # 可重复迭代（可迭代对象）

    it = iter(r)
    assert next(it) == 0
    assert next(it) == 2

    # InfiniteCounter 截取前5个
    counter = InfiniteCounter()
    assert list(islice(counter, 5)) == [0, 1, 2, 3, 4]

    print("All tests passed.")
