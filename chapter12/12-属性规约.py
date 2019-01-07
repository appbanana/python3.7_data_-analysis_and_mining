import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

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
    realIP = df_data['realIP'].value_counts().index
    realIP = np.sort(realIP)
    fullURL = df_data['fullURL'].value_counts().index
    fullURL = np.sort(fullURL)
    # 构建新的DataFrame index为用户 列(特征)为所有不重复的fullURL [10535 rows x 4333 columns]
    D = pd.DataFrame([], index=realIP, columns=fullURL)
    print(df_data.head())
    for i in range(len(df_data)):
        ip = df_data.iloc[i, 0]
        url = df_data.iloc[i, 1]
        D.loc[ip, url] = 1
        print(ip)
    D.fillna(0, inplace=True)
    D.to_csv('./data/zero_one.csv')
    end = time.process_time()
    print('花费时间%f' % (end - start))
    print(D.head())
