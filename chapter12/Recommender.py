import numpy as np


# 参考链接 https://blog.csdn.net/wickedvalley/article/details/79927699

def Jaccard(a, b):
    return 1.0 * (a * b).sum() / (a + b - a * b).sum()


class Recommender():
    sim = None

    def similarity(self, x, distance):
        print(len(x))
        # 构建物品和物品的同现矩阵 计算物品与物品间的相似度
        y = np.ones((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i, j] = distance(x[i], x[j])
        return y

    def fit(self, x, distance=Jaccard):
        self.sim = self.similarity(x, distance)

    def recommend(self, a):
        return np.dot(self.sim, a) * (1 - a)

    def hello(self):
        print('hello test')
