import pandas as pd
from sqlalchemy import create_engine


def count107(j):
    # http://www.lawtime.cn/info/jiaotong  知识首页
    # http://www.lawtime.cn/info/jiaotong/jtlawdljtaqf/ 知识列表
    # http://www.lawtime.cn/info/laodonghetongfa/shishitiaoli/2008101130861.html 知识内容首页
    # 找出类别包含107的网址 [fullURL数组(1138 * 1)][bool值数组]
    j = j[['fullURL']][j['fullURLId'].str.contains('107')].copy()
    j['type'] = None  # 添加空列
    j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
    j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
    j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'

    return j['type'].value_counts()


def count101(p):
    p = p[['fullURLId']][p['fullURLId'].str.startswith('101')].copy()
    p['type'] = None  # 添加空列
    p['type'][p['fullURLId'].str.endswith('001')] = '101001'
    p['type'][p['fullURLId'].str.endswith('002')] = '101002'
    p['type'][p['fullURLId'].str.endswith('003')] = '101003'
    p['type'][~p['fullURLId'].str.contains('(001|002|003)')] = u'其他'

    return p['type'].value_counts()


def count_ask(p):
    p = p[['fullURLId']][p['fullURL'].str.contains('?', regex=False)].copy()
    return p['fullURLId'].value_counts()


def count_199(p):
    p = p[['fullURLId', 'pageTitle']][p['fullURL'].str.contains('?', regex=False)].copy()
    p = p[['pageTitle']][p['fullURLId'].str.contains('1999001')].copy()

    # p['type'] = None  # 添加空列
    # p['type'][p['pageTitle'].str.contains('法律快车-律师助手', na=False, regex=True)] = u'快车-法律助手'
    # p['type'][p['pageTitle'].str.contains('免费发布法律咨询', na=False, regex=True)] = u'免费发布法律咨询'
    # p['type'][p['pageTitle'].str.contains('咨询发布成功', na=False, regex=True)] = u'咨询发布成功'
    # p['type'][p['pageTitle'].str.contains('法律快搜', na=False, regex=True)] = u'法律快搜'
    # p['type'][~p['pageTitle'].str.contains('(法律快车-律师助手|免费发布法律咨询|咨询发布成功|法律快搜)', na=False, regex=True)] = u'其他类型'

    p['type'] = 1  # 添加空列
    p.loc[p['pageTitle'].str.contains('法律快车-律师助手', na=False, regex=True), 'type'] = u'快车-法律助手'
    p.loc[p['pageTitle'].str.contains('免费发布法律咨询', na=False, regex=True), 'type'] = u'免费发布法律咨询'
    p.loc[p['pageTitle'].str.contains('咨询发布成功', na=False, regex=True), 'type'] = u'咨询发布成功'
    p.loc[p['pageTitle'].str.contains('法律快搜', na=False, regex=True), 'type'] = u'法律快搜'
    p.loc[p['type'] == 1, 'type'] = u'其他类型'

    return p['type'].value_counts()

def count_199(p):
    p = p[['fullURLId', 'pageTitle']][p['fullURL'].str.contains('?', regex=False)].copy()
    p = p[['pageTitle']][p['fullURLId'].str.contains('1999001')].copy()

    # p['type'] = None  # 添加空列
    # p['type'][p['pageTitle'].str.contains('法律快车-律师助手', na=False, regex=True)] = u'快车-法律助手'
    # p['type'][p['pageTitle'].str.contains('免费发布法律咨询', na=False, regex=True)] = u'免费发布法律咨询'
    # p['type'][p['pageTitle'].str.contains('咨询发布成功', na=False, regex=True)] = u'咨询发布成功'
    # p['type'][p['pageTitle'].str.contains('法律快搜', na=False, regex=True)] = u'法律快搜'
    # p['type'][~p['pageTitle'].str.contains('(法律快车-律师助手|免费发布法律咨询|咨询发布成功|法律快搜)', na=False, regex=True)] = u'其他类型'

    p['type'] = 1  # 添加空列
    p.loc[p['pageTitle'].str.contains('法律快车-律师助手', na=False, regex=True), 'type'] = u'快车-法律助手'
    p.loc[p['pageTitle'].str.contains('免费发布法律咨询', na=False, regex=True), 'type'] = u'免费发布法律咨询'
    p.loc[p['pageTitle'].str.contains('咨询发布成功', na=False, regex=True), 'type'] = u'咨询发布成功'
    p.loc[p['pageTitle'].str.contains('法律快搜', na=False, regex=True), 'type'] = u'法律快搜'
    p.loc[p['type'] == 1, 'type'] = u'其他类型'

    return p['type'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # fullURLId 网址类型 然后分类统计个数
    # count_107 = [count107(i) for i in sql]
    #
    # count_107 = pd.concat(count_107).groupby(level=0).sum()
    #
    # count_107 = count_107.reset_index()
    # count_107.columns = ['type', 'num']
    # count_107['percent'] = count_107['num'] / count_107['num'].sum() * 100

    # print(count_107)
    """
        type     num    percent
    0  知识内容页  164243  89.799344
    1  知识列表页    9656   5.279388
    2   知识首页    9001   4.921268

    """

    # 注意:这里需要把107的数据的分类先注释掉，因为sql是一个生成器类型，所以在使用过一次以后，就不能继续使用了。必须要重新执行一次读取。
    # 咨询类别内部统计 101开头的
    # count_101 = [count101(m) for m in sql]
    # count_101 = pd.concat(count_101).groupby(level=0).sum()
    # count_101 = count_101.reset_index()
    # count_101.columns = ['type', 'num']
    # count_101 = count_101.sort_values(by=['num'], ascending=False)
    # count_101['percent'] = count_101['num'] / count_101['num'].sum() * 100
    #
    # print(count_101)
    """
         type     num    percent
    2  101003  396612  96.343386
    1  101002    7776   1.888915
    0  101001    5603   1.361058
    3      其他    1674   0.406641

    """
    # 带问号的类型统计
    # count_ask = [count_ask(m) for m in sql]
    # count_ask = pd.concat(count_ask).groupby(level=0).sum()
    # count_ask = count_ask.reset_index()
    # count_ask.columns = ['type', 'num']
    # count_ask = count_ask.sort_values(by=['num'], ascending=False)
    # count_ask['percent'] = count_ask['num'] / count_ask['num'].sum() * 100
    #
    # print(count_ask)
    """
          type    num    percent
    3  1999001  64718  98.818176
    4   301001    356   0.543578
    2   107001    346   0.528309
    0   101003     47   0.071764
    1   102002     25   0.038173

    """

    # 统计带有问号的网址中，其他(1999001)类型统计
    count_199 = [count_199(m) for m in sql]
    count_199 = pd.concat(count_199).groupby(level=0).sum()
    count_199 = count_199.reset_index()
    count_199.columns = ['type', 'num']
    count_199 = count_199.sort_values(by='num', ascending=False)
    count_199['percent'] = count_199['num'] / count_199['num'].sum() * 100
    print(count_199)
    """
           type    num    percent
    3   快车-法律助手  49894  77.094471
    0  免费发布法律咨询   6166   9.527488
    2    咨询发布成功   5220   8.065762
    4      法律快搜   1943   3.002256
    1      其他类型   1495   2.310022


    """
