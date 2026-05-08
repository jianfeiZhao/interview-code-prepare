# 互联网大厂面试代码题库

> 面向需要备战字节/阿里/腾讯/美团/百度等大厂代码面试的工程师，覆盖算法/数据结构、Python 语言特性、机器学习代码手写、大模型算法、系统设计代码五大方向，共 200+ 道精选题目，每题配有完整 Python 实现与详细解析。

---

## 仓库结构

| 目录 | 说明 |
|------|------|
| `00_quick_review/` | 核心考点速查 Cheatsheet，面试前快速过一遍 |
| `01_algorithms/` | 算法与数据结构题库（200题，13个子分类） |
| `02_python_features/` | Python 语言特性手写题（装饰器/生成器/并发/metaclass等） |
| `03_ml_code/` | 机器学习与深度学习代码手写（经典ML + 深度学习基础） |
| `04_llm_algorithms/` | 大模型算法实现（Attention/位置编码/推理优化/RLHF） |
| `05_system_design_code/` | 系统设计代码题（缓存/限流/分布式/并发） |

---

## 如何使用本仓库

1. **面试前速览**：先看 [`00_quick_review/cheatsheet.md`](00_quick_review/cheatsheet.md) 过一遍核心考点，建立全局认知。
2. **专项突破**：根据面试岗位和时间，选择下方「刷题方法论」中的对应方案，按计划推进。
3. **题目练习**：每个 `.py` 文件直接 `python xxx.py` 即可运行，含内置测试用例，方便验证思路。
4. **弱点复盘**：每天练完后，把卡壳超过10分钟的题目记录下来，第二天优先复习。
5. **模拟面试**：计划最后3天进行完整模拟，每次30分钟内手写2道中等题，重点练习讲解思路。

---

## 刷题方法论

### 短期突击方案

#### 1周冲刺（面试在即，最少必刷）

说明：只有 1 周时间时，放弃「全覆盖」心态，只专注最高频题型。每天 3~4 小时，按下方主题顺序推进，必保中等题流畅写出。

| Day | 主题 | 具体题目 |
|-----|------|---------|
| Day 1 | 数组+字符串+链表基础 | 两数之和、三数之和、最大子数组和、接雨水、最长无重复子串、合并两个有序链表、反转链表 |
| Day 2 | 树基础（高频必考） | 二叉树层序遍历、二叉树最大深度、对称二叉树、路径总和、最低公共祖先、二叉树中序遍历 |
| Day 3 | 图+二分+DP入门 | 岛屿数量、课程表（拓扑排序）、二分查找、搜索旋转排序数组、爬楼梯、零钱兑换、最长公共子序列 |
| Day 4 | 回溯+设计题 | 全排列、子集、N皇后、组合总和、LRU缓存、合并K个升序链表 |
| Day 5 | DP进阶 | 买卖股票最佳时机系列、最长递增子序列、编辑距离、0-1背包、最大正方形 |
| Day 6 | 堆+栈+滑动窗口 | 前K个高频元素、数据流的中位数、字符串解码、有效括号、每日温度 |
| Day 7 | 综合复习+补充 | Python特性速览、系统设计题（LRU/限流）、弱点专项复习（把之前卡壳的题再过一遍） |

---

#### 2周强化（较充裕时间）

说明：2 周时间可覆盖大部分高频题型，第 1 周打基础，第 2 周进阶+查漏。

**第一周（基础）**

| Day | 主题 | 具体题目 |
|-----|------|---------|
| Day 1 | 数组基础 | 两数之和、三数之和、接雨水、盛最多水的容器、最大子数组和、乘积除自身、螺旋矩阵 |
| Day 2 | 数组进阶+字符串 | 旋转图像、跳跃游戏、合并区间、下一个排列、字符串解码、子数组和等于K |
| Day 3 | 链表 | 合并两个有序链表、反转链表、环形链表I/II、删除倒数第N个节点、回文链表、奇偶链表 |
| Day 4 | 链表进阶+设计 | 两数相加、排序链表、LRU缓存、合并K个升序链表、复制带随机指针链表 |
| Day 5 | 树基础 | 二叉树层序遍历、最大深度、对称二叉树、路径总和I/II/III、最低公共祖先、中序遍历、前序遍历 |
| Day 6 | 树进阶 | 验证二叉搜索树、二叉树最大路径和、序列化与反序列化、从中序+前序构造二叉树 |
| Day 7 | 图入门 | 岛屿数量、课程表、省份数量、图的克隆、太平洋大西洋水流 |

**第二周（进阶）**

| Day | 主题 | 具体题目 |
|-----|------|---------|
| Day 8 | DP基础 | 爬楼梯、零钱兑换、最长公共子序列、编辑距离、最长递增子序列、唯一路径 |
| Day 9 | DP进阶 | 买卖股票系列、0-1背包、最大正方形、单词拆分、目标和 |
| Day 10 | 二分+数学贪心 | 搜索旋转排序数组、寻找旋转最小值、两个排序数组的中位数、跳跃游戏、会议室、非重叠区间 |
| Day 11 | 滑动窗口+双指针 | 最长无重复子串、最小覆盖子串、找所有字母异位词、滑动窗口最大值、水果成篓 |
| Day 12 | 栈+堆+回溯 | 每日温度、柱状图最大矩形、前K个高频元素、数据流的中位数、全排列、组合总和 |
| Day 13 | Python特性+系统设计 | 装饰器、生成器、metaclass、asyncio、LRU、令牌桶限流、雪花算法 |
| Day 14 | 综合模拟 | 每类抽1道中等题做完整模拟（限时30分钟），整理易错知识点 |

---

#### 3周全覆盖（充分准备）

说明：3 周时间可系统覆盖全部题型，包括字符串进阶、Trie、图算法高级等，适合有一定基础的求职者。

**第一周：数组/链表/树（同2周方案第一周）**

**第二周：图/DP/二分/贪心（同2周方案第二周 Day8~Day12）**

