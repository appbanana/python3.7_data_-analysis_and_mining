import pandas as pd
from sqlalchemy import create_engine


# 这样不行 不能统计用户的点击次数
def handle_data1(p):
    p = p[['fullURL']][p['fullURL'].str.contains('\.html')].copy()
    return p['fullURL'].value_counts()


def handle_data(p):
    p = p[['fullURL', 'fullURLId', 'realIP']][p['fullURL'].str.contains('\.html')].copy()
    return p


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # 第一种handle_data1 是可以统计网页的点击次数 有一定的局限性 你无法统计用户数 改进handle_data
    # result = [handle_data1(i) for i in sql]
    # click_count = pd.concat(result).groupby(level=0).sum()
    # click_count = click_count.reset_index()
    # click_count.columns = ['fullURL', 'click_times']
    # click_count = click_count.sort_values(by='click_times', ascending=False)
    # print(click_count)
    """
                                                      fullURL  click_times
    238371              http://www.lawtime.cn/faguizt/23.html         6503
    260061  http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         4938
    238486               http://www.lawtime.cn/faguizt/9.html         4562
    281373  http://www.lawtime.cn/info/shuifa/slb/20121119...         4495
    238298              http://www.lawtime.cn/faguizt/11.html         3976
    260065  http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         3305

    """

    # 改进后的handle_data
    result = [handle_data(i) for i in sql]
    click_count = pd.concat(result)
    # print(click_count)
    """
                                                    fullURL fullURLId      realIP
    0     http://www.lawtime.cn/info/hunyin/hunyinfagui/...    107001  2683657840
    1              http://www.lawtime.cn/ask/exp/17199.html   1999001   973705742
    2       http://www.lawtime.cn/ask/question_3893276.html    101003  3104681075
    3       http://www.lawtime.cn/ask/question_5281741.html    101003   308351962
    4     http://www.lawtime.cn/info/hunyin/hunyinfagui/...    107001  2683657840

    """

    # 网页统计
    web_count = click_count['fullURL'].value_counts()
    # web_count = pd.DataFrame(web_count)
    # web_count.index.name = 'fullURL'
    # web_count.columns = ['click_times', ]

    web_count = web_count.reset_index()
    web_count.columns = ['fullURL', 'click_times', ]
    # print(web_count)
    """
                                                  fullURL  click_times
    0                   http://www.lawtime.cn/faguizt/23.html         6503
    1       http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         4938
    2                    http://www.lawtime.cn/faguizt/9.html         4562
    3       http://www.lawtime.cn/info/shuifa/slb/20121119...         4495
    4                   http://www.lawtime.cn/faguizt/11.html         3976


    """

    # 类型点击
    click_count['fullURLId'] = click_count['fullURLId'].str.extract('(\d{3})')

    type_count = pd.merge(web_count, click_count, on='fullURL', how='left')
    # print(type_count)
    """
                                                      fullURL  click_times fullURLId      realIP
    0                   http://www.lawtime.cn/faguizt/23.html         6503       199  1973622542
    1                   http://www.lawtime.cn/faguizt/23.html         6503       199  1973622542
    2                   http://www.lawtime.cn/faguizt/23.html         6503       199  1571045489
    3                   http://www.lawtime.cn/faguizt/23.html         6503       199  1571045489
    4                   http://www.lawtime.cn/faguizt/23.html         6503       199   225896631

    """
    temp_type_count = type_count.copy()
    del temp_type_count['realIP']
    temp_type_count = temp_type_count.drop_duplicates(subset='fullURL', keep='first')
    # print(temp_type_count)
    print('*******' * 10)
    print(temp_type_count['click_times'].sum())
    """
                                                          fullURL  click_times fullURLId
    0                   http://www.lawtime.cn/faguizt/23.html         6503       199
    6503    http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         4938       107
    11441                http://www.lawtime.cn/faguizt/9.html         4562       199
    16003   http://www.lawtime.cn/info/shuifa/slb/20121119...         4495       107
    20498               http://www.lawtime.cn/faguizt/11.html         3976       199
    24474   http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         3305       107

    """
    fullURLId_group_sum = temp_type_count.groupby(by='fullURLId').sum()
    # print(fullURLId_group_sum)
    """
                   click_times
    fullURLId             
    101             404535
    103               1715
    107             165057
    199              84302
    301              17412

    """
    temp_type_count = type_count.copy()
    temp_type_count = temp_type_count.groupby(by=['fullURLId', 'realIP']).sum()
    temp_type_count = temp_type_count.reset_index()
    temp_type_count['flag'] = 1
    print(temp_type_count)
    """
           fullURLId      realIP  click_times  flag
    0            101       82033            1     1
    1            101       95502           14     1
    2            101      103182            1     1
    3            101      136206           10     1
    4            101      155761            1     1
    ...
        
    267704       301  4255269489            1     1
    267705       301  4258406777            7     1
    267706       301  4258567694            1     1
    267707       301  4258756465            1     1



    """
    temp_type_count = temp_type_count.groupby(by=['fullURLId']).sum()
    print('****' * 15)
    print(temp_type_count)

    type_count_result = fullURLId_group_sum.reset_index()
    type_count_result = [u'网页类型', u'总点击次数']
    type_count_result['用户数'] = temp_type_count['flag']
    type_count_result['平均点击率'] = temp_type_count['总点击次数'] / temp_type_count['用户数']

    print(type_count_result)


