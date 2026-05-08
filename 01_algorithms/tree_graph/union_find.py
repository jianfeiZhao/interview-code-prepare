"""
题目：并查集（Union-Find）模板
难度：Medium | 高频出现：字节/阿里/腾讯
标签：并查集、图连通分量
LeetCode：#547（省份数量）, #684（冗余连接）, #990（等式方程可满足性）

题目描述
---------
并查集（Union-Find / Disjoint Set Union）是一种支持以下两种操作的数据结构：
  - find(x)：查找元素 x 所属的集合（返回根节点）
  - union(x, y)：将元素 x 和 y 所在的两个集合合并

常见应用题型：
  - #547 省份数量：判断城市连通分量个数
  - #684 冗余连接：找到使无向图构成环的额外边
  - #990 等式方程可满足性：判断变量约束是否矛盾

示例
------
uf = UnionFind(5)
uf.union(0, 1); uf.union(1, 2)
uf.find(0) == uf.find(2)  # True，同一连通分量
uf.find(0) == uf.find(3)  # False

约束
------
- 使用路径压缩 + 按秩合并，均摊时间复杂度接近 O(α(n))（反阿克曼函数，接近 O(1)）

TL;DR（30秒速览）
- find：路径压缩，接近 O(1) 均摊
- union：按秩合并，树高 O(log n)
- 应用：连通分量、判断是否成环、最小生成树

详细解析
---------
并查集核心操作：
  find(x)：找到 x 的根节点，路径压缩（将路径上所有节点直接指向根）
  union(x, y)：合并两个集合，按秩（树高）合并

时间复杂度：
  路径压缩 + 按秩合并 → 近乎 O(α(n)) ≈ O(1)（α为反阿克曼函数）
"""

from typing import List


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # 连通分量数

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # 已连通
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


def find_circle_num(is_connected: List[List[int]]) -> int:
    """#547：省份数量（连通分量数）"""
    n = len(is_connected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i+1, n):
            if is_connected[i][j]:
                uf.union(i, j)
    return uf.count


def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """#684：找冗余连接（成环的那条边）"""
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []


if __name__ == "__main__":
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2)
    assert not uf.connected(0, 3)
    assert uf.count == 3

    assert find_circle_num([[1,1,0],[1,1,0],[0,0,1]]) == 2
    assert find_circle_num([[1,0,0],[0,1,0],[0,0,1]]) == 3

    assert find_redundant_connection([[1,2],[1,3],[2,3]]) == [2,3]
    print("All tests passed.")