**第三周：字符串进阶+Trie+设计+综合**

| Day | 主题 | 具体题目 |
|-----|------|---------|
| Day 15 | 字符串进阶 | 最长回文子串、分组字母异位词、KMP算法（实现strstr）、通配符匹配、正则表达式匹配 |
| Day 16 | Trie字典树 | 实现Trie、添加与搜索单词、单词搜索II、单词替换、键值映射 |
| Day 17 | 图高级 | Dijkstra最短路径、最小生成树、单词接龙、找规律行程、网络延迟时间 |
| Day 18 | 回溯进阶+设计题 | N皇后、数独求解、恢复IP地址、设计推特、LFU缓存 |
| Day 19 | ML/LLM算法 | Softmax+交叉熵、手写反向传播、BatchNorm、LayerNorm、Scaled Dot-Product Attention |
| Day 20 | ML/LLM算法续 | Multi-Head Attention、RoPE、KV Cache、Top-k/Top-p采样、PPO/DPO Loss |
| Day 21 | 综合全真模拟 | 每轮45分钟，完整模拟2~3道题；整理弱点清单；高频公司专项 |

---

### 长期准备方案（3个月系统复习）

适合距离面试还有 3 个月以上、希望系统打牢基础的求职者。

#### 第1个月：算法基础夯实

- **周目标**：每周精刷一个大类，追求「理解原理」而不是记忆代码
- 第1周：数组/字符串/双指针/滑动窗口（共35题）
- 第2周：链表/栈/队列/设计题（共32题）
- 第3周：树/图基础（DFS/BFS/拓扑排序）（共38题）
- 第4周：二分查找+数学贪心（共28题）
- **每日节奏**：工作日2题（1Easy+1Medium），周末4题（含1Hard）

#### 第2个月：进阶题型 + 公司专项

- 第5周：动态规划全覆盖（背包/区间DP/状压DP）（29题）
- 第6周：回溯+堆/优先队列+Trie（共26题）
- 第7周：字符串进阶（KMP/正则/通配符）（12题）+ Python特性（10题）
- 第8周：目标公司真题模拟 + 系统设计代码（5题）
- **公司专项**：字节重点练树/DP/字符串；阿里重点练设计/DP；腾讯重点练图/链表；美团重点练贪心/BFS

#### 第3个月：综合模拟 + 查漏补缺

- 第9-10周：ML/LLM算法（20题）+ 每周2次全题型模拟赛（45分钟 × 3题）
- 第11周：针对面试官高频提问方式练习「口述思路 → 手写代码 → 分析复杂度」
- 第12周：清理弱点清单，只复习错过2次以上的题；最后3天只看 cheatsheet 不刷新题

#### 每周刷题节奏建议（工作日/周末如何分配）

```
工作日（周一~周五）：
  早晨 20 分钟：复习昨天卡壳的题，只看思路不写代码
  晚间 60 分钟：精刷 2 道题（1 道中等 + 1 道 Easy/Hard 视心情）

周末（周六+周日）：
  上午 2 小时：专题集中突破（一口气刷完一个子分类）
  下午 1 小时：模拟面试（找同伴互出题，或自己计时）
  晚间 30 分钟：整理本周错题本，写下每题的关键思路一句话
```

---

### 各类岗位的侧重建议

#### 后端工程师
- **必刷**：全部算法题（重点：数组/链表/树/DP）+ 系统设计代码（5题）+ Python特性
- **高频出现**：LRU缓存、接雨水、合并K个链表、二叉树系列、字符串解码、岛屿数量
- **加分项**：图算法（Dijkstra/拓扑排序）、并发相关Python题（GIL/asyncio）
- **可跳过**：ML/LLM算法（除非岗位有明确要求）

#### 算法工程师（ML/AI方向）
- **必刷**：算法题（中等难度以上）+ 全部ML代码手写（10题）+ Python特性
- **高频出现**：KNN、KMeans、反向传播、BatchNorm、Softmax、排序/堆相关
- **加分项**：DP、图算法、LLM算法（Attention/LayerNorm/Adam）
- **特别注意**：能清晰口述推导过程，比只会写代码更重要

#### 大模型/LLM工程师
- **必刷**：全部LLM算法（10题）+ ML基础（5题）+ 算法题（数组/链表/树基础）
- **高频出现**：Multi-Head Attention、RoPE、KV Cache、Top-k/Top-p采样、PPO/DPO Loss
- **加分项**：GQA、Speculative Decoding、Flash Attention原理
- **特别注意**：要能手写完整的 Attention 前向传播并说清 shape 变化

#### 应届生 vs 社招
- **应届生**：基础算法题（Easy/Medium）打牢，重点准备字节/腾讯/美团常见题型；Python特性选3-5道代表性题目，不必全部手写
- **社招（3年以上）**：算法题应对中等偏难，更关注设计题和系统设计；必须能清晰分析时间/空间复杂度；面试官更看重解题思路而非死记题目

---

### 高频考点速查

| 公司 | 最高频题型 | 代表题目 |
|------|-----------|---------|
| 字节跳动 | 动态规划、字符串、数组、树 | 接雨水、最大子数组和、二叉树系列、字符串解码、LRU缓存 |
| 阿里巴巴 | 设计题、DP、图、树 | LRU/LFU、课程表、岛屿数量、最长公共子序列、序列化树 |
| 腾讯 | 链表、树、DP | 合并K个链表、LRU、二叉树最大路径、反转链表、全排列 |
| 美团 | 贪心、BFS/DFS、数组 | 岛屿数量、跳跃游戏、会议室、前K高频元素、两数之和 |
| 百度 | 字符串、DP、树 | 最长回文子串、编辑距离、验证BST、零钱兑换、单词拆分 |

---

## 题目总览

### 01 算法/数据结构（200题）

---

