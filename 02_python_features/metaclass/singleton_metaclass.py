"""
题目：实现单例模式（多种方式）
难度：Medium | 高频出现：字节/阿里/腾讯
标签：设计模式、metaclass、装饰器


题目描述
---------
实现单例模式（Singleton Pattern），确保一个类只有一个实例，并提供全局访问点。
Python 中有多种实现方式：
  1. 元类（Metaclass）：重写 __call__
  2. 装饰器：包装类的实例化逻辑
  3. __new__ 方法：在类内部控制实例化
  4. 模块级变量（最 Pythonic）

示例
------
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True，同一个实例

约束
------
- 需要考虑线程安全（多线程环境下的单例）
- 元类方式最通用，可复用于任意类

TL;DR（30秒速览）
- 单例保证类只有一个实例
- 面试推荐用 metaclass 方式（体现对 Python 对象模型的理解）
- 线程安全版需加锁

详细解析
---------
Python 实现单例的5种方式：
1. __new__ 方法
2. 装饰器
3. metaclass（推荐，体现对 type 的理解）
4. 模块级变量（Python 天然单例，最简单）
5. 枚举（线程安全）

metaclass 原理：
  type 是所有类的元类，__call__ 触发 __new__ 和 __init__
  重写 metaclass 的 __call__ 可以控制实例创建过程
"""

import threading


# 方法1：__new__ 方法
class SingletonNew:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# 方法2：装饰器实现（线程安全）
def singleton(cls):
    instances = {}
    lock = threading.Lock()
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:  # 双重检查锁
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DatabaseConn:
    def __init__(self, url="localhost"):
        self.url = url


# 方法3：metaclass（最推荐）
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    def __init__(self, env="prod"):
        self.env = env


if __name__ == "__main__":
    # 测试 __new__ 单例
    s1, s2 = SingletonNew(), SingletonNew()
    assert s1 is s2

    # 测试装饰器单例
    db1, db2 = DatabaseConn("db1"), DatabaseConn()
    assert db1 is db2

    # 测试 metaclass 单例
    cfg1, cfg2 = AppConfig("dev"), AppConfig()
    assert cfg1 is cfg2
    assert cfg1.env == "dev"  # 第二次 __init__ 参数被忽略

    # 线程安全测试
    results = []
    def create_instance():
        results.append(AppConfig())
    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert all(r is results[0] for r in results)

    print("All tests passed.")
