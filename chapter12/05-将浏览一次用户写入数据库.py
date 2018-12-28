import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # 分块统计各个IP的点击次数
    result = [i['realIP'].value_counts() for i in sql]
    click_count = pd.concat(result).groupby(level=0).sum()
    click_count = click_count.reset_index()
    click_count.columns = ['realIP', 'times']
    # 筛选出来点击一次的数据
    click_one_data = click_count[click_count['times'] == 1]
    # 筛选出来点击一次的realIP
    # print(click_count)
    """
                realIP  times
    1            95502      1
    2           103182      1
    4           136206      1
    5           140151      1
    6           155761      1
    8           159758      1
    9           213105      1

    """
    # 这里只能在次读取数据 因为sql是一个生成器类型，所以在使用过一次以后，就不能继续使用了。必须要重新执行一次读取。
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    # 取出这三列数据
    data = [i[['fullURLId', 'fullURL', 'realIP']] for i in sql]
    data = pd.concat(data)
    merge_data = pd.merge(click_one_data, data, on='realIP', how='left')
    # 点击一次的数据统计 写入数据库 以方便读取
    # merge_data.to_sql('click_one_count', engine, if_exists='append')

    # print(merge_data)
    """
                    realIP  times fullURLId                                            fullURL
    0            95502      1    101003    http://www.lawtime.cn/ask/question_7882607.html
    1           103182      1    101003    http://www.lawtime.cn/ask/question_7174864.html
    2           136206      1    101003    http://www.lawtime.cn/ask/question_8246285.html
    3           140151      1    107001  http://www.lawtime.cn/info/gongsi/slbgfgs/2011...
    4           155761      1    101003    http://www.lawtime.cn/ask/question_5951952.html
    5           159758      1    101003    http://www.lawtime.cn/ask/question_1909224.html
    6           213105      1    101003    http://www.lawtime.cn/ask/question_1586269.html

    """

    # 网页类型ID统计
    fullURLId_count = merge_data['fullURLId'].value_counts()
    fullURLId_count = fullURLId_count.reset_index()
    fullURLId_count.columns = ['fullURLId', 'count']
    fullURLId_count['percent'] = fullURLId_count['count'] / fullURLId_count['count'].sum() * 100
    print('*****' * 10)
    print(fullURLId_count)
    """
       fullURLId   count    percent
    0     101003  102560  77.626988
    1     107001   19443  14.716279
    2    1999001    9381   7.100417
    3     301001     515   0.389800
    4     102001      70   0.052983
    5     103003      45   0.034060

    """


    # 用户点击一次 浏览的网页统计
    fullURL_count = merge_data['fullURL'].value_counts()
    fullURL_count = fullURL_count.reset_index()
    fullURL_count.columns = ['fullURL', 'count']
    fullURL_count['percent'] = fullURL_count['count'] / fullURL_count['count'].sum() * 100
    print('*****' * 10)
    print(fullURL_count)
    """
                                                     fullURL  count   percent
    0      http://www.lawtime.cn/info/shuifa/slb/20121119...   1013  0.766733
    1      http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...    501  0.379204
    2         http://www.lawtime.cn/ask/question_925675.html    423  0.320166
    3      http://www.lawtime.cn/info/shuifa/slb/20121119...    367  0.277780
    4               http://www.lawtime.cn/ask/exp/13655.html    301  0.227825
    5                http://www.lawtime.cn/ask/exp/8495.html    241  0.182411
    6               http://www.lawtime.cn/ask/exp/13445.html    199  0.150622
    7                        http://www.lawtime.cn/guangzhou    177  0.133970

    """