#### 数组与字符串（24题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [两数之和](01_algorithms/array_string/two_sum.py) | Easy | LC 1 | 字节/阿里/腾讯/全系 |
| 2 | [三数之和](01_algorithms/array_string/three_sum.py) | Medium | LC 15 | 字节/阿里/腾讯 |
| 3 | [接雨水](01_algorithms/array_string/trapping_rain_water.py) | Hard | LC 42 | 字节/阿里/腾讯 |
| 4 | [盛最多水的容器](01_algorithms/array_string/container_with_most_water.py) | Medium | LC 11 | 字节/美团 |
| 5 | [最大子数组和](01_algorithms/array_string/maximum_subarray.py) | Medium | LC 53 | 字节/阿里/全系 |
| 6 | [除自身以外数组的乘积](01_algorithms/array_string/product_except_self.py) | Medium | LC 238 | 字节/腾讯 |
| 7 | [螺旋矩阵](01_algorithms/array_string/spiral_matrix.py) | Medium | LC 54 | 字节/阿里 |
| 8 | [旋转图像](01_algorithms/array_string/rotate_image.py) | Medium | LC 48 | 字节/腾讯 |
| 9 | [矩阵置零](01_algorithms/array_string/set_matrix_zeroes.py) | Medium | LC 73 | 字节/美团 |
| 10 | [搜索插入位置](01_algorithms/array_string/search_insert_position.py) | Easy | LC 35 | 全系大厂 |
| 11 | [删除有序数组中的重复项](01_algorithms/array_string/remove_duplicates.py) | Easy | LC 26 | 字节/腾讯 |
| 12 | [移动零](01_algorithms/array_string/move_zeroes.py) | Easy | LC 283 | 字节/美团 |
| 13 | [有序数组的平方](01_algorithms/array_string/squares_of_sorted_array.py) | Easy | LC 977 | 字节/阿里 |
| 14 | [和为K的子数组](01_algorithms/array_string/subarray_sum_equals_k.py) | Medium | LC 560 | 字节/腾讯/美团 |
| 15 | [下一个排列](01_algorithms/array_string/next_permutation.py) | Medium | LC 31 | 字节/阿里 |
| 16 | [加一](01_algorithms/array_string/plus_one.py) | Easy | LC 66 | 阿里/腾讯 |
| 17 | [旋转数组](01_algorithms/array_string/rotate_array.py) | Medium | LC 189 | 字节/腾讯 |
| 18 | [数组中重复的数字](01_algorithms/array_string/find_all_duplicates.py) | Medium | LC 442 | 字节/美团 |
| 19 | [寻找重复数](01_algorithms/array_string/find_duplicate.py) | Medium | LC 287 | 字节/阿里 |
| 20 | [乘积最大子数组](01_algorithms/array_string/maximum_product_subarray.py) | Medium | LC 152 | 字节/腾讯 |
| 21 | [字符串解码](01_algorithms/array_string/decode_string.py) | Medium | LC 394 | 字节/阿里 |
| 22 | [合并区间](01_algorithms/array_string/merge_intervals.py) | Medium | LC 56 | 字节/美团/阿里 |
| 23 | [跳跃游戏](01_algorithms/array_string/jump_game.py) | Medium | LC 55 | 字节/美团 |
| 24 | [最小栈](01_algorithms/array_string/min_stack.py) | Easy | LC 155 | 全系大厂 |

#### 链表（18题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [合并两个有序链表](01_algorithms/linked_list/merge_two_sorted_lists.py) | Easy | LC 21 | 字节/腾讯/全系 |
| 2 | [反转链表](01_algorithms/linked_list/reverse_linked_list.py) | Easy | LC 206 | 全系大厂 |
| 3 | [环形链表](01_algorithms/linked_list/linked_list_cycle.py) | Easy | LC 141 | 字节/阿里/腾讯 |
| 4 | [两数相加](01_algorithms/linked_list/add_two_numbers.py) | Medium | LC 2 | 字节/腾讯 |
| 5 | [删除链表的倒数第N个节点](01_algorithms/linked_list/remove_nth_from_end.py) | Medium | LC 19 | 字节/阿里 |
| 6 | [合并K个升序链表](01_algorithms/linked_list/merge_k_sorted_lists.py) | Hard | LC 23 | 字节/腾讯/阿里 |
| 7 | [排序链表](01_algorithms/linked_list/sort_list.py) | Medium | LC 148 | 字节/美团 |
| 8 | [LRU缓存](01_algorithms/linked_list/lru_cache.py) | Medium | LC 146 | 字节/腾讯/阿里 |
| 9 | [重排链表](01_algorithms/linked_list/reorder_list.py) | Medium | LC 143 | 字节/腾讯 |
| 10 | [回文链表](01_algorithms/linked_list/palindrome_linked_list.py) | Easy | LC 234 | 字节/美团 |
| 11 | [复制带随机指针的链表](01_algorithms/linked_list/copy_list_with_random.py) | Medium | LC 138 | 字节/阿里 |
| 12 | [相交链表](01_algorithms/linked_list/intersection_of_linked_lists.py) | Easy | LC 160 | 腾讯/美团 |
| 13 | [环形链表II](01_algorithms/linked_list/linked_list_cycle_ii.py) | Medium | LC 142 | 字节/阿里 |
| 14 | [奇偶链表](01_algorithms/linked_list/odd_even_linked_list.py) | Medium | LC 328 | 字节/腾讯 |
| 15 | [分隔链表](01_algorithms/linked_list/partition_list.py) | Medium | LC 86 | 阿里/美团 |
| 16 | [旋转链表](01_algorithms/linked_list/rotate_list.py) | Medium | LC 61 | 字节/阿里 |
| 17 | [两两交换链表节点](01_algorithms/linked_list/swap_nodes_in_pairs.py) | Medium | LC 24 | 字节/腾讯 |
| 18 | [两两交换（变体）](01_algorithms/linked_list/swap_pairs.py) | Medium | LC 24 | 腾讯/美团 |

