"""
题目：滑动窗口限流器（精确版）
难度：Medium | 高频出现：字节/阿里/美团
标签：限流、滑动窗口、Redis


题目描述
---------
设计并实现滑动窗口限流器（Sliding Window Rate Limiter）。
在任意 window_size 时间窗口内，允许最多 max_requests 个请求通过。
相比固定窗口（有边界突发问题），滑动窗口更平滑准确。

接口设计：
  - allow_request(user_id) → bool：判断该用户当前是否可以发起请求

两种实现：
  - 滑动窗口计数器（近似，精度与子窗口数量相关）
  - 滑动窗口日志（精确，记录每次请求时间戳）

示例
------
limiter = SlidingWindowRateLimiter(max_requests=100, window_size=60)
limiter.allow_request("user_1")  # True/False

约束
------
- 需要线程安全，高并发场景建议使用 Redis 原子操作

TL;DR（30秒速览）
- 维护时间窗口内的请求时间戳列表，每次请求时清理过期记录
- 精确但内存开销为 O(请求数)
- 生产中常用 Redis sorted set 实现（score=时间戳）

详细解析
---------
三种限流算法对比：
  固定窗口：边界时刻可能双倍流量（例如：窗口末尾+下窗口开始各发100）
  滑动窗口计数：估算（加权前窗口），比固定窗口更平滑
  滑动窗口精确：记录所有时间戳，精确但内存开销大

Redis sorted set 方案（生产常用）：
  key = user_id
  zadd key timestamp timestamp  # score=timestamp
  zremrangebyscore key 0 (now-window)
  zcard key  # 当前窗口计数
"""

import time
import threading
from collections import deque


class SlidingWindowRateLimiter:
    """精确滑动窗口（记录每次请求时间戳）"""

    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.timestamps = deque()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            cutoff = now - self.window
            while self.timestamps and self.timestamps[0] <= cutoff:
                self.timestamps.popleft()
            if len(self.timestamps) < self.limit:
                self.timestamps.append(now)
                return True
            return False

    def current_count(self) -> int:
        with self._lock:
            now = time.monotonic()
            cutoff = now - self.window
            while self.timestamps and self.timestamps[0] <= cutoff:
                self.timestamps.popleft()
            return len(self.timestamps)


class SlidingWindowCounterRateLimiter:
    """
    滑动窗口计数（加权估算，内存 O(1)）
    estimate = prev_count * overlap_ratio + curr_count
    overlap_ratio = (window - elapsed_in_curr) / window
    """

    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.prev_count = 0
        self.curr_count = 0
        self.curr_window_start = time.monotonic()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.curr_window_start

            if elapsed >= self.window:
                # 滚动到新窗口
                self.prev_count = self.curr_count if elapsed < 2 * self.window else 0
                self.curr_count = 0
                self.curr_window_start = now
                elapsed = 0

            overlap = (self.window - elapsed) / self.window
            estimate = self.prev_count * overlap + self.curr_count

            if estimate < self.limit:
                self.curr_count += 1
                return True
            return False


if __name__ == "__main__":
    # 精确滑动窗口测试
    limiter = SlidingWindowRateLimiter(limit=5, window_seconds=1.0)
    results = [limiter.allow() for _ in range(7)]
    assert results[:5] == [True] * 5
    assert results[5] == False
    assert results[6] == False
    print(f"Precise: {results}")

    # 等待窗口滑动
    time.sleep(0.5)
    # 窗口内还有5个，仍然被拒绝
    assert not limiter.allow()

    # 估算滑动窗口
    counter_limiter = SlidingWindowCounterRateLimiter(limit=10, window_seconds=1.0)
    passed = sum(counter_limiter.allow() for _ in range(15))
    print(f"Counter limiter passed: {passed}/15")
    assert 9 <= passed <= 11, f"Unexpected pass count: {passed}"

    print("All tests passed.")
