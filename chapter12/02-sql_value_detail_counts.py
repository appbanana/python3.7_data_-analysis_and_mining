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
    p = j[['fullURLId']][p['fullURLId'].str.startswith('101')].copy()
    p['type'] = None  # 添加空列
    p['type'][p['fullURLId'].str.endswith('001')] = '101001'
    p['type'][p['fullURLId'].str.endswith('002')] = '101002'
    p['type'][p['fullURLId'].str.endswith('003')] = '101003'
    p['type'][~p['fullURLId'].str.contains('(001|002|003)')] = u'其他'

    return p['type'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)

    # fullURLId 网址类型 然后分类统计个数
    count_107 = [count107(i) for i in sql]

    count_107 = pd.concat(count_107).groupby(level=0).sum()

    count_107 = count_107.reset_index()
    count_107.columns = ['type', 'num']
    count_107['percent'] = count_107['num'] / count_107['num'].sum() * 100

    print(count_107)
    """
        type     num    percent
    0  知识内容页  164243  89.799344
    1  知识列表页    9656   5.279388
    2   知识首页    9001   4.921268

    """

    # 咨询类别内部统计 101开头的
    # print(len(list(sql)))
    # count_101 = [count101(m) for m in sql]
    # print('********count_101************')
    # print(count_101)
    # count_101 = pd.concat(count_101).groupby(level=0).sum()
    # print(count_101)
