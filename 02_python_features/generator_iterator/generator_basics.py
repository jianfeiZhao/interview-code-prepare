"""
题目：生成器和 yield 的使用
难度：Medium | 高频出现：字节/阿里
标签：生成器、迭代器、惰性求值


题目描述
---------
实现和理解 Python 生成器（Generator）的基本概念和使用场景。
生成器是使用 yield 关键字的函数，每次 next() 调用时从上次 yield 处继续执行，
相比列表推导式节省内存，适合处理大型数据流或无限序列。

实现以下几个典型生成器：
  - 无限计数器、斐波那契数列生成器
  - 文件分块读取生成器
  - 管道式数据处理（生成器链式组合）

示例
------
for num in fibonacci():
    if num > 100: break
    print(num)  # 懒加载，不预先计算所有值

约束
------
- 掌握 yield、yield from、send()、throw()、close() 等接口

TL;DR（30秒速览）
- yield：暂停函数执行，返回值给调用方；下次 next() 从暂停处继续
- 生成器表达式：(x*x for x in range(10))，比列表推导式节省内存
- send()：向生成器发送值，yield 表达式的值就是 send 传入的值

详细解析
---------
生成器 vs 迭代器：
  - 迭代器：实现 __iter__ + __next__ 的对象
  - 生成器：用 yield 定义的函数，是迭代器的语法糖

yield from：
  委托子生成器，等价于 for item in sub_gen: yield item
  但 yield from 还能传递 send/throw/close

典型应用：
  1. 大文件逐行读取
  2. 无限序列（斐波那契、计数器）
  3. 协程（基于 send 的数据管道）
"""

from typing import Generator, Iterator


def infinite_counter(start: int = 0) -> Generator[int, None, None]:
    """无限计数器"""
    n = start
    while True:
        yield n
        n += 1


def fibonacci() -> Generator[int, None, None]:
    """无限斐波那契序列"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_large_file(filepath: str, chunk_size: int = 1024):
    """逐块读取大文件（节省内存）"""
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk


def flatten(nested) -> Generator:
    """递归展开嵌套列表，使用 yield from"""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def echo_generator():
    """接收 send 值的双向生成器"""
    received = None
    while True:
        received = yield received  # send 的值赋给 received


if __name__ == "__main__":
    # 无限计数器取前5个
    counter = infinite_counter(10)
    assert [next(counter) for _ in range(5)] == [10, 11, 12, 13, 14]

    # 斐波那契前10项
    fib = fibonacci()
    fibs = [next(fib) for _ in range(10)]
    assert fibs == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # 展开嵌套列表
    assert list(flatten([1, [2, [3, 4], 5], 6])) == [1, 2, 3, 4, 5, 6]

    # send 双向通信
    gen = echo_generator()
    next(gen)  # 启动生成器（推进到第一个 yield）
    assert gen.send("hello") == "hello"
    assert gen.send(42) == 42

    print("All tests passed.")
