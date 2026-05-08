"""
题目：实现 retry 装饰器（自动重试）
难度：Medium | 高频出现：字节/阿里
标签：装饰器、异常处理、工程实践


题目描述
---------
实现一个通用的 retry 装饰器，使被装饰的函数在遇到指定异常时自动重试指定次数。
  - 支持 max_retries（最大重试次数）、delay（重试间隔秒数）、exceptions（可重试异常类型）
  - 进阶：支持指数退避（delay * 2^attempt）和随机抖动（jitter）
  - 超过最大次数后，将最后一次异常重新抛出

示例
------
@retry(max_retries=3, delay=1.0, exceptions=(ConnectionError,))
def call_api():
    ...  # 最多重试3次，每次等1秒

约束
------
- 适用于任何可调用对象，支持关键字参数传递

TL;DR（30秒速览）
- 思路：捕获指定异常，循环重试 max_retries 次，可加指数退避
- 关键点：最后一次失败要 raise，否则吞掉异常
- 进阶：指数退避 delay * (2 ** attempt)，抖动 random.uniform

详细解析
---------
retry 装饰器是工程中常见的弹性模式：
  1. 捕获可重试的异常类型
  2. 重试间隔可线性/指数增加
  3. 超过最大次数后重新抛出异常

指数退避（Exponential Backoff）：
  第 i 次重试等待 delay * 2^i 秒，避免服务雪崩
  加 jitter（抖动）避免多客户端同时重试
"""

import functools
import time
import random
from typing import Type, Tuple


def retry(
    max_retries: int = 3,
    delay: float = 0.1,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    backoff: bool = True,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise  # 最后一次失败，重新抛出
                    wait = delay * (2 ** attempt) if backoff else delay
                    wait += random.uniform(0, wait * 0.1)  # 加抖动
                    print(f"[retry] {func.__name__} failed ({e}), retrying in {wait:.2f}s "
                          f"({attempt+1}/{max_retries})")
                    time.sleep(wait)
        return wrapper
    return decorator


# 示例：模拟不稳定的网络请求
call_count = 0

@retry(max_retries=3, delay=0.01, exceptions=(ConnectionError,))
def unstable_request():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("Network error")
    return "success"


if __name__ == "__main__":
    call_count = 0
    result = unstable_request()
    assert result == "success"
    assert call_count == 3

    import pytest
    # 超过最大重试次数时应该抛出异常
    @retry(max_retries=2, delay=0.01, exceptions=(ValueError,))
    def always_fail():
        raise ValueError("always fails")

    try:
        always_fail()
        assert False, "Should have raised"
    except ValueError:
        pass

    print("All tests passed.")
