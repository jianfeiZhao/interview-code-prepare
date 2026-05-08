"""
LeetCode #127 - Word Ladder
难度: Hard
高频公司: 字节跳动 / 阿里巴巴

题目描述:
字典 wordList 中从单词 beginWord 到 endWord 的转换序列是一个按下述规格形成的序列：
    - 序列中第一个单词是 beginWord
    - 序列中最后一个单词是 endWord
    - 每次转换只能改变一个字母
    - 转换过程中的中间单词必须是字典 wordList 中的单词
给你两个单词 beginWord 和 endWord 和一个字典 wordList，找到从 beginWord 到 endWord 的
最短转换序列中的单词数目。如果不存在则返回 0。

示例:
    输入: beginWord = "hit", endWord = "cog",
         wordList = ["hot","dot","dog","lot","log","cog"]
    输出: 5
    解释: "hit" -> "hot" -> "dot" -> "dog" -> "cog"，长度为 5

    输入: beginWord = "hit", endWord = "cog",
         wordList = ["hot","dot","dog","lot","log"]
    输出: 0  (endWord 不在 wordList 中)

约束条件:
    - 1 <= beginWord.length <= 10
    - endWord.length == beginWord.length
    - 1 <= wordList.length <= 5000
    - wordList[i].length == beginWord.length
    - beginWord, endWord 和 wordList[i] 由小写英文字母组成
    - beginWord != endWord
    - wordList 中的所有字符串互不相同

TL;DR:
    核心思路：
        方法1 BFS + 通配符预处理 ★：
            将每个单词转为「模式」（如 "hot" -> ["*ot","h*t","ho*"]），
            相同模式的单词可互相转换，避免 O(n^2 * L) 的边枚举。
            BFS 第一次到达 endWord 时的层数即为最短路径。

        方法2 BFS 简洁版：
            每个位置尝试替换所有 26 个字母，在 word_set 中查找，直观易写。

        方法3 双向 BFS（面试加分）：
            同时从 beginWord 和 endWord 出发，每次扩展较小的集合，
            搜索空间从 O(b^d) 降到 O(2*b^(d/2))。

    复杂度:
        方法1/2: Time O(n * L^2)，Space O(n * L)  [n=字典大小, L=单词长度]
        方法3:   实践中更快
"""

from typing import List
from collections import deque, defaultdict
import string


# ──────────────────────────────────────────────
# 方法1：BFS + 通配符预处理 ★
# ──────────────────────────────────────────────

def ladder_length_bfs(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    BFS 单词接龙（通配符预处理加速邻居查找）。
    """
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    L = len(beginWord)
    pattern_map = defaultdict(list)
    for word in wordList:
        for i in range(L):
            pattern = word[:i] + '*' + word[i + 1:]
            pattern_map[pattern].append(word)

    visited = {beginWord}
    queue = deque([(beginWord, 1)])

    while queue:
        word, length = queue.popleft()
        for i in range(L):
            pattern = word[:i] + '*' + word[i + 1:]
            for neighbor in pattern_map[pattern]:
                if neighbor == endWord:
                    return length + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, length + 1))
    return 0


# 保留原始接口名，兼容旧测试
def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    return ladder_length_bfs(begin_word, end_word, word_list)


# ──────────────────────────────────────────────
# 方法2：BFS 简洁版（26字母枚举）
# ──────────────────────────────────────────────

def ladder_length_bfs_simple(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """每个位置尝试替换所有 26 个字母，在 word_set 中查找。"""
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    visited = {beginWord}
    queue = deque([(beginWord, 1)])

    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                if c == word[i]:
                    continue
                new_word = word[:i] + c + word[i + 1:]
                if new_word == endWord:
                    return length + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    return 0


# ──────────────────────────────────────────────
# 方法3：双向 BFS（面试加分项）
# ──────────────────────────────────────────────

def ladder_length_bidirectional(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    双向 BFS：同时从起点和终点出发，每次扩展较小的集合。
    """
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    begin_visited = {beginWord}
    end_visited = {endWord}
    step = 1

    while begin_visited and end_visited:
        if len(begin_visited) > len(end_visited):
            begin_visited, end_visited = end_visited, begin_visited

        step += 1
        next_visited = set()

        for word in begin_visited:
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    if c == word[i]:
                        continue
                    new_word = word[:i] + c + word[i + 1:]
                    if new_word in end_visited:
                        return step
                    if new_word in word_set and new_word not in begin_visited:
                        next_visited.add(new_word)

        begin_visited = next_visited
        word_set -= begin_visited

    return 0


# ──────────────────────────────────────────────
# 测试
# ──────────────────────────────────────────────

def test():
    # 用例1: "hit" -> "cog" -> 5
    word_list1 = ["hot", "dot", "dog", "lot", "log", "cog"]
    assert ladder_length_bfs("hit", "cog", word_list1) == 5
    assert ladder_length_bfs_simple("hit", "cog", word_list1) == 5
    assert ladder_length_bidirectional("hit", "cog", word_list1) == 5

    # 用例2: endWord 不在 wordList -> 0
    word_list2 = ["hot", "dot", "dog", "lot", "log"]
    assert ladder_length_bfs("hit", "cog", word_list2) == 0
    assert ladder_length_bfs_simple("hit", "cog", word_list2) == 0
    assert ladder_length_bidirectional("hit", "cog", word_list2) == 0

    # 用例3: 一步直达 "a" -> "c" wordList=["a","b","c"] -> 2
    assert ladder_length_bfs("a", "c", ["a", "b", "c"]) == 2
    assert ladder_length_bfs_simple("a", "c", ["a", "b", "c"]) == 2

    # 用例4: 无法到达 -> 0
    assert ladder_length_bfs("hit", "xyz", ["hot", "dot"]) == 0

    # 用例5: "red" -> "tax" -> 4
    word_list5 = ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]
    assert ladder_length_bfs("red", "tax", word_list5) == 4

    print("All tests passed!")


if __name__ == "__main__":
    test()
