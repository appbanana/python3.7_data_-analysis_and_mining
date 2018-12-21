import pandas as pd
from sqlalchemy import create_engine


def count107(j):
    # http://www.lawtime.cn/info/jiaotong  知识首页
    # http://www.lawtime.cn/info/jiaotong/jtlawdljtaqf/ 知识列表
    # http://www.lawtime.cn/info/laodonghetongfa/shishitiaoli/2008101130861.html 知识内容首页
    # 找出类别包含107的网址 [fullURL数组(1138 * 1)][bool值数组]
    j = j[['fullURL']][j['fullURLId'].str.contains('107')].copy()
    j['type'] = None  # 添加空列
    # j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
    # j['type'][j['fullURL'].str.contains('info/.+/.+?/')] = u'知识列表页'
    # j['type'][j['fullURL'].str.contains('/\d+(_?).html')] = u'知识内容页'

    j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
    j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
    j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'

    return j['type'].value_counts()


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    # fullURLId 网址类型 然后分类统计个数
    counts = [count107(i) for i in sql]
    counts = pd.concat(counts).groupby(level=0).sum()

    print(counts)
