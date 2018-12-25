import pandas as pd
from sqlalchemy import create_engine


def clean_data(p):
    p = p[['realIP']][p['fullURL'].str.contains('\.html')].copy()
    return p['realIP'].value_counts()


# 遇到的问题 pandas写入数据到mysq(pymysql.err.InternalError) (1366, "Incorrect string value: for column  at row 1
# 解决方法：alter table cleaned_gzdata convert to character set utf8mb4

if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    for p in sql:
        p = p[['realIP', 'fullURL']][p['fullURL'].str.contains('\.html')].copy()
        # 保存到数据库的cleaned_gzdata表中（如果表不存在则自动创建）
        p.to_sql('cleaned_gzdata', engine, index=False, if_exists='append')

    # 过滤掉不含.html结尾的数据
    # click_count = [clean_data(i) for i in sql]
    # click_count = pd.concat(click_count).groupby(level=0).sum()
    # click_count = pd.DataFrame(click_count)
    # click_count.columns = ['times']
    # click_count['flag'] = 1

    # print(click_count.columns)
    # excel 最多可以写入655536行 256列数据
    # click_count.to_excel('./temp/clean_data.xls')
    # print(click_count.groupby(by=['realIP']).sum())
    # click_count.to_sql('clean_data', engine, index=False, if_exists='append')
