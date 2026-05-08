"""
题目：线程安全消息队列（生产者-消费者）
难度：Medium | 高频出现：字节/阿里/腾讯
标签：并发、队列、生产者消费者、条件变量


题目描述
---------
设计并实现线程安全的有界队列（Bounded Thread-Safe Queue），支持阻塞式生产者-消费者模式。

接口设计：
  - put(item, block=True, timeout=None)：入队，满时阻塞等待
  - get(block=True, timeout=None)：出队，空时阻塞等待
  - qsize() → int：当前队列大小
  - empty() / full() → bool：是否空/满

关键实现：使用 Lock + Condition 实现线程间通知（notify/wait），
或使用 threading.Semaphore 控制容量。

示例
------
q = ThreadSafeQueue(maxsize=10)
# 生产者线程
q.put(item)   # 满时阻塞
# 消费者线程
item = q.get()  # 空时阻塞

约束
------
- 需防止死锁，正确处理 timeout 参数
- Python 标准库 queue.Queue 是参考实现

TL;DR（30秒速览）
- 用 Lock + Condition 实现有界阻塞队列
- put()：队列满时阻塞；get()：队列空时阻塞
- Python 标准库 queue.Queue 已内置，但面试常考手写

详细解析
---------
关键同步原语：
  Lock：互斥锁，防止并发修改
  Condition：条件变量（内含 Lock），支持 wait/notify
  Semaphore：计数信号量，可用于实现有界队列

condition.wait()：释放锁并阻塞，被 notify 后重新获得锁
condition.notify_all()：唤醒所有等待线程

生产者-消费者模式是并发编程的基础，常见于：
  线程池任务队列、消息队列、流水线处理
"""

import threading
from typing import Generic, TypeVar
from collections import deque

T = TypeVar('T')


class BoundedBlockingQueue(Generic[T]):
    """有界阻塞队列（手写版 queue.Queue）"""

    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self._queue = deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item: T, timeout: float = None) -> bool:
        """入队，队满时阻塞（直到有空位或超时）"""
        with self._not_full:
            if not self._not_full.wait_for(
                lambda: len(self._queue) < self.maxsize,
                timeout=timeout
            ):
                return False  # 超时
            self._queue.append(item)
            self._not_empty.notify()
            return True

    def get(self, timeout: float = None) -> T:
        """出队，队空时阻塞（直到有数据或超时）"""
        with self._not_empty:
            if not self._not_empty.wait_for(
                lambda: len(self._queue) > 0,
                timeout=timeout
            ):
                raise TimeoutError("Queue is empty and timeout exceeded")
            item = self._queue.popleft()
            self._not_full.notify()
            return item

    def qsize(self) -> int:
        with self._lock:
            return len(self._queue)

    def empty(self) -> bool:
        return self.qsize() == 0

    def full(self) -> bool:
        with self._lock:
            return len(self._queue) >= self.maxsize


if __name__ == "__main__":
    import time

    q = BoundedBlockingQueue(maxsize=5)
    produced = []
    consumed = []
    SENTINEL = object()

    def producer():
        for i in range(20):
            q.put(i)
            produced.append(i)
            time.sleep(0.001)
        q.put(SENTINEL)

    def consumer():
        while True:
            item = q.get()
            if item is SENTINEL:
                break
            consumed.append(item)
            time.sleep(0.002)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert sorted(produced) == sorted(consumed), "All items should be consumed"
    assert produced == list(range(20))
    print(f"Produced: {len(produced)}, Consumed: {len(consumed)}")

    # 超时测试
    q2 = BoundedBlockingQueue(maxsize=2)
    q2.put(1)
    q2.put(2)
    result = q2.put(3, timeout=0.05)
    assert not result, "Should timeout when queue is full"

    print("All tests passed.")
