"""
题目：上下文管理器（contextmanager）
难度：Medium | 高频出现：字节/阿里
标签：上下文管理器、with 语句、资源管理


题目描述
---------
实现上下文管理器（Context Manager），支持 with 语句的资源管理。
两种实现方式：
  1. 基于类：实现 __enter__ 和 __exit__ 方法
  2. 基于 contextlib.contextmanager 装饰器（生成器方式）

常见用途：文件操作、数据库事务、锁管理、计时器、临时状态切换等。

示例
------
with Timer() as t:
    expensive_computation()
print(f"耗时: {t.elapsed:.3f}s")

约束
------
- __exit__ 接受三个异常参数（exc_type, exc_val, exc_tb），返回 True 可抑制异常

TL;DR（30秒速览）
- 实现 __enter__/__exit__ 协议 或 用 @contextmanager 装饰器
- __exit__ 参数：(exc_type, exc_val, exc_tb)，返回 True 可吞掉异常
- @contextmanager：yield 前是 __enter__，yield 后是 __exit__

详细解析
---------
两种实现方式：
1. 类方式：__enter__ + __exit__（适合复杂资源管理）
2. @contextmanager 装饰器（代码更简洁）

常见用途：
  - 文件/数据库连接管理
  - 锁的获取与释放
  - 临时改变环境（切换目录、修改配置）
  - 计时器
"""

import time
from contextlib import contextmanager


class Timer:
    """计时器上下文管理器（类方式）"""
    def __init__(self, name=""):
        self.name = name
        self.elapsed = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self  # 绑定到 as 子句

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"{self.name}: {self.elapsed*1000:.2f}ms")
        return False  # 不吞掉异常


@contextmanager
def timer(name=""):
    """计时器上下文管理器（装饰器方式）"""
    start = time.perf_counter()
    try:
        yield  # with 块的代码在这里执行
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name}: {elapsed:.2f}ms")


@contextmanager
def managed_resource(name: str):
    """模拟资源管理（如数据库连接）"""
    print(f"Acquiring {name}")
    resource = {"name": name, "active": True}
    try:
        yield resource
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        resource["active"] = False
        print(f"Releasing {name}")


if __name__ == "__main__":
    # 类方式
    with Timer("class-timer") as t:
        time.sleep(0.01)
    assert t.elapsed > 0.01

    # 装饰器方式
    with timer("decorator-timer"):
        time.sleep(0.01)

    # 资源管理
    with managed_resource("db_conn") as res:
        assert res["active"] == True
        assert res["name"] == "db_conn"
    assert res["active"] == False

    print("All tests passed.")
