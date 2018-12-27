import pandas as pd
from sqlalchemy import create_engine
# import pymysql


# def handle_data(p):
#     p = p[["realIP", "fullURL", 'fullURLId']]
#     return p['realIP'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # 分块统计各个IP的点击次数
    result = [i['realIP'].value_counts() for i in sql]
    click_count = pd.concat(result).groupby(level=0).sum()
    # click_count = pd.DataFrame(click_count)
    click_count = click_count.reset_index()
    click_count.columns = ['realIP', 'times']
    # 筛选出来点击一次的数据
    click_count = click_count[click_count['times'] == 1]

    # print(click_count)
    print(click_count)
