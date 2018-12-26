import pandas as pd
from sqlalchemy import create_engine

# mac上启动mariaDB mysql.server start
# mac上关闭mariaDB mysql.server stop
# 连接数据库 mysql -u root

if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
    sql = pd.read_sql('all_gzdata', engine, chunksize=1024 * 5)
    # fullURLId 网址类型 然后分类统计个数
    counts = [i['fullURLId'].value_counts() for i in sql]

    # 合并统计结果，把相同的统计项合并（即按index分组并求和）
    counts = pd.concat(counts).groupby(level=0).sum()
    # 重置index索引 生成一个新的DataFrame返回  注意与它counts.to_frame()的区别
    # reset_index官方参考地址 https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.reset_index.html?highlight=reset_index#pandas.Series.reset_index
    counts = counts.reset_index()
    """
          index  fullURLId
    0    101001       5603
    1    101002       7776
    2    101003     396612
    3    101004        125
    4    101005         63

    """

    # 重置列名
    counts.columns = ['index', 'num']
    """
          index     num
    0    101001    5603
    1    101002    7776
    2    101003  396612
    3    101004     125
    4    101005      63

    """

    # 在增加一列
    # 提取前三个数字作为类别id
    counts['type'] = counts['index'].str.extract('(\d{3})')
    # print('****' * 10)
    # print(counts)
    """
          index     num type
    0    101001    5603  101
    1    101002    7776  101
    2    101003  396612  101
    3    101004     125  101
    4    101005      63  101

    """

    # # 按类别合并
    counts_ = counts.groupby(by='type').sum()
    counts_ = counts_.sort_values(by=['num'], ascending=False)
    counts_ = counts_.reset_index()
    counts_['percent'] = (counts_['num'] / counts_['num'].sum()) * 100

    # print('****' * 10)
    print(counts_)
    """
      type     num    percent
    0  101  411665  49.156965
    1  199  201426  24.052302
    2  107  182900  21.840110
    3  301   18430   2.200728
    4  102   17357   2.072601
    5  106    3957   0.472506
    6  103    1715   0.204788

    """
