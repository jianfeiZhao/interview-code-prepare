"""
题目：GIL 与多线程/多进程的选择
难度：Medium | 高频出现：字节/腾讯
标签：并发、GIL、threading、multiprocessing


题目描述
---------
理解 Python GIL（全局解释器锁）对多线程并发的影响，以及如何使用 threading 模块。
GIL 使得 CPython 同一时刻只有一个线程执行 Python 字节码，
因此多线程对 CPU 密集型任务无法真正并行，但对 I/O 密集型任务仍有效。

实现以下并发模式：
  - 多线程下载（I/O 密集型的提速场景）
  - 线程锁（避免竞态条件）
  - 生产者-消费者模式（threading.Queue）

示例
------
# CPU 密集型：多进程（multiprocessing）
# I/O 密集型：多线程（threading）或异步（asyncio）

约束
------
- 掌握 Lock、RLock、Semaphore、Event、Condition 等同步原语

TL;DR（30秒速览）
- GIL：CPython 全局解释器锁，同一时刻只有一个线程执行字节码
- CPU密集型 → multiprocessing（绕过GIL）
- I/O密集型 → threading 或 asyncio（GIL 在I/O等待时主动释放）

详细解析
---------
GIL 存在原因：
  CPython 的内存管理（引用计数）不是线程安全的，GIL 保护对象引用计数

GIL 的影响：
  - 多线程无法真正并行执行 Python 字节码
  - I/O 等待、系统调用时 GIL 会释放，所以 I/O 密集型多线程有效
  - time.sleep() 也会释放 GIL

何时用 threading vs multiprocessing vs asyncio：
  - 网络请求/文件读写 → asyncio（协程，单线程高并发）
  - 并发 I/O 且用同步库 → threading（线程池）
  - 计算密集（矩阵运算/图像处理）→ multiprocessing 或 numpy/numba
"""

import threading
import multiprocessing
import time


def cpu_bound_task(n: int) -> int:
    """CPU密集型：纯计算"""
    total = 0
    for i in range(n):
        total += i * i
    return total


def io_bound_task(seconds: float) -> str:
    """I/O密集型模拟：sleep 期间 GIL 释放"""
    time.sleep(seconds)
    return f"done after {seconds}s"


def demo_threading_io():
    """多线程适合I/O密集型"""
    start = time.time()
    threads = [threading.Thread(target=io_bound_task, args=(0.1,)) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.time() - start
    print(f"Threading IO: {elapsed:.2f}s (expected ~0.1s, not ~1s)")
    return elapsed


def demo_multiprocessing_cpu():
    """多进程适合CPU密集型"""
    start = time.time()
    with multiprocessing.Pool(4) as pool:
        pool.map(cpu_bound_task, [10**6] * 4)
    elapsed = time.time() - start
    print(f"Multiprocessing CPU: {elapsed:.2f}s")
    return elapsed


# 线程安全示例：用锁保护共享变量
class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1

    @property
    def count(self):
        return self._count


if __name__ == "__main__":
    # 测试线程安全计数器
    counter = ThreadSafeCounter()
    threads = [threading.Thread(target=counter.increment) for _ in range(1000)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert counter.count == 1000, f"Expected 1000, got {counter.count}"
    print(f"ThreadSafeCounter: {counter.count}")

    elapsed = demo_threading_io()
    assert elapsed < 0.5, "Threading should speed up I/O tasks"

    print("All tests passed.")
