import time
import random
import pandas as pd
import numpy as np


def rand_recommd(K, recomMatrix):  #

    recomMatrix.fillna(0.0, inplace=True)  # 此处必须先填充空值
    recommends = ['random_rec' + str(y) for y in range(1, K + 1)]
    currentemp = pd.DataFrame([], index=recomMatrix.columns, columns=recommends)

    for i in range(len(recomMatrix.columns)):  # len(res.columns)1
        curentcol = recomMatrix.columns[i]
        temp = recomMatrix[curentcol][recomMatrix[curentcol] != 0]
        if len(temp) == 0:
            currentemp.iloc[i, :] = np.nan
        elif len(temp) < K:
            r = temp.index.take(np.random.permutation(len(temp)))  # 注意：这个random是numpy模块的下属模块
            currentemp.iloc[i, :len(r)] = r
        else:
            r = random.sample(list(temp.index), K)
            currentemp.iloc[i, :] = r
    return currentemp


if __name__ == '__main__':
    # zero_one_2是数据零一化后的数据 点击过的网址为1 未点击过的为0
    file_name = './data/zero_one_2.csv'
    df = pd.read_csv(file_name, index_col=[0])
    print(df.head())

    start = time.process_time()

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

    # df_test是用户浏览过的网页的矩阵形式，not_click_data则表示是用户未浏览过的网页的矩阵形式
    not_click_data = 1 - test_data
    # 这是用户未浏览过(待推荐）的网页的表格形式
    rand_matrix = pd.DataFrame(not_click_data, index=test.columns, columns=test.index)
    print(rand_matrix.head())

    start = time.process_time()
    random_result = rand_recommd(3, rand_matrix)  # 调用随机推荐函数
    end = time.process_time()
    print(random_result)
    """
                                                      random_rec1                                        random_rec2                                        random_rec3
    realIP                                                                                                                                                             
    3537045625  http://***/info/hunyin/jiehuntiaojian/20101026...  http://***/info/hunyin/lhlawlhqs/2013111228719...  http://***/info/hunyin/hunwaitongji/2014012428...
    435107511    http://***/info/hunyin/lhgz/201312262876320.html  http://***/info/hunyin/shanyangyiwu/2011022812...  http://***/info/hunyin/feihunshengzinv/2010111...
    1684084919  http://***/info/hunyin/xujialihun/qizhalihun/2...  http://***/info/hunyin/xujialihun/tongmoulihun...  http://***/info/hunyin/zhonghun/zhonghunzhishi...
    1216988280  http://***/info/hunyin/fuhunzaihun/20090824231...  http://***/info/hunyin/lihunfangchan/201012078...  http://***/info/hunyin/lihuntiaojian/201101251...
    3527710734  http://***/info/hunyin/lihuntiaojian/201202221...  http://***/info/hunyin/ccfghqcc/20110908150689...  http://***/info/hunyin/znfylaw/fuyangyiwu/2013...
    1662161422  http://***/info/lunwen/mfhunyin/2011072884401....  http://***/info/hunyin/fuqizhaiwu/201103031244...  http://***/info/hunyin/fuqigongtongcaichan/201...
    4028210446  http://***/info/hunyin/hunyinjiufen/hunnaqiang...  http://***/info/hunyin/hunyinfagui/20101018650...  http://***/info/hunyin/hunyinfaanli/2011060113...
    649601401   http://***/info/hunyin/jiehun/jiehunchengxu/20...  http://***/info/hunyin/junrenlihun/20111020159...  http://***/info/hunyin/jiatingbaoli/2015042233...

    """
