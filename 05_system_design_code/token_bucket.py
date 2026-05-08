"""
题目：令牌桶限流器（Token Bucket Rate Limiter）
难度：Medium | 高频出现：字节/阿里/美团（后端岗）
标签：限流、令牌桶、系统设计


题目描述
---------
设计并实现令牌桶限流器（Token Bucket Rate Limiter）。
令牌桶以固定速率 rate 向桶中放入令牌，桶的最大容量为 capacity。
每次请求消耗一个令牌，桶空时拒绝请求。支持突发流量（桶满时可瞬间处理 capacity 个请求）。

接口设计：
  - allow_request(n=1) → bool：尝试消耗 n 个令牌，成功返回 True，失败返回 False
  - 使用懒更新（lazy refill）：请求到来时才计算应补充的令牌数

示例
------
limiter = TokenBucket(capacity=10, rate=2)  # 每秒补充2个，最多10个
limiter.allow_request()  # True（消耗1个）
...

约束
------
- 需要线程安全（多线程并发调用）
- 对比漏桶：令牌桶允许突发，漏桶严格匀速

TL;DR（30秒速览）
- 桶容量 capacity，每秒补充 rate 个令牌
- 每次请求消耗 1 个令牌；无令牌时拒绝
- 关键：懒更新——请求到来时才计算补充了多少令牌

详细解析
---------
令牌桶 vs 漏桶：
  令牌桶：允许突发流量（桶满时突发 capacity 个请求）
  漏桶：严格匀速处理，不允许突发

令牌桶参数：
  capacity：桶最大容量（突发上限）
  rate：每秒补充令牌数（稳态限制）

线程安全：多线程访问时用锁保护令牌计算
"""

import time
import threading


class TokenBucket:
    def __init__(self, capacity: float, rate: float):
        """
        capacity: 桶最大令牌数
        rate: 每秒补充令牌数
        """
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity    # 初始满桶
        self.last_time = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        """懒更新：根据流逝时间补充令牌"""
        now = time.monotonic()
        elapsed = now - self.last_time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_time = now

    def acquire(self, tokens: float = 1.0) -> bool:
        """尝试获取令牌，成功返回 True，失败返回 False"""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait_and_acquire(self, tokens: float = 1.0):
        """阻塞直到获得令牌"""
        while not self.acquire(tokens):
            time.sleep(1.0 / self.rate)


class SlidingWindowCounter:
    """
    滑动窗口计数限流器（基于时间窗口）
    比令牌桶更精确，但内存开销稍大
    """
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.requests = []  # 存储请求时间戳
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            cutoff = now - self.window
            self.requests = [t for t in self.requests if t > cutoff]
            if len(self.requests) < self.limit:
                self.requests.append(now)
                return True
            return False


if __name__ == "__main__":
    # 令牌桶测试
    bucket = TokenBucket(capacity=5, rate=2)  # 每秒2个，最多5个

    # 初始满桶，前5个请求全部通过
    results = [bucket.acquire() for _ in range(5)]
    assert all(results), "First 5 requests should pass"

    # 第6个请求被拒绝（桶空了）
    assert not bucket.acquire(), "6th request should be rejected"

    # 等待0.6秒，应该补充 ≈1.2 个令牌
    time.sleep(0.6)
    assert bucket.acquire(), "After refill, should be allowed"

    # 线程安全测试
    bucket2 = TokenBucket(capacity=100, rate=100)
    passed = []
    def test_thread():
        for _ in range(10):
            passed.append(bucket2.acquire())
    threads = [threading.Thread(target=test_thread) for _ in range(20)]
    for t in threads: t.start()
    for t in threads: t.join()
    # 总请求200次，容量100，通过的不超过100（允许少量误差）
    print(f"Passed: {sum(passed)}/200")

    # 滑动窗口测试
    sw = SlidingWindowCounter(limit=3, window_seconds=1.0)
    assert sw.allow() and sw.allow() and sw.allow()
    assert not sw.allow()  # 第4个被拒绝

    print("All tests passed.")
