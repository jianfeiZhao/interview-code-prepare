"""
题目：asyncio 协程基础
难度：Medium | 高频出现：字节/阿里
标签：异步、协程、事件循环

题目描述
---------
Python asyncio 是基于事件循环的异步并发框架。本题演示 asyncio 的核心用法：
用 async def 定义协程函数，用 await 主动让出控制权；用 asyncio.gather()
并发运行多个 I/O 任务（总耗时接近单个任务，而非累加）；用 asyncio.wait_for()
对协程设置超时。asyncio 适用于高并发 I/O 密集型场景（网络请求、数据库查询），
与多线程的本质区别在于：单线程内协作式切换，无线程切换开销，GIL 不构成瓶颈。

示例/场景
---------
场景一：顺序 await 3 个耗时 0.1s 的请求 → 总耗时 ~0.3s（低效）
场景二：asyncio.gather() 并发 3 个请求 → 总耗时 ~0.1s（推荐）
场景三：asyncio.Queue 实现生产者-消费者协程通信

关键概念
---------
- 事件循环（Event Loop）：统一调度所有协程的运行与切换
- 协程（Coroutine）：async def 函数，可在 await 处暂停并让出控制权
- Task：被事件循环主动调度的协程包装，asyncio.create_task() 立即入队
- asyncio.gather()：并发启动多个协程，等待全部完成后返回结果列表
- asyncio vs threading：asyncio 协作式（主动 yield），threading 抢占式（OS调度）；
  asyncio 在高并发 I/O 时开销更低，threading 更适合 CPU 密集型任务

TL;DR（30秒速览）
- async def 定义协程函数，await 让出控制权
- asyncio.gather() 并发运行多个协程
- 协程不是线程，单线程内切换，GIL 无影响

详细解析
---------
核心概念：
  - 事件循环（Event Loop）：调度协程的运行
  - 协程（Coroutine）：async def 函数，可被暂停和恢复
  - Task：被事件循环调度的协程包装
  - await：暂停当前协程，让事件循环去跑其他协程

asyncio vs threading：
  - asyncio 单线程，协作式（主动 yield）
  - threading 多线程，抢占式（OS调度）
  - asyncio 在高并发 I/O 时开销更低（无线程切换）

常用 API：
  asyncio.gather(*coros)    → 并发运行，等待全部完成
  asyncio.wait_for(coro, timeout)  → 超时控制
  asyncio.create_task(coro) → 立即调度，不等待
"""

import asyncio
import time


async def fetch_data(url: str, delay: float) -> str:
    """模拟异步 HTTP 请求"""
    await asyncio.sleep(delay)  # 模拟I/O等待，释放控制权
    return f"data from {url}"


async def main_sequential():
    """顺序执行（低效）"""
    start = time.time()
    r1 = await fetch_data("api/users", 0.1)
    r2 = await fetch_data("api/orders", 0.1)
    elapsed = time.time() - start
    print(f"Sequential: {elapsed:.2f}s")
    return [r1, r2]


async def main_concurrent():
    """并发执行（推荐）"""
    start = time.time()
    results = await asyncio.gather(
        fetch_data("api/users", 0.1),
        fetch_data("api/orders", 0.1),
        fetch_data("api/products", 0.1),
    )
    elapsed = time.time() - start
    print(f"Concurrent: {elapsed:.2f}s (3 tasks, ~0.1s total)")
    return results


async def producer_consumer():
    """生产者-消费者模式"""
    queue = asyncio.Queue(maxsize=5)

    async def producer():
        for i in range(5):
            await queue.put(i)
            await asyncio.sleep(0.01)
        await queue.put(None)  # 结束信号

    async def consumer():
        results = []
        while True:
            item = await queue.get()
            if item is None:
                break
            results.append(item * 2)
            queue.task_done()
        return results

    prod_task = asyncio.create_task(producer())
    results = await consumer()
    await prod_task
    return results


if __name__ == "__main__":
    # 并发执行3个任务，总时间约 0.1s 而非 0.3s
    results = asyncio.run(main_concurrent())
    assert len(results) == 3

    # 生产者消费者
    results = asyncio.run(producer_consumer())
    assert results == [0, 2, 4, 6, 8]

    print("All tests passed.")
