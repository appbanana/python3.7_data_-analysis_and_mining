import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql = pd.read_sql('all_gzdata', engine, chunksize=10000)

    # 分块统计各个IP的点击次数
    result = [i['realIP'].value_counts() for i in sql]
    result = pd.concat(result).groupby(level=0).sum()
    result = pd.DataFrame(result)
    result[1] = 1
    # 各个IP的点击次数
    print(result)
    """
                realIP  1
    82033            2  1
    95502            1  1
    103182           1  1
    116010           2  1
    136206           1  1

    """
    click_count = result.groupby(by=['realIP']).sum()
    # 将索引也变成其中的一列
    click_count = click_count.reset_index()
    click_count.columns = [u'点击次数', u'用户数']
    click_count[u'用户百分比'] = click_count[u'用户数'] / click_count[u'用户数'].sum() * 100
    # 记录百分比等于各个层上用户数乘以点击次数与所有的点击次数之比
    click_count[u'记录百分比'] = click_count[u'用户数'] * click_count[u'点击次数'] / result['realIP'].sum() * 100

    # 取出前8个数据
    # 后面加copy消除警告
    # A value is trying to be set on a copy of a slice from a DataFrame.
    # Try using .loc[row_indexer,col_indexer] = value instead
    click_count_8 = click_count.iloc[:8, :].copy()
    print(click_count_8)
    """
        点击次数     用户数      用户百分比      记录百分比
    0     1  132119  57.405854  15.776345
    1     2   44175  19.194087  10.549884
    2     3   17573   7.635488   6.295182
    3     4   10156   4.412793   4.850916
    4     5    5952   2.586151   3.553645
    5     6    4132   1.795359   2.960416
    6     7    2632   1.143607   2.200012
    7     8    2008   0.872478   1.918204


    """
    click_count_8.loc[7, u'点击次数'] = u'7次以上'
    click_count_8.loc[7, u'用户数'] = click_count.iloc[8:, 1].sum()
    click_count_8.loc[7, u'用户百分比'] = click_count.iloc[8:, 2].sum()
    click_count_8.loc[7, u'记录百分比'] = click_count.iloc[8:, 3].sum()
    print(click_count_8)
    """
       点击次数     用户数      用户百分比      记录百分比
    0     1  132119  57.405854  15.776345
    1     2   44175  19.194087  10.549884
    2     3   17573   7.635488   6.295182
    3     4   10156   4.412793   4.850916
    4     5    5952   2.586151   3.553645
    5     6    4132   1.795359   2.960416
    6     7    2632   1.143607   2.200012
    7  7次以上   11402   4.954182  51.895397

    """

    # 接下来统计7次以上 用户的分布情况

    # 本来想着这样操作来统计 有部分的数据不对 弃用
    # bins = [7, 100, 1000, 50000]
    # temp_count = click_count.iloc[8:, :]
    # click_count_cut = pd.cut(temp_count[u'点击次数'], bins=bins, right=True,)
    # print(click_count_cut)
    """
    301      (100, 1000]
    302      (100, 1000]
    303      (100, 1000]
    304    (1000, 50000]
    305    (1000, 50000]
    306    (1000, 50000]
    307    (1000, 50000]

    """

    # click_count_8 = click_count.copy()
    result_data = pd.DataFrame()
    result_data[u'点击次数'] = pd.Series(['8~100', '101~1000', '1000以上'])

    # 这样筛选出来的数据不对
    # value1 = click_count.iloc[:, 1][8:101].sum()
    # # value1 = click_count[u'用户数'][8:101].sum()
    # value2 = click_count.iloc[:, 1][101:1001].sum()
    # value3 = click_count.iloc[:, 1][1001:].sum()

    value1 = click_count.loc[click_count[u'点击次数'].isin(range(8, 101)), u'用户数'].sum()
    value2 = click_count.loc[click_count[u'点击次数'].isin(range(101, 1001)), u'用户数'].sum()
    value3 = click_count.loc[click_count[u'点击次数'] > 1000, u'用户数'].sum()
    result_data[u'用户数'] = [value1, value2, value3]
    print(result_data)
    """
           点击次数    用户数
        0     8~100  12952
        1  101~1000    439
        2    1000以上     19

    """
