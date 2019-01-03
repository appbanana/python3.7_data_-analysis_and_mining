import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def statistics_number(sql_string, sql_engine):
    """
    数据统计
    :param sql_string: 需要执行sql语句
    :return: 数据的数量
    """
    df_count = pd.read_sql_query(sql_string, sql_engine, chunksize=1024 * 5)
    # df_count 是生成器对象，遍历取出数据总数
    df_count = [x['count(*)'] for x in df_count]
    return df_count[0].at[0]


def handle_data(p):
    p = p[['fullURL', 'realIP', 'timestamp_format']]
    return p


# 使用sql查询与书中数据有出入 思路可以参考
if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    # 删除数据规则
    rule_list = []
    # 对应规则下数据的个数
    rule_count_list = []

    # 统计总数
    total_count = statistics_number('select count(*) from all_gzdata', engine)

    # 读取中间类型网页的数据总数
    # 这个sql要注意 %要转义一下
    sql_str = 'select count(*) from all_gzdata where fullURL like "%%midques_%%" '
    midques_count = statistics_number(sql_str, engine)
    rule_list.append('中间类型网页(带midques_关键字)')
    rule_count_list.append(midques_count)

    # 统计'法律快车-律师助手', '咨询发布成功', '法律快搜与免费发布法律咨询'的数量
    page_title_list = ['法律快车-律师助手', '咨询发布成功', '法律快搜', '免费发布法律咨询']
    page_title_count_list = []
    for page_title in page_title_list:
        sql_str = 'select count(*) from all_gzdata where pageTitle like "%%{0}%%" '.format(page_title)
        temp_count = statistics_number(sql_str, engine)
        page_title_count_list.append(temp_count)
    page_title_list = ['法律快车-律师助手', '咨询发布成功', '法律快搜与免费发布法律咨询']
    # 后两个合并 就是'法律快搜与免费发布法律咨询'数据的总数量
    page_title_count_list[2] = page_title_count_list[2] + page_title_count_list[3]
    # 截取数组到最后一个 ps（最后一个不要）
    page_title_count_list = page_title_count_list[:-1]
    # 将数据保存到数组中
    rule_list = rule_list + page_title_list
    rule_count_list = rule_count_list + page_title_count_list

    # 统计不包含关键字的 fullURL 不包含
    sql_str = 'select count(*) from all_gzdata where fullURL not like "%%lawtime%%" '
    no_key_word_count = statistics_number(sql_str, engine)
    rule_list.append('主网址不包含关键字')
    rule_count_list.append(no_key_word_count)

    # 统计无.html数据
    sql_str = 'select count(*) from all_gzdata where fullURL not like "%%.html" '
    not_html_count = statistics_number(sql_str, engine)
    rule_list.append('无.html点击行为的用户记录')
    rule_count_list.append(not_html_count)

    # 使用传统方法统计重复记录
    # duplicate_df = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    # duplicate_df = [handle_data(i) for i in duplicate_df]
    # duplicate_df_ = pd.concat(duplicate_df)
    # print('*****duplicate_df******')
    # print(len(duplicate_df_[duplicate_df_.duplicated() == True]), len(duplicate_df_.drop_duplicates()))

    # 使用sql去重 统计重复记录
    sql_str = 'select count(*) from (select distinct realIP, fullURL, timestamp_format from all_gzdata) as dt '
    # 去除重复数据后的数据
    duplicate_df_count = statistics_number(sql_str, engine)
    rule_list.append('重复记录')
    rule_count_list.append((total_count - duplicate_df_count))

    rule_result = pd.DataFrame(
        {u'删除数据规则': rule_list, u'删除数据记录': rule_count_list, u'原始数据记录': np.repeat(total_count, len(rule_list))})
    rule_result['百分比'] = rule_result[u'删除数据记录'] / rule_result[u'原始数据记录'] * 100
    print('*********' * 10)
    print(rule_result)
    """
                     删除数据规则  删除数据记录  原始数据记录        百分比
    0  中间类型网页(带midques_关键字)    2036  837450   0.243119
    1             法律快车-律师助手   52868  837450   6.312974
    2                咨询发布成功    5220  837450   0.623321
    3         法律快搜与免费发布法律咨询   11604  837450   1.385635
    4             主网址不包含关键字      77  837450   0.009195
    5       无.html点击行为的用户记录  165677  837450  19.783509
    6                  重复记录   35479  837450   4.236551

    """