#### 树与图（38题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [二叉树中序遍历](01_algorithms/tree_graph/binary_tree_inorder.py) | Easy | LC 94 | 全系大厂 |
| 2 | [二叉树前序遍历](01_algorithms/tree_graph/binary_tree_preorder.py) | Easy | LC 144 | 全系大厂 |
| 3 | [二叉树层序遍历](01_algorithms/tree_graph/binary_tree_level_order.py) | Medium | LC 102 | 字节/阿里 |
| 4 | [二叉树最大深度](01_algorithms/tree_graph/max_depth_binary_tree.py) | Easy | LC 104 | 字节/腾讯 |
| 5 | [对称二叉树](01_algorithms/tree_graph/symmetric_tree.py) | Easy | LC 101 | 字节/阿里 |
| 6 | [路径总和](01_algorithms/tree_graph/path_sum.py) | Easy | LC 112 | 字节/腾讯 |
| 7 | [路径总和III](01_algorithms/tree_graph/path_sum_iii.py) | Medium | LC 437 | 字节/阿里 |
| 8 | [最低公共祖先](01_algorithms/tree_graph/lowest_common_ancestor.py) | Medium | LC 236 | 字节/腾讯/阿里 |
| 9 | [验证二叉搜索树](01_algorithms/tree_graph/validate_bst.py) | Medium | LC 98 | 字节/阿里 |
| 10 | [二叉树最大路径和](01_algorithms/tree_graph/binary_tree_max_path.py) | Hard | LC 124 | 字节/腾讯 |
| 11 | [二叉树右视图](01_algorithms/tree_graph/binary_tree_right_side.py) | Medium | LC 199 | 字节/美团 |
| 12 | [序列化与反序列化二叉树](01_algorithms/tree_graph/serialize_deserialize.py) | Hard | LC 297 | 字节/阿里 |
| 13 | [从中序与前序遍历构造二叉树](01_algorithms/tree_graph/construct_binary_tree.py) | Medium | LC 105 | 字节/腾讯 |
| 14 | [将有序数组转换为BST](01_algorithms/tree_graph/convert_sorted_array_bst.py) | Easy | LC 108 | 阿里/美团 |
| 15 | [展平二叉树到链表](01_algorithms/tree_graph/flatten_binary_tree.py) | Medium | LC 114 | 字节/腾讯 |
| 16 | [BST中第K小的元素](01_algorithms/tree_graph/kth_smallest_bst.py) | Medium | LC 230 | 字节/阿里 |
| 17 | [平衡二叉树](01_algorithms/tree_graph/balanced_binary_tree.py) | Easy | LC 110 | 腾讯/美团 |
| 18 | [二叉树直径](01_algorithms/tree_graph/diameter_of_binary_tree.py) | Easy | LC 543 | 字节/美团 |
| 19 | [填充每个节点的下一个右侧节点](01_algorithms/tree_graph/populating_next_right.py) | Medium | LC 116 | 腾讯/阿里 |
| 20 | [完全二叉树的节点个数](01_algorithms/tree_graph/count_complete_tree_nodes.py) | Medium | LC 222 | 字节/阿里 |
| 21 | [岛屿数量](01_algorithms/tree_graph/number_of_islands.py) | Medium | LC 200 | 字节/美团/全系 |
| 22 | [课程表（拓扑排序）](01_algorithms/tree_graph/course_schedule.py) | Medium | LC 207 | 字节/阿里 |
| 23 | [省份数量](01_algorithms/tree_graph/number_of_provinces.py) | Medium | LC 547 | 字节/腾讯 |
| 24 | [克隆图](01_algorithms/tree_graph/clone_graph.py) | Medium | LC 133 | 字节/阿里 |
| 25 | [太平洋大西洋水流](01_algorithms/tree_graph/pacific_atlantic.py) | Medium | LC 417 | 字节/美团 |
| 26 | [被围绕的区域](01_algorithms/tree_graph/surrounded_regions.py) | Medium | LC 130 | 腾讯/阿里 |
| 27 | [腐烂的橘子](01_algorithms/tree_graph/rotting_oranges.py) | Medium | LC 994 | 字节/美团 |
| 28 | [网络延迟时间（Dijkstra）](01_algorithms/tree_graph/network_delay_time.py) | Medium | LC 743 | 字节/阿里 |
| 29 | [最小生成树（Kruskal/Prim）](01_algorithms/tree_graph/minimum_spanning_tree.py) | Medium | LC 1584 | 字节/阿里 |
| 30 | [拓扑排序（通用）](01_algorithms/tree_graph/topological_sort.py) | Medium | LC - | 字节/阿里 |
| 31 | [并查集（Union-Find）](01_algorithms/tree_graph/union_find.py) | Medium | LC - | 字节/阿里/腾讯 |
| 32 | [单词接龙](01_algorithms/tree_graph/word_ladder.py) | Hard | LC 127 | 字节/百度 |
| 33 | [寻找规律行程](01_algorithms/tree_graph/find_itinerary.py) | Hard | LC 332 | 字节/阿里 |
| 34 | [距离所有人最远的房子](01_algorithms/tree_graph/as_far_from_land.py) | Medium | LC 1162 | 美团 |
| 35 | [所有距离为K的节点](01_algorithms/tree_graph/all_nodes_distance_k.py) | Medium | LC 863 | 字节/腾讯 |
| 36 | [能看到几个人（单调栈）](01_algorithms/tree_graph/number_of_visible_people.py) | Hard | LC 1944 | 字节 |
| 37 | [Dijkstra最短路径](01_algorithms/tree_graph/dijkstra.py) | Medium | LC - | 字节/阿里 |
| 38 | [飞地数量](01_algorithms/tree_graph/number_of_enclaves.py) | Medium | LC 1020 | 美团/字节 |

