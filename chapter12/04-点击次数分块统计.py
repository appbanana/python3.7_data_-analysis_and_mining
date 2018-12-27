import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# def clean_data(p):
#     p = p[['realIP']][p['fullURL'].str.contains('\.html')].copy()
#     return p['realIP'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # 分块统计各个IP的点击次数
    click_count = [i['realIP'].value_counts() for i in sql]
    click_count = pd.concat(click_count).groupby(level=0).sum()
    # 将Series转化为DataFrame
    click_count = pd.DataFrame(click_count)
    click_count.columns = ['times']
    click_count['flag'] = 1
    # print(click_count)
    """
                times  flag
    82033           2     1
    95502           1     1
    103182          1     1
    116010          2     1
    136206          1     1
    140151          1     1
    155761          1     1
    159601          2     1
    159758          1     1
    213105          1     1
    226318          2     1

    """

    total_df = click_count.groupby(by=['times']).sum()
    # print(total_df)
    """
             flag
    times        
    1      132119
    2       44175
    3       17573
    4       10156
    5        5952
    6        4132
    7        2632
    8        2008
    ...
    ...
    """
    # total_df1 = pd.DataFrame(total_df, index=None)
    # print(total_df1.columns)
    # 自动重新设置index并将原来的index作为columns
    total_df = total_df.reset_index()
    # print(total_df.columns)

    # result = total_df.iloc[:8, :]
    #
    # # 消除警告 A value is trying to be set on a copy of a slice from a DataFrame
    # result = result.copy()
    # result.columns = [u'点击次数', u'用户数']
    #
    # result.loc[7, 'flag'] = total_df.iloc[8:, 1].sum()
    # result.loc[7, u'用户数'] = total_df.loc[total_df['times'] > 7, 'flag'].sum()
    # result.loc[7, u'点击次数'] = u'7次以上'
    #
    # print(result)
    total_df.columns = [u'点击次数', u'用户数']
    # 用户点击次数统计表
    total_df[u'用户百分比'] = total_df[u'用户数'] / total_df[u'用户数'].sum() * 100
    # 用户点击次数与用户总数相比
    total_df[u'记录百分比'] = total_df[u'用户数'] * total_df[u'点击次数'] / click_count[u'times'].sum() * 100
    result = total_df.iloc[:8, :]
    result.loc[7, u'点击次数'] = u'7次以上'
    # result.loc[7, '用户数'] = total_df.iloc[8:, 1].sum()
    result.loc[7, u'用户数'] = total_df.loc[total_df[u'点击次数'] > 7, u'用户数'].sum()
    result.loc[7, u'用户百分比'] = total_df.loc[total_df[u'点击次数'] > 7, u'用户百分比'].sum()
    result.loc[7, u'记录百分比'] = total_df.loc[total_df[u'点击次数'] > 7, u'记录百分比'].sum()

    print(result)
    """
   点击次数     用户数      用户百分比      记录百分比
    0     1  132119  57.405854  15.776345
    1     2   44175  19.194087  10.549884
    2     3   17573   7.635488   6.295182
    3     4   10156   4.412793   4.850916
    4     5    5952   2.586151   3.553645
    5     6    4132   1.795359   2.960416
    6     7    2632   1.143607   2.200012
    7  7次以上   13410   5.826660  53.813601


    """




    # 浏览7次以上的用户分析表
    total_df = total_df.sort_values(by=[u'点击次数'],)
    result_data = pd.DataFrame()
    result_data[u'点击次数'] = pd.Series(['8~100', '101~1000', '1000以上'])
    # 这两句也可以
    # value1 = total_df[total_df['times'].isin(range(7, 101))].iloc[:, 1]
    # value2 = total_df[total_df['times'].isin(range(101, 1001))].iloc[:, 1]
    value1 = total_df.loc[total_df[u'点击次数'].isin(range(8, 101)), u'用户数'].sum()
    value2 = total_df.loc[total_df[u'点击次数'].isin(range(101, 1001)), u'用户数'].sum()

    value3 = total_df.loc[total_df[u'点击次数'] > 1000, u'用户数'].sum()
    result_data[u'用户数'] = [value1, value2, value3]

    """
           点击次数    用户数
        0     8~100  12952
        1  101~1000    439
        2    1000以上     19

    """

    # 浏览7次以上用户分析表
    result_data_7 = total_df.iloc[7:, :]
    # print(total_df.max())
    """
    times     42790
    flag     132119

    """
    # 用于划分区间 这样不太对
    bins = [7, 100, 1000, 50000]
    result_data_7 = pd.cut(result_data_7[u'点击次数'], bins=bins, right=True,)
    # result_data_7 = pd.DataFrame(result_data_7.value_counts())
    # print(result_data_7)
    """
    这个数据有问题
    302      (100, 1000]
    303      (100, 1000]
    304    (1000, 50000]
    305    (1000, 50000]
    306    (1000, 50000]

    """