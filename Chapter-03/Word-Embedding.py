'''
Author: NanluQingshi
Date: 2026-07-05 09:17:23
LastEditors: NanluQingshi
LastEditTime: 2026-07-05 09:31:17
Description: Word Embedding
'''
import numpy as np

# 词向量字典：每个词用一个二维向量表示，两个维度分别代表抽象的"语义坐标"
# 二维只是为了方便画图理解；实际应用中通常是 100~300 维
embeddings = {
  "king": np.array([0.9, 0.8]),     # king 的语义向量
  "queen": np.array([0.9, 0.2]),    # queen 的语义向量（x 与 king 接近，y 差很远）
  "man": np.array([0.7, 0.9]),      # man 的语义向量
  "woman": np.array([0.7, 0.3])     # woman 的语义向量
}

def cos_similarity(vec1, vec2):
  # ========== 完整手算示例：king 与 queen ==========
  # king  = [0.9, 0.8]
  # queen = [0.9, 0.2]
  #
  # ---- 第 1 步：点积（对应位置相乘再求和）----
  # 0.9×0.9 + 0.8×0.2 = 0.81 + 0.16 = 0.97 ← 方向一致程度
  dot_product = np.dot(vec1, vec2)

  # ---- 第 2 步：两个向量的长度（欧几里得范数）----
  # ||king||  = sqrt(0.9² + 0.8²) = sqrt(0.81 + 0.64) = sqrt(1.45) ≈ 1.204
  # ||queen|| = sqrt(0.9² + 0.2²) = sqrt(0.81 + 0.04) = sqrt(0.85) ≈ 0.922
  # 长度乘积 = 1.204 × 0.922 ≈ 1.110  ← 用来消除长度影响
  norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

  # ---- 第 3 步：余弦相似度 = 点积 / 长度乘积 ----
  # 0.97 / 1.110 ≈ 0.874  ← cos(夹角)
  # 值域 [-1, 1]：1 = 方向完全相同，0 = 正交无关，-1 = 方向完全相反
  return dot_product / norm_product

# king - man + woman
result_vec = embeddings["king"] - embeddings["man"] + embeddings["woman"]

# 计算结果向量与 “queen” 的相似度
sim = cos_similarity(result_vec, embeddings["queen"])
print(f"king - man + woman 的结果向量: {result_vec}")
print(f"该结果与 'queen' 的相似度: {sim:.4f}")