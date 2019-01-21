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
    print(web_count)
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
    # print(type_count_result)
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
    # print(temp_type_count)
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
    print(type_count_result)
    """
      网页类型    总点击数     用户数     平均点击率
        4  301   17412    3992  4.361723
        1  103    1715     470  3.648936
        2  107  165057   55032  2.999291
        3  199   84302   32068  2.628851
        0  101  404535  176163  2.296368
    """

    # 翻页网页统计
    # _数字 后面代表页码，我是简单匹配1到100页的数据
    web_page_count = web_count[web_count['fullURL'].str.contains('_\d{1,2}\.html')]
    # 把'_数字.html'替换成'.html'
    web_page_count['tempURL'] = web_page_count['fullURL'].str.replace('_\d{0,2}\.html', '.html')
    # print(web_page_count)
    """
                                                      fullURL  click_times                                            tempURL
    5       http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...         3305  http://www.lawtime.cn/info/hunyin/lhlawlhxy/20...
    10      http://www.lawtime.cn/info/shuifa/slb/20121119...         2161  http://www.lawtime.cn/info/shuifa/slb/20121119...
    24      http://www.lawtime.cn/info/minshi/fagui/201305...          653  http://www.lawtime.cn/info/minshi/fagui/201305...
    35      http://www.lawtime.cn/info/hunyin/hunyinfagui/...          440  http://www.lawtime.cn/info/hunyin/hunyinfagui/...
    40      http://www.lawtime.cn/info/jiaotong/jtlawjtxgf...          377  http://www.lawtime.cn/info/jiaotong/jtlawjtxgf...


    """
    # 这样做的目的为了一会过滤出个数大于1的网址 个数大于1才有翻页的可能
    temp_web_page_count = web_page_count['tempURL'].value_counts()
    temp_web_page_count = temp_web_page_count.reset_index()
    temp_web_page_count.columns = ['tempURL', u'出现次数']
    temp_web_page_count = temp_web_page_count[temp_web_page_count[u'出现次数'] > 1]
    temp_web_page_count = temp_web_page_count.sort_values(by=u'出现次数', ascending=False)
    # print(temp_web_page_count)
    """
                                                    tempURL  出现次数
    0     http://www.lawtime.cn/info/hetong/htfalv/20131...    31
    1     http://www.lawtime.cn/info/xingshisusongfa/fal...    29
    2     http://www.lawtime.cn/info/hehuo/falvguiding/2...    25
    4     http://www.lawtime.cn/info/jiaotong/shpcbaoxia...    24
    3     http://www.lawtime.cn/info/xingfa/xingfaquanwe...    24
    5     http://www.lawtime.cn/info/minshi/fagui/201401...    22
    6     http://www.lawtime.cn/info/hetong/zlht/2011030...    22
    7     http://www.lawtime.cn/info/gongsi/gszc/2011052...    20
    8                     http://law.lawtime.cn/p1area.html    20

    """
    # 合并数据 以temp_web_page_count为基准
    temp_web_page_count = pd.merge(temp_web_page_count, web_page_count, on='tempURL', how='left')
    # 以'http://***/'替换'http://www.域名.cn/info' 方便数据查看 我的正则比较简单粗暴
    temp_web_page_count['tempURL'] = temp_web_page_count['tempURL'].str.replace('(.*)/info', 'http://***/',
                                                                                regex=True)
    temp_web_page_count['fullURL'] = temp_web_page_count['fullURL'].str.replace('(.*)/info', 'http://***/',
                                                                                regex=True)
    # 过滤掉tempURL出现一次的数据  因为翻页的话tempURL出现的次数要大于1次
    temp_web_page_count = temp_web_page_count[temp_web_page_count[u'出现次数'] > 1]
    # 删除这一列 因为它的使命已经完成
    del temp_web_page_count['出现次数']
    # 打印出来数据较多 因此在过滤到点击次数大于100的数据
    temp_web_page_count = temp_web_page_count[temp_web_page_count[u'click_times'] > 100]
    temp_web_page_count = temp_web_page_count.sort_values(by=['fullURL'], ascending=True)
    # temp_web_page_count = temp_web_page_count.groupby()

    # print(temp_web_page_count)
    """
                                                    tempURL                                            fullURL  click_times
    1519        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_4.html          653
    1520        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_5.html          177
    1521        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_6.html          138
    1522        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_2.html          129
    1523        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_7.html          126
    1524        http://***//minshi/fagui/2013051382463.html      http://***//minshi/fagui/2013051382463_3.html          111
    4276   http://***//laodong/ldzyjygl/20140312142061.html  http://***//laodong/ldzyjygl/20140312142061_2....          173
    4277   http://***//laodong/ldzyjygl/20140312142061.html  http://***//laodong/ldzyjygl/20140312142061_3....          112
    6649  http://***//laodong/ldzyjqdy/201411043308948.html  http://***//laodong/ldzyjqdy/201411043308948_2...          186
    4708  http://***//laodong/gsbxtiaoli/201408193306484...  http://***//laodong/gsbxtiaoli/201408193306484...          106
    ...
    ...
    """
    del temp_web_page_count['tempURL']
    """
                                                    fullURL  click_times
    2297     http://***//hetong/ldht/201311152872128_2.html          377
    2298     http://***//hetong/ldht/201311152872128_3.html          218
    2299     http://***//hetong/ldht/201311152872128_4.html          146
    2300     http://***//hetong/ldht/201311152872128_5.html          122
    7433  http://***//hunyin/hunyinfagui/20110813143541_...          172
    7434  http://***//hunyin/hunyinfagui/20110813143541_...          121
    2816  http://***//hunyin/hunyinfagui/201411053308986...          440
    2817  http://***//hunyin/hunyinfagui/201411053308986...          373
    2818  http://***//hunyin/hunyinfagui/201411053308986...          340
    2819  http://***//hunyin/hunyinfagui/201411053308986...          328
    6133  http://***//hunyin/jihuashengyu/20120215163891...          267
    6134  http://***//hunyin/jihuashengyu/20120215163891...          133

    """
    # 因为打印显示不完全再次替换
    temp_web_page_count['fullURL'] = temp_web_page_count['fullURL'].str.replace('hunyinfagui/', 'hyfg/',
                                                                                regex=True)
    temp_web_page_count['fullURL'] = temp_web_page_count['fullURL'].str.replace('jihuashengyu/', 'jhsy/',
                                                                                regex=True)

    temp_web_page_count['fullURL'] = temp_web_page_count['fullURL'].str.replace('jiaotong/', 'jt/',
                                                                                regex=True)
    temp_web_page_count['fullURL'] = temp_web_page_count['fullURL'].str.replace('laodong/', 'ld/',
                                                                                regex=True)
    print(temp_web_page_count)
    """
                                                    fullURL  click_times
    2732     http://***//hetong/ldht/201311152872128_2.html          377
    2733     http://***//hetong/ldht/201311152872128_3.html          218
    2734     http://***//hetong/ldht/201311152872128_4.html          146
    2735     http://***//hetong/ldht/201311152872128_5.html          122
    5917      http://***//hunyin/hyfg/20110813143541_2.html          172
    5918      http://***//hunyin/hyfg/20110813143541_3.html          121
    2984     http://***//hunyin/hyfg/201411053308986_2.html          440
    2985     http://***//hunyin/hyfg/201411053308986_3.html          373
    2986     http://***//hunyin/hyfg/201411053308986_4.html          340
    2987     http://***//hunyin/hyfg/201411053308986_5.html          328
    5965      http://***//hunyin/jhsy/20120215163891_2.html          267
    5966      http://***//hunyin/jhsy/20120215163891_3.html          133
    6321     http://***//hunyin/jhsy/201411053308990_2.html          143
    6757   http://***//jt/jtlawjtxgfg/20121011120700_2.html          103
    6926  http://***//jt/jtlawjtxgfg/201411273309942_2.html          158
    6925  http://***//jt/jtlawjtxgfg/201411273309942_3.html          377
    6185       http://***//jt/jtpcbz/201406193018102_2.html          110
    4621   http://***//ld/gsbxtiaoli/201408193306484_3.html          106
    7501     http://***//ld/ldzyjqdy/201411043308948_2.html          186
    4726      http://***//ld/ldzyjygl/20140312142061_2.html          173
    4727      http://***//ld/ldzyjygl/20140312142061_3.html          112
    1746      http://***//minshi/fagui/2013051382463_2.html          129
    1748      http://***//minshi/fagui/2013051382463_3.html          111
    1743      http://***//minshi/fagui/2013051382463_4.html          653
    1744      http://***//minshi/fagui/2013051382463_5.html          177
    1745      http://***//minshi/fagui/2013051382463_6.html          138
    1747      http://***//minshi/fagui/2013051382463_7.html          126

    """








