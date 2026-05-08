# 面试速查卡 Cheatsheet

> 30分钟过完核心考点，面试前必看。

---

## 一、算法复杂度速查

| 数据结构/算法 | 平均时间 | 最坏时间 | 空间 |
|-------------|---------|---------|------|
| 哈希表 查找/插入 | O(1) | O(n) | O(n) |
| 二叉搜索树 查找 | O(log n) | O(n) | O(n) |
| 堆 插入/删除 | O(log n) | O(log n) | O(n) |
| 快速排序 | O(n log n) | O(n²) | O(log n) |
| 归并排序 | O(n log n) | O(n log n) | O(n) |
| 二分查找 | O(log n) | O(log n) | O(1) |
| BFS/DFS | O(V+E) | O(V+E) | O(V) |
| DP（通常） | O(n²) | - | O(n) |

---

## 二、常见题型 → 解题模式

### 数组/字符串
```
找两数/三数之和        → 哈希表 or 双指针（排序后）
子数组最大和/积        → Kadane 算法（DP）
接雨水/柱状图          → 单调栈 or 双指针
括号匹配/字符串解码    → 栈
滑动窗口（最长/最短）  → 双指针 + 哈希/计数
```

### 链表
```
反转链表               → 迭代（prev/cur/next 三指针）
找环/入环点            → 快慢指针 Floyd 算法
合并有序链表           → 递归 or 虚拟头节点迭代
找链表倒数第K节点      → 快慢指针（快指针先走K步）
```

### 树
```
前/中/后序遍历         → 递归 or 迭代（栈）
层序遍历               → BFS（队列）
最近公共祖先 LCA       → 后序DFS
序列化/反序列化        → 前序遍历 + 队列重建
```

### 动态规划 DP
```
状态定义：dp[i] 表示...到第i个元素时的最优解
初始化：dp[0] 或 dp[0][0] 的边界值
转移：dp[i] = f(dp[i-1], dp[i-2], ...)
子问题类型：
  - 线性DP：爬楼梯、打家劫舍、股票买卖
  - 二维DP：LCS、编辑距离、背包问题
  - 区间DP：戳气球、矩阵链乘
```

### 回溯
```python
def backtrack(path, choices):
    if 终止条件:
        result.append(path[:])
        return
    for choice in choices:
        做选择
        backtrack(path, 新choices)
        撤销选择
```

### 二分查找模板
```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target: return mid
    elif nums[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```

---

## 三、Python 核心考点速记

### 装饰器
```python
def decorator(func):
    @functools.wraps(func)          # 保留原函数信息
    def wrapper(*args, **kwargs):
        # 前置逻辑
        result = func(*args, **kwargs)
        # 后置逻辑
        return result
    return wrapper
```

### 生成器 vs 迭代器
- `yield` → 生成器函数，惰性求值，节省内存
- `__iter__` + `__next__` → 自定义迭代器
- `yield from` → 委托子生成器

### GIL（全局解释器锁）
- Python 同一时刻只有一个线程执行字节码
- **CPU 密集型** → 用 `multiprocessing`（绕过GIL）
- **I/O 密集型** → 用 `threading` 或 `asyncio`（GIL 在I/O等待时释放）

### 常用内置工具
```python
from collections import defaultdict, Counter, deque, OrderedDict
from heapq import heappush, heappop, nlargest, nsmallest
from functools import lru_cache, wraps, reduce
from itertools import product, permutations, combinations
import bisect  # 二分插入
```

---

## 四、ML 核心公式速查

### 常用激活函数
| 函数 | 公式 | 导数 | 特点 |
|-----|------|------|------|
| Sigmoid | 1/(1+e⁻ˣ) | σ(1-σ) | 梯度消失 |
| ReLU | max(0,x) | 0 or 1 | 稀疏激活 |
| Softmax | eˣⁱ/Σeˣʲ | - | 多分类输出 |

### BatchNorm
```
μ = mean(x), σ² = var(x)
x̂ = (x - μ) / sqrt(σ² + ε)
y = γ·x̂ + β
```

### LayerNorm（LLM 常用）
```
对每个样本的特征维度归一化（而非batch维度）
```

---

## 五、大模型算法速记

### Attention 计算
```
Q, K, V = XWq, XWk, XWv
Attention = softmax(QKᵀ / √d_k) · V
```
- `√d_k` 缩放防止点积过大导致 softmax 梯度消失

### MHA vs MQA vs GQA
| 类型 | Q头数 | K/V头数 | 代表模型 |
|-----|-------|---------|---------|
| MHA | H | H | BERT, GPT-2 |
| MQA | H | 1 | PaLM |
| GQA | H | G (1<G<H) | LLaMA2, Mistral |

### RoPE 核心思想
- 将位置信息编码为旋转矩阵，作用在 Q/K 上
- 相对位置通过 Q·Kᵀ 内积自然体现

### KV Cache
- 推理时缓存每层的 K/V，避免重复计算
- 显存占用：`2 × n_layers × seq_len × n_heads × head_dim × dtype_bytes`

### Top-k / Top-p 采样
- **Top-k**：只从概率最高的 k 个 token 中采样
- **Top-p (nucleus)**：从累积概率 ≥ p 的最小 token 集合采样

### PPO vs DPO
| | PPO | DPO |
|---|-----|-----|
| 需要奖励模型 | 是 | 否 |
| 训练复杂度 | 高 | 低 |
| 稳定性 | 较难调参 | 更稳定 |

---

## 六、系统设计代码快速模板

### LRU Cache（OrderedDict 实现）
```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = OrderedDict()
    def get(self, key):
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    def put(self, key, value):
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
```

### 令牌桶限流（核心逻辑）
```python
tokens = min(capacity, tokens + rate * elapsed_time)
if tokens >= 1: tokens -= 1; return True  # 放行
return False  # 拒绝
```
