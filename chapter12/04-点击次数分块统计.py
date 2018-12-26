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
    # print(total_df.max())
    """
    times     42790
    flag     132119

    """
    # 用户点击次数统计表
    result = total_df.iloc[:8, :]
    # 消除警告 A value is trying to be set on a copy of a slice from a DataFrame
    result = result.copy()
    result.columns = [u'点击次数', u'用户数']
    # result.loc[7, 'flag'] = total_df.iloc[8:, 1].sum()
    result.loc[7, u'用户数'] = total_df.loc[total_df['times'] > 7, 'flag'].sum()
    result.loc[7, u'点击次数'] = u'7次以上'
    result[u'用户百分比'] = result[u'用户数'] / result[u'用户数'].sum() * 100

    # print(result)
    """
   点击次数     用户数      用户百分比
    0     1  132119  57.405854
    1     2   44175  19.194087
    2     3   17573   7.635488
    3     4   10156   4.412793
    4     5    5952   2.586151
    5     6    4132   1.795359
    6     7    2632   1.143607
    7  7次以上   13410   5.826660


    """

    # 浏览7次以上的用户分析表

    # result = total_df.iloc[7:, :].copy()
    total_df = total_df.sort_values(by=['times'],)
    result_data = pd.DataFrame()
    result_data[u'点击次数'] = pd.Series(['8~100', '101~1000', '1000以上'])
    value1 = total_df.loc[total_df['times'] > 7 & total_df['times'] < 101, 'flag'].sum()
    value2 = total_df.loc[total_df['times'] > 100 & total_df['times'] < 1001, 'flag'].sum()
    value3 = total_df.loc[total_df['times'] > 1000, 'flag'].sum()
    result_data[u'用户数'] = [value1, value2, value3]


    # result = pd.cut(x=result['times'], bins=[7, 100, 1000, np.inf], )
    # print('********' * 10)
    # print(result)
    # result_data = result.value_counts()
    # print('********' * 10)
    print(result_data)
