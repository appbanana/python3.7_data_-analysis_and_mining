import time
import pandas as pd
import numpy as np
# from scipy import spatial
from sqlalchemy import create_engine


from Recommender import Recommender, Jaccard


# mariadb配置允许远程访问方式 https://blog.csdn.net/qq_24038207/article/details/79063246

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
    df_data = pd.read_sql('hunyin_data', engine)
    # print(df_data)
    """
               realIP                                            fullURL   type1   type2          type3
    0          116010  http://***/info/hunyin/lhlawlhxy/2011070713769...  zhishi  hunyin      lhlawlhxy
    1          418673  http://***/info/hunyin/lihunfangchan/201103101...  zhishi  hunyin  lihunfangchan
    2         1393009  http://***/info/hunyin/hunyinfagui/20110813143...  zhishi  hunyin    hunyinfagui
    3         1675790  http://***/info/hunyin/jihuashengyu/2012021516...  zhishi  hunyin   jihuashengyu
    4         1885994  http://***/info/hunyin/lihunfangchan/201012218...  zhishi  hunyin  lihunfangchan

    """
    # 用户10525 物品4333 应该使用基于物品的协同算法
    # 10535
    print(len(df_data['realIP'].value_counts()))
    # 4333
    print(len(df_data['fullURL'].value_counts()))

    # 将数据转换成0-1的矩阵
    # 只取用户reaIP和fullURL这两列数据
    start = time.process_time()
    df_data = df_data[['realIP', 'fullURL']]
    df_data = df_data.sort_values(by=['realIP', 'fullURL'], ascending=[True, True])

    # 构建新的DataFrame index为用户 列(特征)为所有不重复的fullURL [10535 rows x 4333 columns]
    # 这种方法理论上可行 实际上处理速度太慢 原因：数据特征向量太大了
    # realIP = df_data['realIP'].value_counts().index
    # realIP = np.sort(realIP)
    # fullURL = df_data['fullURL'].value_counts().index
    # fullURL = np.sort(fullURL)
    # D = pd.DataFrame([], index=realIP, columns=fullURL)
    # print(df_data.head())
    # for i in range(len(df_data)):
    #     ip = df_data.iloc[i, 0]
    #     url = df_data.iloc[i, 1]
    #     D.loc[ip, url] = 1
    #     print(ip)
    # D.fillna(0, inplace=True)
    # D.to_csv('./data/zero_one_1.csv')
    # end = time.process_time()
    # # 花费时间41160.895804  试过就知道了
    # print('花费时间%f' % (end - start))
    # print(D.head())

    # 方法改进
    # 将realIP置位索引 inplace 设置为True 会把原来的数据给替换掉
    df_data.set_index('realIP', inplace=True)
    print(df_data.head())
    """
                                                       fullURL
    realIP                                                    
    116010   http://***/info/hunyin/lhlawlhxy/2011070713769...
    418673   http://***/info/hunyin/lihunfangchan/201103101...
    1393009  http://***/info/hunyin/hunyinfagui/20110813143...
    1675790  http://***/info/hunyin/jihuashengyu/2012021516...
    1885994  http://***/info/hunyin/lihunfangchan/201012218...

    """
    # print(df_data.values)
    # [['http://***/info/hunyin/lhlawlhxy/20110707137693.html']
    #  ['http://***/info/hunyin/lihunfangchan/20110310125984.html']
    #  ['http://***/info/hunyin/hunyinfagui/20110813143541.html']
    #      ...
    #  ['http://***/info/hunyin/hunyinfagui/201411053308986.html']
    #  ['http://***/info/hunyin/jihuashengyu/201411053308990.html']
    #  ['http://***/info/hunyin/lhlawlhxy/20110707137693.html']]

    # 取出不为空的值作为索引 然后把它对应的值置位1
    ct = lambda x: pd.Series(1, index=x[pd.notnull(x)])
    temp = map(ct, df_data.values)
    data = pd.DataFrame(list(temp), index=df_data.index, dtype='int').fillna(0)
    data = data.groupby(level='realIP').sum()

    # 如果有大于1的全部置位1  其实是没有大于1的 data[data > 1].shape (10535, 4333)
    data[data > 1] = 1
    # 这种方法比较快 数据转化花费时间16.807064
    end = time.process_time()
    print('数据转化花费时间%f' % (end - start))

    # 这个尽量不要每次都要写入 文件太大 很耗时间  确保自己正确写入后就把它注释掉了 后面用到的话直接去这个文件读取
    # data.to_csv('./data/zero_one_2.csv')
    # 交叉验证
    df = data.copy()
    # 随机打乱数据
    sample = np.random.permutation(len(df))
    # 打乱数据
    df = df.take(sample)
    train = df.iloc[: int(len(df) * 0.9), :]
    test = df.iloc[int(len(df) * 0.9):, :]

    # print(train.columns)
    # print(train.index)

    df = df.values
    # (9481, 4333)
    train_data = df[: int(len(df) * 0.9), :]
    # (1054, 4333)
    test_data = df[int(len(df) * 0.9):, :]

    train_data = train_data.T
    test_data = test_data.T

    rec_model = Recommender()
    start = time.process_time()
    # 计算物品的相似度矩阵
    rec_model.fit(train_data)
    # print(rec_model.sim)
    df_sim = pd.DataFrame(rec_model.sim)
    df_sim.index = train.columns
    df_sim.columns = train.columns

    df_sim.to_csv('./data/similarity_matrix.csv')

    end = time.process_time()

    print('计算物品的相似度矩阵 花费时间 %f' % (end - start))

    print(df_sim)

    start = time.process_time()
    recommend_result = rec_model.recommend(test_data)
    recommend_result = pd.DataFrame(recommend_result)
    recommend_result.index = test.columns
    recommend_result.columns = test.index
    recommend_result.to_csv('./data/recommend_matrix.csv')
    end = time.process_time()

    print('计算推荐物品的矩阵 花费时间 %f' % (end - start))


