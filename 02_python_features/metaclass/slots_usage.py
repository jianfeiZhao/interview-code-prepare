"""
题目：__slots__ 内存优化
难度：Medium | 高频出现：阿里/字节
标签：__slots__、内存优化、对象模型

题目描述
---------
Python 对象默认通过实例的 __dict__（字典）存储属性，字典本身有较大内存开销。
__slots__ 允许在类级别预先声明全部实例属性，Python 改用紧凑的 C 结构体存储，
从而消除 __dict__，在大量实例场景下可节省 40-50% 内存。
本题演示 __slots__ 的声明方式、内存对比测量，以及不能动态添加属性的限制，
并展示如何通过 __getstate__/__setstate__ 让 __slots__ 类支持 pickle 序列化。

示例/场景
---------
场景：创建 PointDict（普通类）与 PointSlots（__slots__ 类）各一个实例，
用 sys.getsizeof 对比内存占用；尝试对 __slots__ 实例动态添加属性触发 AttributeError；
演示带 pickle 支持的 __slots__ 类的序列化/反序列化。

关键概念
---------
- __dict__：Python 实例默认的属性字典，灵活但内存开销较大
- __slots__：类级别属性名元组，禁用 __dict__，改用固定内存块，节省内存
- 内存节省幅度：大量小对象（百万级）时效果显著，通常节省 30-50%
- 限制：声明 __slots__ 后不可动态添加未声明的属性（AttributeError）
- pickle 兼容：__slots__ 类需手动实现 __getstate__/__setstate__ 才能被 pickle
- 适用场景：属性固定的数据类、高频创建的轻量对象（如坐标点、日志记录）

TL;DR（30秒速览）
- __slots__ 禁用 __dict__，用固定内存块存属性，显著节省内存
- 适用于大量实例的轻量对象（如数据记录类）
- 代价：不能动态添加属性，不能被 pickle 默认处理（需自定义）

详细解析
---------
Python 对象默认有 __dict__（字典）存储实例属性，字典有较大开销。
__slots__ 预先声明属性名，Python 用更紧凑的 C 结构体存储，节省 30-50% 内存。

使用建议：
  - 大量小对象（百万级）时使用
  - 对象属性固定不变时使用
  - 不需要 __dict__（动态属性）时使用
"""

import sys


class PointDict:
    """普通类，使用 __dict__"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class PointSlots:
    """使用 __slots__ 的类"""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class PointSlotsWithPickle:
    """支持 pickle 的 __slots__ 类"""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getstate__(self):
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __setstate__(self, state):
        for key, val in state.items():
            setattr(self, key, val)


if __name__ == "__main__":
    p_dict = PointDict(1, 2, 3)
    p_slot = PointSlots(1, 2, 3)

    size_dict = sys.getsizeof(p_dict) + sys.getsizeof(p_dict.__dict__)
    size_slot = sys.getsizeof(p_slot)

    print(f"With __dict__: {size_dict} bytes")
    print(f"With __slots__: {size_slot} bytes")
    print(f"Memory saved: {size_dict - size_slot} bytes ({(1 - size_slot/size_dict)*100:.1f}%)")

    assert size_slot < size_dict, "__slots__ should use less memory"
    assert hasattr(p_dict, '__dict__')
    assert not hasattr(p_slot, '__dict__')

    # __slots__ 不能动态添加属性
    p_dict.w = 4  # OK
    try:
        p_slot.w = 4  # AttributeError
        assert False
    except AttributeError:
        pass

    import pickle
    p = PointSlotsWithPickle(1, 2, 3)
    restored = pickle.loads(pickle.dumps(p))
    assert restored.x == 1 and restored.y == 2 and restored.z == 3

    print("All tests passed.")
