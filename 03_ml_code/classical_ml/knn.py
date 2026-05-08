"""
题目：手写 K 近邻分类器（KNN）
难度：Medium | 高频出现：阿里/字节/百度
标签：KNN、距离计算、分类


题目描述
---------
手写实现 K 近邻分类器（K-Nearest Neighbors, KNN）。
给定训练集和测试点，计算测试点到所有训练点的距离，
取最近的 K 个邻居进行多数投票，决定测试点所属类别。
无需显式训练，属于懒学习（Lazy Learning）算法。

输入/输出
----------
输入: X_train（训练特征矩阵）, y_train（训练标签）, X_test（测试集）, k（邻居数）
输出: y_pred（预测标签列表）

超参数
------
- k：邻居数（太小过拟合，太大欠拟合，通常取奇数）
- 距离度量：欧氏距离（默认）、曼哈顿距离、余弦相似度

TL;DR（30秒速览）
- 思路：计算测试点与所有训练点距离，取最近 K 个，投票决定分类
- 时间：O(n×d) 预测单点，n=训练样本数，d=特征维度
- 关键超参：K 值选择（通常取奇数，交叉验证选最优）

详细解析
---------
KNN 三要素：
  1. K 值：太小过拟合，太大欠拟合
  2. 距离度量：欧氏距离（L2）、曼哈顿距离（L1）、余弦相似度
  3. 决策规则：多数投票（分类）、均值（回归）

优化：KD-Tree 将查询复杂度降至 O(log n)
"""

import numpy as np
from collections import Counter
from typing import List


class KNNClassifier:
    def __init__(self, k: int = 3, distance: str = 'euclidean'):
        self.k = k
        self.distance = distance

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.X_train = X
        self.y_train = y
        return self

    def _compute_distances(self, x: np.ndarray) -> np.ndarray:
        if self.distance == 'euclidean':
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        elif self.distance == 'manhattan':
            return np.sum(np.abs(self.X_train - x), axis=1)
        else:
            raise ValueError(f"Unknown distance: {self.distance}")

    def predict_one(self, x: np.ndarray) -> int:
        distances = self._compute_distances(x)
        k_indices = np.argsort(distances)[:self.k]
        k_labels = self.y_train[k_indices]
        return Counter(k_labels).most_common(1)[0][0]

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self.predict_one(x) for x in X])

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        predictions = self.predict(X)
        return np.mean(predictions == y)


if __name__ == "__main__":
    np.random.seed(42)
    # 生成两类数据
    X0 = np.random.randn(50, 2) + np.array([0, 0])
    X1 = np.random.randn(50, 2) + np.array([3, 3])
    X = np.vstack([X0, X1])
    y = np.array([0] * 50 + [1] * 50)

    # 训练测试集分割
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNNClassifier(k=3)
    knn.fit(X_train, y_train)
    acc = knn.score(X_test, y_test)
    print(f"Accuracy: {acc:.4f}")
    assert acc > 0.9, f"Expected accuracy > 0.9, got {acc}"
    print("All tests passed.")
