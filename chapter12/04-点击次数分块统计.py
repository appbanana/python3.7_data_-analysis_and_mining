import pandas as pd
from sqlalchemy import create_engine


# def clean_data(p):
#     p = p[['realIP']][p['fullURL'].str.contains('\.html')].copy()
#     return p['realIP'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('cleaned_gzdata', engine, chunksize=1024 * 5)

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
    1      132803
    2       44041
    3       17379
    4        9627
    5        5563
    6        3718
    7        2427

    """
    # total_df1 = pd.DataFrame(total_df, index=None)
    # print(total_df1.columns)

    total_df = total_df.reset_index()
    # print(total_df.columns)

    result = total_df.iloc[:8, :]
    # 消除警告 A value is trying to be set on a copy of a slice from a DataFrame
    result = result.copy()
    # result.loc[7, 'flag'] = total_df.iloc[8:, 1].sum()
    result.loc[7, 'flag'] = total_df.loc[total_df['times'] > 7, 'flag'].sum()
    result.loc[7, 'times'] = u'7次以上'

    # result.loc[result['times'] == 8, 'flag'] = 1000

    print(result)
