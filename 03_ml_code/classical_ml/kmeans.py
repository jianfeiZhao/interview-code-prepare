"""
题目：手写 K-Means 聚类
难度：Medium | 高频出现：阿里/字节/百度
标签：K-Means、EM算法、聚类


题目描述
---------
手写实现 K-Means 聚类算法（无监督学习）。
将 n 个样本划分为 k 个簇，使得簇内距离最小、簇间距离最大。
迭代执行分配步骤（E步）和更新步骤（M步）直到收敛。

输入/输出
----------
输入: X（数据矩阵 n×d）, k（聚类数）, max_iter（最大迭代次数）
输出: 簇标签 labels（长度 n），聚类中心 centroids（k×d）

超参数
------
- k：聚类数（需要预先指定）
- 初始化方法：随机、K-Means++
- 收敛条件：中心点变化 < tol 或达到 max_iter

TL;DR（30秒速览）
- 思路：随机初始化K个中心，交替执行分配步骤和更新步骤直到收敛
- 时间：O(n×k×d×iter)  收敛通常几十次迭代
- 陷阱：初始化影响结果（K-Means++ 更好），可能陷入局部最优

详细解析
---------
K-Means 算法步骤：
  1. 随机初始化 K 个中心（或用 K-Means++ 初始化）
  2. E步：每个点分配到最近的中心
  3. M步：每个簇的中心更新为该簇所有点的均值
  4. 重复 E/M 直到中心不再变化（或达到最大迭代次数）

K-Means++ 初始化：
  第一个中心随机选，后续中心以与已选中心最远的概率选取
  减少坏初始化的概率，加速收敛
"""

import numpy as np
from typing import Tuple


class KMeans:
    def __init__(self, k: int = 3, max_iter: int = 100, tol: float = 1e-4, init: str = 'kmeans++'):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.init = init
        self.centers_ = None
        self.labels_ = None
        self.inertia_ = None

    def _init_centers(self, X: np.ndarray) -> np.ndarray:
        if self.init == 'random':
            idx = np.random.choice(len(X), self.k, replace=False)
            return X[idx].copy()

        # K-Means++ 初始化
        centers = [X[np.random.randint(len(X))]]
        for _ in range(self.k - 1):
            dists = np.min(
                [np.sum((X - c) ** 2, axis=1) for c in centers], axis=0
            )
            probs = dists / dists.sum()
            centers.append(X[np.random.choice(len(X), p=probs)])
        return np.array(centers)

    def fit(self, X: np.ndarray) -> 'KMeans':
        centers = self._init_centers(X)
        for _ in range(self.max_iter):
            # E步：分配
            labels = self._assign(X, centers)
            # M步：更新
            new_centers = np.array([
                X[labels == j].mean(axis=0) if (labels == j).any() else centers[j]
                for j in range(self.k)
            ])
            if np.max(np.linalg.norm(new_centers - centers, axis=1)) < self.tol:
                break
            centers = new_centers

        self.centers_ = centers
        self.labels_ = self._assign(X, centers)
        self.inertia_ = sum(
            np.sum((X[self.labels_ == j] - centers[j]) ** 2)
            for j in range(self.k)
        )
        return self

    def _assign(self, X: np.ndarray, centers: np.ndarray) -> np.ndarray:
        dists = np.array([np.sum((X - c) ** 2, axis=1) for c in centers])
        return np.argmin(dists, axis=0)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self._assign(X, self.centers_)


if __name__ == "__main__":
    np.random.seed(42)
    X0 = np.random.randn(100, 2) + np.array([0, 0])
    X1 = np.random.randn(100, 2) + np.array([5, 5])
    X2 = np.random.randn(100, 2) + np.array([10, 0])
    X = np.vstack([X0, X1, X2])

    km = KMeans(k=3)
    km.fit(X)

    # 3个簇应该分开
    labels = km.labels_
    assert len(set(labels)) == 3
    # 每个真实簇的样本应该大部分被分到同一簇
    for start in [0, 100, 200]:
        cluster_labels = labels[start:start+100]
        most_common = Counter(cluster_labels).most_common(1)[0][1]
        assert most_common > 90, f"Cluster purity too low: {most_common}"

    from collections import Counter
    print(f"Inertia: {km.inertia_:.2f}")
    print("All tests passed.")
