import pandas as pd
from sqlalchemy import create_engine


# def clean_data(p):
#     p = p[['realIP']][p['fullURL'].str.contains('\.html')].copy()
#     return p['realIP'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # 分块统计各个IP的点击次数
    click_count = [i['realIP'].value_counts() for i in sql]
    click_count = pd.concat(click_count).groupby(level=0).sum()
    # 将Series转化为DataFrame
    # click_count = pd.DataFrame(click_count)
    # click_count[1] = 1
    # click_group_count = click_count.groupby(by='realIP').sum
    # click_group_count = click_group_count.reset_index()
    # click_group_count = pd.DataFrame(click_group_count)

    # print(click_count)

    # 将Series转化为DataFrame
    click_count = pd.DataFrame(click_count)
    click_count.columns = ['times']
    click_count['flag'] = 1
    total_df = click_count.groupby(by=['times']).sum()
    total_df.to_sql('click_group_count', engine, if_exists='append')

    print(total_df)