#### 动态规划（29题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [爬楼梯](01_algorithms/dynamic_programming/climbing_stairs.py) | Easy | LC 70 | 全系大厂 |
| 2 | [零钱兑换](01_algorithms/dynamic_programming/coin_change.py) | Medium | LC 322 | 字节/阿里/美团 |
| 3 | [最长公共子序列](01_algorithms/dynamic_programming/longest_common_subsequence.py) | Medium | LC 1143 | 字节/腾讯 |
| 4 | [编辑距离](01_algorithms/dynamic_programming/edit_distance.py) | Hard | LC 72 | 字节/阿里/百度 |
| 5 | [最长递增子序列](01_algorithms/dynamic_programming/longest_increasing_subsequence.py) | Medium | LC 300 | 字节/腾讯 |
| 6 | [唯一路径](01_algorithms/dynamic_programming/unique_paths.py) | Medium | LC 62 | 字节/美团 |
| 7 | [最小路径和](01_algorithms/dynamic_programming/minimum_path_sum.py) | Medium | LC 64 | 腾讯/阿里 |
| 8 | [打家劫舍](01_algorithms/dynamic_programming/house_robber.py) | Medium | LC 198 | 字节/腾讯 |
| 9 | [买卖股票最佳时机（通用）](01_algorithms/dynamic_programming/stock_problems.py) | Medium | LC 188 | 字节/阿里 |
| 10 | [买卖股票最佳时机（贪心）](01_algorithms/dynamic_programming/best_time_to_buy.py) | Easy | LC 121 | 全系大厂 |
| 11 | [0-1背包问题](01_algorithms/dynamic_programming/knapsack_01.py) | Medium | LC - | 字节/阿里/腾讯 |
| 12 | [分割等和子集](01_algorithms/dynamic_programming/partition_equal_subset.py) | Medium | LC 416 | 字节/阿里 |
| 13 | [目标和](01_algorithms/dynamic_programming/target_sum.py) | Medium | LC 494 | 字节/腾讯 |
| 14 | [单词拆分](01_algorithms/dynamic_programming/word_break.py) | Medium | LC 139 | 字节/百度 |
| 15 | [最大正方形](01_algorithms/dynamic_programming/maximal_square.py) | Medium | LC 221 | 字节/阿里 |
| 16 | [最大矩形](01_algorithms/dynamic_programming/maximal_rectangle.py) | Hard | LC 85 | 字节/阿里 |
| 17 | [戳气球](01_algorithms/dynamic_programming/burst_balloons.py) | Hard | LC 312 | 字节 |
| 18 | [完全平方数](01_algorithms/dynamic_programming/perfect_squares.py) | Medium | LC 279 | 字节/美团 |
| 19 | [解码方法](01_algorithms/dynamic_programming/decode_ways.py) | Medium | LC 91 | 字节/腾讯 |
| 20 | [三角形最小路径和](01_algorithms/dynamic_programming/triangle.py) | Medium | LC 120 | 阿里/腾讯 |
| 21 | [整数拆分](01_algorithms/dynamic_programming/integer_break.py) | Medium | LC 343 | 字节/美团 |
| 22 | [比特位计数](01_algorithms/dynamic_programming/counting_bits.py) | Easy | LC 338 | 美团/腾讯 |
| 23 | [等差数列划分](01_algorithms/dynamic_programming/arithmetic_slices.py) | Medium | LC 413 | 字节 |
| 24 | [回文子串](01_algorithms/dynamic_programming/palindromic_substrings.py) | Medium | LC 647 | 字节/百度 |
| 25 | [石子游戏](01_algorithms/dynamic_programming/stone_game.py) | Medium | LC 877 | 字节/腾讯 |
| 26 | [最长湍流子数组](01_algorithms/dynamic_programming/longest_turbulent_subarray.py) | Medium | LC 978 | 字节 |
| 27 | [正则表达式匹配](01_algorithms/dynamic_programming/regular_expression.py) | Hard | LC 10 | 字节/百度 |
| 28 | [直线上最多的点](01_algorithms/dynamic_programming/max_points_on_line.py) | Hard | LC 149 | 字节/阿里 |
| 29 | [跳跃游戏（DP版）](01_algorithms/dynamic_programming/jump_game.py) | Medium | LC 55 | 字节/美团 |

#### 二分查找（14题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [二分查找](01_algorithms/binary_search/binary_search.py) | Easy | LC 704 | 全系大厂 |
| 2 | [搜索旋转排序数组](01_algorithms/binary_search/search_in_rotated_array.py) | Medium | LC 33 | 字节/阿里 |
| 3 | [搜索旋转排序数组（变体）](01_algorithms/binary_search/search_rotated_array.py) | Medium | LC 81 | 字节/腾讯 |
| 4 | [寻找旋转排序数组最小值](01_algorithms/binary_search/find_minimum_in_rotated_array.py) | Medium | LC 153 | 字节/美团 |
| 5 | [在排序数组中查找元素的第一个和最后一个位置](01_algorithms/binary_search/find_first_last_position.py) | Medium | LC 34 | 字节/阿里 |
| 6 | [寻找峰值](01_algorithms/binary_search/find_peak_element.py) | Medium | LC 162 | 字节/腾讯 |
| 7 | [x的平方根](01_algorithms/binary_search/sqrt_x.py) | Easy | LC 69 | 腾讯/美团 |
| 8 | [两个正序数组的中位数](01_algorithms/binary_search/median_two_sorted_arrays.py) | Hard | LC 4 | 字节/阿里 |
| 9 | [搜索二维矩阵](01_algorithms/binary_search/search_2d_matrix.py) | Medium | LC 74 | 字节/腾讯 |
| 10 | [珂珂吃香蕉](01_algorithms/binary_search/koko_eating_bananas.py) | Medium | LC 875 | 字节/阿里 |
| 11 | [运输船载重](01_algorithms/binary_search/capacity_to_ship.py) | Medium | LC 1011 | 字节/美团 |
| 12 | [分割数组的最大值](01_algorithms/binary_search/split_array_largest_sum.py) | Hard | LC 410 | 字节/阿里 |
| 13 | [BST中第K小的元素（二分）](01_algorithms/binary_search/kth_smallest_in_bst.py) | Medium | LC 230 | 字节 |
| 14 | [找到右边区间](01_algorithms/binary_search/find_right_interval.py) | Medium | LC 436 | 腾讯/阿里 |

