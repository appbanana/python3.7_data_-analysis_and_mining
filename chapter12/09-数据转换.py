import pandas as pd
from sqlalchemy import create_engine


def handle_data(p):
    p = p.copy()
    p['fullURL'] = p['fullURL'].str.replace('_\d{0,2}\.html', '.html')
    return p


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
    sql = pd.read_sql('cleaned_gzdata', engine, chunksize=1024 * 5)
    result = [handle_data(i) for i in sql]
    # 去重前 df_result.shape (646578,, 6)
    df_result = pd.concat(result)
    print(df_result.shape)
    # 去除重复的数据
    df_result = df_result.drop_duplicates(subset=['realIP', 'fullURL'], keep='first')
    print('********' * 10)
    print(df_result.shape)
    # 去重后 df_result.shape (531229, 6)
    df_result.to_sql('cleaned_gzdata_one', engine, index=False, if_exists='append')




