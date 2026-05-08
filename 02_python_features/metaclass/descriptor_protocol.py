"""
题目：描述符协议（Descriptor Protocol）
难度：Hard | 高频出现：字节/阿里（高级岗）
标签：描述符、property、__get__、__set__


题目描述
---------
理解并实现 Python 描述符协议（Descriptor Protocol）。
描述符是定义了 __get__、__set__ 或 __delete__ 方法的对象，
当作为类属性使用时，可以控制属性的访问行为。常见应用：property、classmethod、staticmethod。

数据描述符（同时实现 __get__ 和 __set__）优先级高于实例字典。
非数据描述符（只有 __get__）优先级低于实例字典。

示例
------
class Validator:
    def __set_name__(self, owner, name): self.name = name
    def __get__(self, obj, type=None): ...
    def __set__(self, obj, value): ...  # 带验证的属性赋值

约束
------
- 掌握数据描述符 vs 非数据描述符的区别
- 理解 MRO（方法解析顺序）与描述符查找顺序

TL;DR（30秒速览）
- 描述符：实现了 __get__/__set__/__delete__ 的类
- property 是描述符的语法糖
- 数据描述符（__get__+__set__）优先级 > 实例 __dict__ > 非数据描述符

详细解析
---------
描述符协议核心方法：
  __get__(self, obj, objtype=None) → 属性访问时调用
  __set__(self, obj, value)        → 属性赋值时调用
  __delete__(self, obj)            → del 属性时调用

应用场景：
  1. 类型验证（如 Django ORM 的字段类型检查）
  2. 懒加载属性
  3. 缓存属性（@cached_property）
"""

from functools import cached_property


class TypedAttribute:
    """类型检查描述符"""
    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.storage_name = f"_{owner.__name__}_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # 通过类访问时返回描述符本身
        return getattr(obj, self.storage_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, self.storage_name, value)


class Person:
    name = TypedAttribute('name', str)
    age = TypedAttribute('age', int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


class Circle:
    """使用 cached_property 懒加载"""
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        import math
        print("Computing area...")  # 只计算一次
        return math.pi * self.radius ** 2


if __name__ == "__main__":
    p = Person("Alice", 30)
    assert p.name == "Alice"
    assert p.age == 30

    try:
        p.age = "thirty"
        assert False
    except TypeError as e:
        print(f"Caught: {e}")

    c = Circle(5)
    area1 = c.area  # 计算
    area2 = c.area  # 直接从缓存取，不重新计算
    assert area1 == area2
    assert abs(area1 - 78.539) < 0.01

    print("All tests passed.")