#### 数学与贪心（14题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [计数质数](01_algorithms/math_greedy/count_primes.py) | Medium | LC 204 | 字节/百度 |
| 2 | [多数元素](01_algorithms/math_greedy/majority_element.py) | Easy | LC 169 | 字节/阿里 |
| 3 | [缺失数字](01_algorithms/math_greedy/missing_number.py) | Easy | LC 268 | 字节/美团 |
| 4 | [只出现一次的数字](01_algorithms/math_greedy/single_number.py) | Easy | LC 136 | 全系大厂 |
| 5 | [快乐数](01_algorithms/math_greedy/happy_number.py) | Easy | LC 202 | 腾讯/美团 |
| 6 | [2的幂](01_algorithms/math_greedy/power_of_two.py) | Easy | LC 231 | 腾讯/阿里 |
| 7 | [Pow(x, n)](01_algorithms/math_greedy/power_function.py) | Medium | LC 50 | 字节/阿里 |
| 8 | [整数反转](01_algorithms/math_greedy/reverse_integer.py) | Medium | LC 7 | 字节/腾讯 |
| 9 | [加油站](01_algorithms/math_greedy/gas_station.py) | Medium | LC 134 | 字节/美团 |
| 10 | [分发糖果](01_algorithms/math_greedy/candy.py) | Hard | LC 135 | 字节/阿里 |
| 11 | [合并区间（贪心版）](01_algorithms/math_greedy/interval_merge.py) | Medium | LC 56 | 字节/美团 |
| 12 | [会议室](01_algorithms/math_greedy/meeting_rooms.py) | Medium | LC 252 | 字节/美团 |
| 13 | [用最少数量的箭引爆气球](01_algorithms/math_greedy/minimum_number_of_arrows.py) | Medium | LC 452 | 字节/腾讯 |
| 14 | [无重叠区间](01_algorithms/math_greedy/non_overlapping_intervals.py) | Medium | LC 435 | 字节/阿里 |

#### 字符串进阶（12题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [最长回文子串](01_algorithms/string_advanced/longest_palindromic_substring.py) | Medium | LC 5 | 字节/百度/腾讯 |
| 2 | [字母异位词分组](01_algorithms/string_advanced/group_anagrams.py) | Medium | LC 49 | 字节/阿里 |
| 3 | [实现strstr（KMP）](01_algorithms/string_advanced/implement_strstr_kmp.py) | Easy | LC 28 | 字节/百度 |
| 4 | [实现strstr（暴力）](01_algorithms/string_advanced/implement_strstr.py) | Easy | LC 28 | 字节/腾讯 |
| 5 | [最长公共前缀](01_algorithms/string_advanced/longest_common_prefix.py) | Easy | LC 14 | 腾讯/美团 |
| 6 | [反转字符串中的单词](01_algorithms/string_advanced/reverse_words_in_string.py) | Medium | LC 151 | 字节/腾讯 |
| 7 | [罗马数字转整数](01_algorithms/string_advanced/roman_to_integer.py) | Easy | LC 13 | 阿里/美团 |
| 8 | [有效的字母异位词](01_algorithms/string_advanced/valid_anagram.py) | Easy | LC 242 | 字节/腾讯 |
| 9 | [有效的括号](01_algorithms/string_advanced/valid_parentheses.py) | Easy | LC 20 | 全系大厂 |
| 10 | [通配符匹配](01_algorithms/string_advanced/wildcard_matching.py) | Hard | LC 44 | 字节/百度 |
| 11 | [字符串编解码](01_algorithms/string_advanced/encode_decode_strings.py) | Medium | LC 271 | 字节/阿里 |
| 12 | [Z字形变换](01_algorithms/string_advanced/zigzag_conversion.py) | Medium | LC 6 | 腾讯/美团 |

#### 滑动窗口（11题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [最长无重复子串](01_algorithms/sliding_window/longest_substring_no_repeat.py) | Medium | LC 3 | 字节/美团/全系 |
| 2 | [最小覆盖子串](01_algorithms/sliding_window/minimum_window_substring.py) | Hard | LC 76 | 字节/阿里 |
| 3 | [找到字符串中所有字母异位词](01_algorithms/sliding_window/find_all_anagrams.py) | Medium | LC 438 | 字节/腾讯 |
| 4 | [字符串的排列](01_algorithms/sliding_window/permutation_in_string.py) | Medium | LC 567 | 字节/美团 |
| 5 | [滑动窗口最大值](01_algorithms/sliding_window/sliding_window_maximum.py) | Hard | LC 239 | 字节/阿里 |
| 6 | [水果成篓](01_algorithms/sliding_window/fruit_into_baskets.py) | Medium | LC 904 | 字节/美团 |
| 7 | [替换后的最长重复字符](01_algorithms/sliding_window/longest_repeating_char_replace.py) | Medium | LC 424 | 字节/腾讯 |
| 8 | [最大连续1的个数III](01_algorithms/sliding_window/max_consecutive_ones.py) | Medium | LC 1004 | 美团/阿里 |
| 9 | [K个不同整数的子数组](01_algorithms/sliding_window/subarrays_k_different.py) | Hard | LC 992 | 字节 |
| 10 | [K个元音字符串子串](01_algorithms/sliding_window/count_vowel_substrings.py) | Medium | LC 1456 | 腾讯 |
| 11 | [元素和小于等于阈值](01_algorithms/sliding_window/count_subarrays_with_k.py) | Medium | LC 1343 | 美团 |

