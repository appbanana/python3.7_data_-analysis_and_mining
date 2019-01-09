import time
import pandas as pd
import numpy as np


def popular_recommed(K, recomMatrix):
    recomMatrix.fillna(0, inplace=True)
    recommends = ['popular_rec' + str(y) for y in range(1, K + 1)]
    currentemp = pd.DataFrame([], index=recomMatrix.columns, columns=recommends)

    for i in range(len(recomMatrix.columns)):
        curentcol = recomMatrix.columns[i]
        # 取出用户数据 过滤掉不为0的数据 1代表用户未点击的网址
        temp = recomMatrix[curentcol][recomMatrix[curentcol] != 0]
        if len(temp) == 0:
            currentemp.iloc[i, :] = np.nan
        elif len(temp) < K:
            r = temp.index  # 注意：这个random是numpy模块的下属模块
            currentemp.iloc[i, :len(r)] = r
        else:
            r = temp.index[:K]
            currentemp.iloc[i, :] = r

    return currentemp


if __name__ == '__main__':
    # zero_one_2是数据零一化后的数据 点击过的网址为1 未点击过的为0
    file_name = './data/zero_one_2.csv'
    data_df = pd.read_csv(file_name, index_col=[0])
    # print(data_df.head())

    """
             http://***/info/hunyin/lhlawlhxy/20110707137693.html                          ...                           http://***/info/hunyin/lhlawlhqs/20120712164793.html
realIP                                                                                 ...                                                                               
116010                                                 1.0                             ...                                                                         0.0   
418673                                                 0.0                             ...                                                                         0.0   
1393009                                                0.0                             ...                                                                         0.0   
1675790                                                0.0                             ...                                                                         0.0   
1885994                                                0.0                             ...                                                                         0.0   
    """

    # 随机打乱数据
    sample = np.random.permutation(len(data_df))
    # 打乱数据
    df = data_df.take(sample)
    # train = df.iloc[: int(len(df) * 0.9), :]
    test = df.iloc[int(len(df) * 0.9):, :]

    df = df.values
    # (9481, 4333)
    # train_data = df[: int(len(df) * 0.9), :]
    # (1054, 4333)
    test_data = df[int(len(df) * 0.9):, :]

    # train_data = train_data.T
    test_data = test_data.T

    # df_test是用户浏览过的网页的矩阵形式，not_click_data则表示是用户未浏览过的网页的矩阵形式
    not_click_data = 1 - test_data
    # 这是用户未浏览过(待推荐）的网页的表格形式
    not_click_df = pd.DataFrame(not_click_data, index=test.columns, columns=test.index)
    not_click_df.index.name = 'fullURL'
    print(not_click_df.index.name)
    print(not_click_df.head())
    """
    realIP                                              617685369   3791662875  3150531039  4048699194  2161386359     ...      4028210446  806049972   4167205495  1681376554  2308652858
http://***/info/hunyin/lhlawlhxy/20110707137693...         1.0         1.0         1.0         1.0         1.0     ...             0.0         1.0         1.0         1.0         0.0
http://***/info/hunyin/lihunfangchan/2011031012...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/hunyinfagui/201108131435...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/jihuashengyu/20120215163...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/lihunfangchan/2010122187...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0

[5 rows x 1054 columns]

    """
    # 根据网页的点击热度排名
    print('*******' * 10)
    popular_data = data_df.T
    popular_data = popular_data.sum(axis=1)
    popular_data = pd.DataFrame(popular_data)
    popular_data.columns = ['num']
    popular_data.index.name = 'fullURL'
    popular_data = popular_data.sort_values(by='num', ascending=False)

    # print(popular_data)
    """
                                                           num
    fullURL                                                   
    http://***/info/hunyin/lhlawlhxy/20110707137693...  3507.0
    http://***/info/hunyin/hunyinfagui/201411053308...   509.0
    http://***/info/hunyin/jihuashengyu/20120215163...   457.0
    http://***/info/hunyin/jihuashengyu/20141105330...   211.0
    http://***/info/hunyin/jiehun/hunjia/2011092015...   192.0
    http://***/info/hunyin/hunyinfagui/201108131435...   190.0
    http://***/info/hunyin/lihunshouxu/201312042874...   172.0
    http://***/info/hunyin/feihunshengzinv/20110125...   114.0

    """

    # 接下来要not_click_df的索引按照popular_data中的fullURL顺序调整
    # 第一种直接使用reindex 参考链接：https://blog.csdn.net/songyunli1111/article/details/78953841
    # 第二种是merge 先合并 在按照num排序
    # 第三种方法使用category set_categories  reorder_categories 数据类型 参考链接：https://www.jianshu.com/p/2d3dd3e30d51
    list_custom = list(popular_data.index)
    not_click_df = not_click_df.reindex(list_custom)
    # print(not_click_df)
    """
    realIP                                              3029210996  918442360   3026064850  3102607287  2264677946     ...      1850505742  3111329913  494868238   3757720177  1519745550
fullURL                                                                                                            ...                                                                
http://***/info/hunyin/lhlawlhxy/20110707137693...         0.0         0.0         0.0         0.0         0.0     ...             1.0         1.0         1.0         1.0         0.0
http://***/info/hunyin/hunyinfagui/201411053308...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/jihuashengyu/20120215163...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/jihuashengyu/20141105330...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0
http://***/info/hunyin/jiehun/hunjia/2011092015...         1.0         1.0         1.0         1.0         1.0     ...             1.0         1.0         1.0         1.0         1.0

    """
    start = time.process_time()
    popular_result = popular_recommed(3, not_click_df)  # 调用随机推荐函数
    end = time.process_time()
    popular_result.to_csv('popular_result.csv')
    print(popular_result)
    """
                                                     popular_rec1                                       popular_rec2                                       popular_rec3
realIP                                                                                                                                                             
2348307832  http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...
171504604   http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...
4011605818  http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...
3184854967  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...  http://***/info/hunyin/jihuashengyu/2014110533...
4094818362  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...  http://***/info/hunyin/jihuashengyu/2014110533...
2757717873  http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...
102569332   http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...
412457486   http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...  http://***/info/hunyin/jihuashengyu/2014110533...
2794177834  http://***/info/hunyin/lhlawlhxy/2011070713769...  http://***/info/hunyin/hunyinfagui/20141105330...  http://***/info/hunyin/jihuashengyu/2012021516...

    """
