import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def statistics_number(filter_string):
    sql_string = 'select count(*) from all_gzdata where fullURL like "%%{0}%%" '.format(filter_string)
    df_count = pd.read_sql_query(sql_string, engine, chunksize=1024 * 5)
    df_count = [x['count(*)'] for x in df_count]
    # df_count = df_count[0]
    return df_count[0]


def handle_data(p):
    p = p[['fullURL', 'realIP', 'timestamp_format']]
    return p


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    # sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    total_count = pd.read_sql_query('select count(*) from all_gzdata', engine, chunksize=1024 * 5)
    # total_count 是生成器对象，遍历取出数据总数
    total_count = [x['count(*)'] for x in total_count]
    total_count = total_count[0]

    # 读取中间类型网页的数据总数
    # 这个sql要注意 %要转义一下
    sql_str = 'select count(*) from all_gzdata where fullURL like "%%midques_%%" '
    midques_count = pd.read_sql_query(sql_str, engine, chunksize=1024 * 5)
    midques_count = [x['count(*)'] for x in midques_count]
    midques_count = midques_count[0]

    # 统计'法律快车-律师助手', '咨询发布成功', '法律快搜与免费发布法律咨询'的数量
    page_title_list = ['法律快车-律师助手', '咨询发布成功', '法律快搜', '免费发布法律咨询']
    page_title_count_list = []
    for page_title in page_title_list:
        sql_str = 'select count(*) from all_gzdata where pageTitle like "%%{0}%%" '.format(page_title)
        temp_count = pd.read_sql_query(sql_str, engine, chunksize=1024 * 5)
        temp_count = [x['count(*)'] for x in temp_count]
        temp_count = temp_count[0]
        page_title_count_list.append(temp_count)
    # print(page_title_count_list)
    page_title_list = ['法律快车-律师助手', '咨询发布成功', '法律快搜与免费发布法律咨询']
    page_title_count_list[2] = page_title_count_list[2] + page_title_count_list[3]
    page_title_count_list = page_title_count_list[:-1]
    print(page_title_count_list)

    # 统计不包含关键字的

    # 统计无.html数据
    sql_str = 'select count(*) from all_gzdata where fullURL like "%%.html" '
    not_html_count = pd.read_sql_query(sql_str, engine, chunksize=1024 * 5)
    not_html_count = [x['count(*)'] for x in not_html_count]
    not_html_count = not_html_count[0]
    not_html_count = total_count - not_html_count
    print('---not_html_count----')
    print(not_html_count)

    # 统计重复记录
    # sql_str = 'select fullURL, realIP, timestamp_format from all_gzdata '
    duplicate_df = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    duplicate_df = [handle_data(i) for i in duplicate_df]
    duplicate_df = pd.concat(duplicate_df)
    print('*****duplicate_df******')
    print(duplicate_df.shape)
    print(duplicate_df.drop_duplicates())
    print(duplicate_df.shape)
