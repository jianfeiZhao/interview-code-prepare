"""
题目：实现一个带参数的装饰器
难度：Medium | 高频出现：字节/阿里/腾讯
标签：装饰器、闭包、函数式编程


题目描述
---------
实现带参数的装饰器（装饰器工厂模式）。
带参数的装饰器需要三层函数嵌套：外层接受参数、中层接受函数、内层接受调用参数。
常见场景：日志级别、权限控制、缓存 TTL 等需要在装饰时传入配置的情况。

示例
------
@log(level='INFO', prefix='[API]')
def fetch_data(url):
    ...

约束
------
- 装饰器必须保留原函数的名称和文档字符串（使用 functools.wraps）

TL;DR（30秒速览）
- 思路：三层嵌套：outer(参数) → decorator(func) → wrapper(*args, **kwargs)
- 关键：@functools.wraps(func) 保留原函数的 __name__、__doc__ 等元信息
- 陷阱：@decorator vs @decorator() 的区别（有无参数时语法不同）

详细解析
---------
无参装饰器：@decorator（两层函数）
有参装饰器：@decorator(args)（三层函数，最外层接收参数，返回一个无参装饰器）

@functools.wraps(func) 必须加，否则 func.__name__ 会变成 'wrapper'

常考变体：
  1. 带参数的 @timer(unit='ms') 计时装饰器
  2. 权限检查 @require_role('admin')
  3. 参数验证 @validate(type_map={'name': str})
"""

import functools
import time


def timer(unit: str = 's'):
    """带参数的计时装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if unit == 'ms':
                elapsed *= 1000
            print(f"{func.__name__} took {elapsed:.4f} {unit}")
            return result
        return wrapper
    return decorator


def repeat(n: int):
    """重复执行 n 次的装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@timer(unit='ms')
def slow_func():
    time.sleep(0.01)
    return 42


@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
    return name


if __name__ == "__main__":
    # 验证 wraps 保留了函数信息
    assert slow_func.__name__ == 'slow_func'
    result = slow_func()
    assert result == 42

    assert greet.__name__ == 'greet'
    greet("Alice")
    print("All tests passed.")