#### 栈与队列（11题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [每日温度](01_algorithms/stack_queue/daily_temperatures.py) | Medium | LC 739 | 字节/美团 |
| 2 | [下一个更大元素I](01_algorithms/stack_queue/next_greater_element.py) | Easy | LC 496 | 字节/腾讯 |
| 3 | [柱状图中最大矩形](01_algorithms/stack_queue/largest_rectangle_histogram.py) | Hard | LC 84 | 字节/阿里 |
| 4 | [矩阵中最大矩形（栈版）](01_algorithms/stack_queue/maximal_rectangle.py) | Hard | LC 85 | 字节/阿里 |
| 5 | [基本计算器](01_algorithms/stack_queue/basic_calculator.py) | Hard | LC 224 | 字节/百度 |
| 6 | [逆波兰表达式求值](01_algorithms/stack_queue/evaluate_reverse_polish.py) | Medium | LC 150 | 字节/腾讯 |
| 7 | [用栈实现队列](01_algorithms/stack_queue/implement_queue_using_stacks.py) | Easy | LC 232 | 全系大厂 |
| 8 | [用队列实现栈](01_algorithms/stack_queue/implement_stack_using_queues.py) | Easy | LC 225 | 全系大厂 |
| 9 | [行星碰撞](01_algorithms/stack_queue/asteroid_collision.py) | Medium | LC 735 | 字节/腾讯 |
| 10 | [简化路径](01_algorithms/stack_queue/simplify_path.py) | Medium | LC 71 | 腾讯/阿里 |
| 11 | [最小栈（栈队列版）](01_algorithms/stack_queue/min_stack.py) | Easy | LC 155 | 全系大厂 |

#### 回溯（11题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [全排列](01_algorithms/backtracking/permutations.py) | Medium | LC 46 | 字节/腾讯/阿里 |
| 2 | [子集](01_algorithms/backtracking/subsets.py) | Medium | LC 78 | 字节/阿里 |
| 3 | [N皇后](01_algorithms/backtracking/n_queens.py) | Hard | LC 51 | 字节/百度 |
| 4 | [组合总和](01_algorithms/backtracking/combination_sum.py) | Medium | LC 39 | 字节/腾讯 |
| 5 | [组合总和III](01_algorithms/backtracking/combination_sum_iii.py) | Medium | LC 216 | 字节/阿里 |
| 6 | [括号生成](01_algorithms/backtracking/generate_parentheses.py) | Medium | LC 22 | 字节/腾讯/全系 |
| 7 | [电话号码的字母组合](01_algorithms/backtracking/letter_combinations.py) | Medium | LC 17 | 字节/美团 |
| 8 | [回文串分割](01_algorithms/backtracking/palindrome_partition.py) | Medium | LC 131 | 字节/阿里 |
| 9 | [复原IP地址](01_algorithms/backtracking/restore_ip_addresses.py) | Medium | LC 93 | 字节/腾讯 |
| 10 | [数独求解器](01_algorithms/backtracking/sudoku_solver.py) | Hard | LC 37 | 字节/百度 |
| 11 | [单词搜索](01_algorithms/backtracking/word_search.py) | Medium | LC 79 | 字节/腾讯 |

#### 堆/优先队列（8题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [前K个高频元素](01_algorithms/heap_priority_queue/top_k_frequent.py) | Medium | LC 347 | 字节/美团 |
| 2 | [数据流的中位数](01_algorithms/heap_priority_queue/find_median_data_stream.py) | Hard | LC 295 | 字节/腾讯 |
| 3 | [第K个最大元素](01_algorithms/heap_priority_queue/find_kth_largest.py) | Medium | LC 215 | 字节/阿里 |
| 4 | [合并K个升序链表（堆版）](01_algorithms/heap_priority_queue/merge_k_sorted_lists.py) | Hard | LC 23 | 字节/腾讯/阿里 |
| 5 | [重构字符串](01_algorithms/heap_priority_queue/reorganize_string.py) | Medium | LC 767 | 字节/美团 |
| 6 | [任务调度器](01_algorithms/heap_priority_queue/task_scheduler.py) | Medium | LC 621 | 字节/腾讯 |
| 7 | [IPO（最大化资本）](01_algorithms/heap_priority_queue/ipo.py) | Hard | LC 502 | 字节/阿里 |
| 8 | [丑数](01_algorithms/heap_priority_queue/ugly_number.py) | Medium | LC 264 | 腾讯/百度 |

#### 字典树 Trie（7题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [实现Trie（前缀树）](01_algorithms/trie/trie_implement.py) | Medium | LC 208 | 字节/阿里 |
| 2 | [添加与搜索单词](01_algorithms/trie/design_add_search_words.py) | Medium | LC 211 | 字节/腾讯 |
| 3 | [单词搜索II](01_algorithms/trie/word_search_ii.py) | Hard | LC 212 | 字节/阿里 |
| 4 | [单词替换](01_algorithms/trie/replace_words.py) | Medium | LC 648 | 腾讯/百度 |
| 5 | [最长公共前缀（Trie）](01_algorithms/trie/longest_common_prefix.py) | Easy | LC 14 | 腾讯/美团 |
| 6 | [键值映射](01_algorithms/trie/map_sum_pairs.py) | Medium | LC 677 | 字节/阿里 |
| 7 | [统计前缀相同的单词数](01_algorithms/trie/count_words_with_prefix.py) | Easy | LC 2185 | 腾讯/美团 |

#### 设计题（3题）

| # | 题目 | 难度 | LeetCode | 高频公司 |
|---|------|------|----------|---------|
| 1 | [设计推特](01_algorithms/design/design_twitter.py) | Medium | LC 355 | 字节/腾讯 |
| 2 | [LFU缓存](01_algorithms/design/lfu_cache.py) | Hard | LC 460 | 字节/阿里 |
| 3 | [基于时间的键值存储](01_algorithms/design/time_based_key_value.py) | Medium | LC 981 | 字节/阿里 |

---

### 02 Python 语言特性（10题）

