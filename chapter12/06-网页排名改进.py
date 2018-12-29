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
    # temp_type_count['flag'] = 1

    # print(type_count)
    """
                                                      fullURL  click_times fullURLId      realIP
    0                   http://www.lawtime.cn/faguizt/23.html         6503       199  1973622542
    1                   http://www.lawtime.cn/faguizt/23.html         6503       199  1973622542
    2                   http://www.lawtime.cn/faguizt/23.html         6503       199  1571045489
    3                   http://www.lawtime.cn/faguizt/23.html         6503       199  1571045489
    4                   http://www.lawtime.cn/faguizt/23.html         6503       199   225896631

    """

    # 统计各个类型的点击次数
    type_count_result = type_count.copy()
    # 统计fullURLId对应的总点击数
    type_count_result = type_count_result.drop_duplicates(subset='fullURL', keep='first')
    """
                                                      fullURL  click_times fullURLId      realIP
    0                   http://www.lawtime.cn/faguizt/23.html         6503       199  1973622542
    6503    http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         4938       107  1275347569
    11441                http://www.lawtime.cn/faguizt/9.html         4562       199   683972366
    16003   http://www.lawtime.cn/info/shuifa/slb/20121119...         4495       107  2319132987
    20498               http://www.lawtime.cn/faguizt/11.html         3976       199   192814350
    24474   http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         3305       107   838215995
    27779               http://www.lawtime.cn/faguizt/43.html         3251       199   225896631
    31030               http://www.lawtime.cn/faguizt/15.html         2718       199  2523538039

    """
    # 删除无效数据 删除fullURL，realIP这两列数据
    del type_count_result['fullURL']
    del type_count_result['realIP']
    # print(type_count_result)
    """
            click_times fullURLId
    0              6503       199
    6503           4938       107
    11441          4562       199
    16003          4495       107
    20498          3976       199
    24474          3305       107
    27779          3251       199
    31030          2718       199

    """
    # 计算各个fullURLId下总的点击数
    type_count_result = type_count_result.groupby(by=['fullURLId']).sum()
    type_count_result = type_count_result.reset_index()
    print(type_count_result)
    """
      fullURLId  click_times
    0       101       404535
    1       103         1715
    2       107       165057
    3       199        84302
    4       301        17412

    """

    # 接下来统计各个fullURLId总用户数
    temp_type_count = type_count.copy()
    temp_type_count = temp_type_count.groupby(by=['fullURLId', 'realIP']).sum()
    temp_type_count = temp_type_count.reset_index()
    # 把用户的realIP置位1 方便用户数统计计数
    temp_type_count['realIP'] = 1
    # 删除无效数据
    del temp_type_count['click_times']
    temp_type_count = temp_type_count.groupby(by='fullURLId').sum()
    # print('********' * 10)
    temp_type_count = temp_type_count.reset_index()
    print(temp_type_count)
    """
      fullURLId  realIP
    0       101  176163
    1       103     470
    2       107   55032
    3       199   32068
    4       301    3992

    """

    # temp_type_count与type_count_result开始合并
    type_count_result = pd.merge(type_count_result, temp_type_count, on='fullURLId', how='left')
    # print(type_count_result)
    type_count_result.columns = [u'网页类型', u'总点击数', u'用户数']
    type_count_result[u'平均点击率'] = type_count_result[u'总点击数'] / type_count_result[u'用户数']
    type_count_result = type_count_result.sort_values(by=[u'平均点击率'], ascending=False)
    # print(type_count_result)
    """
      网页类型    总点击数     用户数     平均点击率
        4  301   17412    3992  4.361723
        1  103    1715     470  3.648936
        2  107  165057   55032  2.999291
        3  199   84302   32068  2.628851
        0  101  404535  176163  2.296368
    """

    # 翻页网页统计
    # web_page_count = pd.DataFrame()
    # web_count['tempURL'] = web_count['fullURL'].str.extract(r'(.+)\.html', expand=False)
    # print(web_count)
    """
                                                      fullURL  click_times                                        tempfullURL
    0                   http://www.lawtime.cn/faguizt/23.html         6503                   http://www.lawtime.cn/faguizt/23
    1       http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         4938  http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...
    2                    http://www.lawtime.cn/faguizt/9.html         4562                    http://www.lawtime.cn/faguizt/9
    3       http://www.lawtime.cn/info/shuifa/slb/20121119...         4495  http://www.lawtime.cn/info/shuifa/slb/20121119...

    """
    # _数字 后面代表页码，我是简单匹配1到100页的数据
    web_page_count = web_count[web_count['fullURL'].str.contains('(.*)_[1-100]\.html')]
    print(web_page_count)

    # web_count['tempURL'] = web_count['fullURL'].str.extract(r'(.+)\.html', expand=False)

    # print(web_page_count)
    # for url in web_count['tempURL']:
    #     temp = web_count[web_count['fullURL'].str.startswith(url)]
    #     if not temp.empty:
    #         web_page_count.append(temp)
    # # [web_page_count.append(web_count[]) for url in web_count['tempURL']]
    # print(web_page_count)




