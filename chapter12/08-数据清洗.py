import pandas as pd
from sqlalchemy import create_engine


def handle_full_url(p):
    p = p[['userID', 'realIP', 'timestamp_format', 'ymd', 'pageTitle', 'fullURL']].copy()

    # 只要以.html结尾的  & 只要包含主网址（lawtime) & 网址中间没有midques_的
    # 以.html结尾的
    end_with_html = p['fullURL'].str.endswith('.html')
    # 包含关键字
    key_word_cond = p['fullURL'].str.contains('lawtime')
    # 不包含中间型网页的
    midques_cond = ~p['fullURL'].str.contains('midques_')

    # 接下来处理pageTitle
    # 法律快车 - 律师助手 免费发布法律咨询 咨询发布成功 法律快搜 全部过滤掉
    helper_cond = ~p['pageTitle'].str.contains('法律快车-律师助手', na=False)
    free_cond = ~p['pageTitle'].str.contains('免费发布法律咨询', na=False)
    advisory_cond = ~p['pageTitle'].str.contains('咨询发布成功', na=False)
    search_cond = ~p['pageTitle'].str.contains('法律快搜', na=False)

    p = p[end_with_html & key_word_cond & midques_cond & helper_cond & free_cond & advisory_cond & search_cond]

    return p


# 使用sql查询与书中数据有出入 思路可以参考
if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    result = [handle_full_url(i) for i in sql]
    df_result = pd.concat(result)
    # 去除重复的数据
    df_result = df_result.drop_duplicates()
    df_result.to_sql('cleaned_gzdata', engine, index=False, if_exists='append')

    print(df_result.head())