| # | 题目 | 难度 | 标签 | 高频公司 |
|---|------|------|------|---------|
| 1 | [实现一个带参数的装饰器](02_python_features/decorator/decorator_with_args.py) | Medium | 装饰器 | 字节/阿里 |
| 2 | [实现 retry 装饰器](02_python_features/decorator/retry_decorator.py) | Medium | 装饰器 | 字节/腾讯 |
| 3 | [手写生成器和 yield](02_python_features/generator_iterator/generator_basics.py) | Medium | 生成器 | 字节/美团 |
| 4 | [实现自定义迭代器](02_python_features/generator_iterator/custom_iterator.py) | Medium | 迭代器 | 阿里/腾讯 |
| 5 | [实现单例模式（metaclass）](02_python_features/metaclass/singleton_metaclass.py) | Hard | metaclass | 字节/阿里 |
| 6 | [contextmanager 上下文管理器](02_python_features/decorator/context_manager.py) | Medium | 上下文管理 | 字节/腾讯 |
| 7 | [__slots__ 内存优化](02_python_features/metaclass/slots_usage.py) | Medium | 内存/属性 | 阿里/美团 |
| 8 | [GIL 与多线程](02_python_features/concurrency/gil_threading.py) | Hard | 并发/GIL | 字节/阿里 |
| 9 | [asyncio 协程基础](02_python_features/concurrency/asyncio_basics.py) | Hard | 异步 | 字节/腾讯 |
| 10 | [描述符协议](02_python_features/metaclass/descriptor_protocol.py) | Hard | 描述符 | 阿里/字节 |

---

### 03 机器学习/AI 代码手写（10题）

| # | 题目 | 难度 | 标签 | 高频公司 |
|---|------|------|------|---------|
| 1 | [K 近邻分类器（KNN）](03_ml_code/classical_ml/knn.py) | Medium | 经典ML | 字节/阿里 |
| 2 | [K-Means 聚类](03_ml_code/classical_ml/kmeans.py) | Medium | 经典ML | 字节/美团 |
| 3 | [决策树（信息增益）](03_ml_code/classical_ml/decision_tree.py) | Hard | 经典ML | 阿里/百度 |
| 4 | [Softmax + 交叉熵](03_ml_code/deep_learning/softmax_crossentropy.py) | Medium | 深度学习基础 | 全系大厂 |
| 5 | [手写反向传播（标量）](03_ml_code/deep_learning/backprop_scalar.py) | Hard | 深度学习 | 字节/阿里 |
| 6 | [手写反向传播（矩阵）](03_ml_code/deep_learning/backprop_matrix.py) | Hard | 深度学习 | 字节/阿里 |
| 7 | [BatchNorm 前向+反向](03_ml_code/deep_learning/batch_norm.py) | Hard | 深度学习 | 字节/阿里/腾讯 |
| 8 | [LayerNorm 实现](03_ml_code/deep_learning/layer_norm.py) | Hard | 深度学习 | 字节/阿里 |
| 9 | [Dropout 实现](03_ml_code/deep_learning/dropout.py) | Medium | 深度学习 | 全系大厂 |
| 10 | [Adam 优化器](03_ml_code/deep_learning/adam_optimizer.py) | Hard | 优化器 | 字节/阿里 |

---

### 04 大模型算法（10题）

| # | 题目 | 难度 | 标签 | 高频公司 |
|---|------|------|------|---------|
| 1 | [Scaled Dot-Product Attention](04_llm_algorithms/attention_variants/scaled_dot_product_attention.py) | Hard | Attention | 字节/阿里/全系 |
| 2 | [Multi-Head Attention](04_llm_algorithms/attention_variants/multi_head_attention.py) | Hard | Attention | 字节/阿里/腾讯 |
| 3 | [Group Query Attention (GQA)](04_llm_algorithms/attention_variants/grouped_query_attention.py) | Hard | Attention | 字节/阿里 |
| 4 | [RoPE 旋转位置编码](04_llm_algorithms/positional_encoding/rope.py) | Hard | 位置编码 | 字节/阿里/全系 |
| 5 | [ALiBi 位置编码](04_llm_algorithms/positional_encoding/alibi.py) | Hard | 位置编码 | 字节/阿里 |
| 6 | [KV Cache 原理实现](04_llm_algorithms/inference_optimization/kv_cache.py) | Hard | 推理优化 | 字节/阿里/全系 |
| 7 | [Top-k / Top-p 采样](04_llm_algorithms/inference_optimization/sampling.py) | Medium | 解码策略 | 字节/阿里/腾讯 |
| 8 | [Speculative Decoding（推测解码）](04_llm_algorithms/inference_optimization/speculative_decoding.py) | Hard | 推理优化 | 字节/阿里 |
| 9 | [PPO Clip Loss](04_llm_algorithms/rlhf/ppo_clip_loss.py) | Hard | RLHF | 字节/阿里/全系 |
| 10 | [DPO Loss](04_llm_algorithms/rlhf/dpo_loss.py) | Hard | RLHF | 字节/阿里/全系 |

---

### 05 系统设计代码（5题）

| # | 题目 | 难度 | 标签 | 高频公司 |
|---|------|------|------|---------|
| 1 | [LRU Cache](05_system_design_code/lru_cache.py) | Medium | 缓存 | 字节/腾讯/阿里 |
| 2 | [令牌桶限流器](05_system_design_code/token_bucket.py) | Medium | 限流 | 字节/美团 |
| 3 | [滑动窗口限流器](05_system_design_code/sliding_window_rate_limiter.py) | Medium | 限流 | 字节/阿里 |
| 4 | [雪花算法 ID 生成器](05_system_design_code/snowflake_id.py) | Hard | 分布式 | 字节/阿里 |
| 5 | [线程安全消息队列](05_system_design_code/thread_safe_queue.py) | Medium | 并发 | 字节/腾讯 |

---

## 贡献与反馈

如有题目错误、更好的解法或希望补充新题，欢迎提 Issue 或 PR。每道题的 `.py` 文件顶部均有解题思路说明，运行即可验证。

> 祝面试顺利！
