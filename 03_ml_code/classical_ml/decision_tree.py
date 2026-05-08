"""
题目：手写决策树（信息增益）
难度：Hard | 高频出现：字节/阿里
标签：决策树、信息增益、ID3


题目描述
---------
手写实现决策树分类器（CART 算法）。
通过递归地选择最优特征和切分点，将训练数据划分为纯净度更高的子集，
构建二叉决策树用于分类任务。

关键概念：
  - 基尼不纯度（Gini Impurity）：CART 使用的划分准则
  - 信息增益（Information Gain）：ID3/C4.5 使用的准则
  - 停止条件：最大深度、最小样本数、节点纯净

输入/输出
----------
输入: X（特征矩阵）, y（标签）, max_depth（最大深度）
输出: 拟合后的决策树模型，predict(X_test) 返回预测标签

TL;DR（30秒速览）
- 信息增益 = 父节点熵 - 子节点加权熵，选增益最大的特征分裂
- 递归构建：直到样本同类/无特征/达到最大深度
- 面试重点：熵的公式、信息增益计算、剪枝策略

详细解析
---------
信息熵：H(D) = -Σ p_k * log2(p_k)
信息增益：Gain(D, A) = H(D) - Σ |D_v|/|D| * H(D_v)

决策树三要素：
  1. 特征选择：信息增益（ID3）、增益率（C4.5）、基尼系数（CART）
  2. 树的生成：递归分裂
  3. 剪枝：防止过拟合（预剪枝/后剪枝）
"""

import numpy as np
from collections import Counter
from typing import Optional


class TreeNode:
    def __init__(self, feature_idx=None, threshold=None, left=None, right=None, label=None):
        self.feature_idx = feature_idx  # 分裂特征
        self.threshold = threshold       # 分裂阈值（二值特征时为None）
        self.left = left
        self.right = right
        self.label = label               # 叶节点的预测标签


class DecisionTreeClassifier:
    def __init__(self, max_depth: int = 10, min_samples_split: int = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _entropy(self, y: np.ndarray) -> float:
        n = len(y)
        counts = Counter(y)
        return -sum((c/n) * np.log2(c/n + 1e-12) for c in counts.values())

    def _information_gain(self, y, y_left, y_right) -> float:
        n = len(y)
        gain = self._entropy(y)
        gain -= (len(y_left) / n) * self._entropy(y_left)
        gain -= (len(y_right) / n) * self._entropy(y_right)
        return gain

    def _best_split(self, X, y):
        best_gain, best_feat, best_thresh = -1, None, None
        for feat in range(X.shape[1]):
            thresholds = np.unique(X[:, feat])
            for thresh in thresholds:
                left_mask = X[:, feat] <= thresh
                right_mask = ~left_mask
                if left_mask.sum() < 1 or right_mask.sum() < 1:
                    continue
                gain = self._information_gain(y, y[left_mask], y[right_mask])
                if gain > best_gain:
                    best_gain, best_feat, best_thresh = gain, feat, thresh
        return best_feat, best_thresh

    def _build(self, X, y, depth) -> TreeNode:
        # 终止条件
        if len(set(y)) == 1 or depth >= self.max_depth or len(y) < self.min_samples_split:
            return TreeNode(label=Counter(y).most_common(1)[0][0])

        feat, thresh = self._best_split(X, y)
        if feat is None:
            return TreeNode(label=Counter(y).most_common(1)[0][0])

        left_mask = X[:, feat] <= thresh
        left = self._build(X[left_mask], y[left_mask], depth + 1)
        right = self._build(X[~left_mask], y[~left_mask], depth + 1)
        return TreeNode(feature_idx=feat, threshold=thresh, left=left, right=right)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.root = self._build(X, y, 0)
        return self

    def _predict_one(self, x, node) -> int:
        if node.label is not None:
            return node.label
        if x[node.feature_idx] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._predict_one(x, self.root) for x in X])

    def score(self, X, y) -> float:
        return np.mean(self.predict(X) == y)


if __name__ == "__main__":
    np.random.seed(42)
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=200, n_features=4, random_state=42)
    split = 160
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    dt = DecisionTreeClassifier(max_depth=5)
    dt.fit(X_train, y_train)
    acc = dt.score(X_test, y_test)
    print(f"Accuracy: {acc:.4f}")
    assert acc > 0.75, f"Expected >0.75, got {acc}"
    print("All tests passed.")
