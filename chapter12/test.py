import pandas as pd
import numpy as np
from Recommender import Recommender


if __name__ == '__main__':

    df = pd.read_csv('./data/zero_one_1.csv')
    # df2 = pd.read_csv('./data/zero_one_2.csv')
    # 随机打乱数据
    sample = np.random.permutation(len(df))
    # 打乱数据
    df = df.take(sample)
    train = df.iloc[: int(len(df) * 0.9), :]
    test = df.iloc[int(len(df) * 0.9):, :]

    df = df.values
    # (9481, 4333)
    train_data = df[: int(len(df) * 0.9), :]
    # (1054, 4333)
    test_data = df[int(len(df) * 0.9):, :]

    train_data = train_data.T
    test_data = test_data.T

    r = Recommender()
    print(r.hello())
    print(dir(r))
    # start = time.process_time()
    # # 计算物品的相似度矩阵
    # sim = r.fit(train_data)
    # df_sim = pd.DataFrame(sim)
    # end = time.process_time()
