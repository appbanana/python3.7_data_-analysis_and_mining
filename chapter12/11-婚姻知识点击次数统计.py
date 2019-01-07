import pandas as pd
from sqlalchemy import create_engine


def handle_data(p):
    p = p.copy()
    # 筛选出来 标签包含婚姻的数据
    p = p[p['type2'].str.contains('hunyin') | p['type3'].str.contains('hunyin')]
    return p


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
    sql = pd.read_sql('cleaned_type_data', engine, chunksize=1024 * 5)
    result = [handle_data(i) for i in sql]
    # df_result.shape (16606, 5)
    df_result = pd.concat(result)
    # 写入婚姻数据 以方便使用
    df_result.to_sql('hunyin_data', engine, index=False, if_exists='append')

    # print(df_result)

    # 统计网址被点击从次数
    web_click_result = df_result['fullURL'].value_counts()
    web_click_result = web_click_result.reset_index()
    web_click_result.columns = ['fullURL', 'times']
    # 按次数分割数据 pd.cut具体查看官网https://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html?highlight=cut
    web_click_cut = pd.cut(web_click_result['times'], bins=[0, 1, 2, 3, 4, 5000], labels=['1', '2', '3', '4', '5~5000'])
    web_click_result['range'] = web_click_cut
    # web_click_cut = pd.DataFrame(web_click_cut)
    # print(web_click_result)
    """
                                                fullURL  times   range
    0     http://***/info/hunyin/lhlawlhxy/2011070713769...   3507  5~5000
    1     http://***/info/hunyin/hunyinfagui/20141105330...    509  5~5000
    2     http://***/info/hunyin/jihuashengyu/2012021516...    457  5~5000
    3     http://***/info/hunyin/jihuashengyu/2014110533...    211  5~5000
    4     http://***/info/hunyin/jiehun/hunjia/201109201...    192  5~5000
    5     http://***/info/hunyin/hunyinfagui/20110813143...    190  5~5000

    """
    # 统计各个阶段内次数的统计
    web_group_result = web_click_result['range'].value_counts(sort=False)
    # web_group_result = pd.DataFrame(web_group_result)
    # web_group_result.index.name = '点击次数'
    web_group_result = web_group_result.reset_index()
    web_group_result.columns = [u'点击次数', u'网页个数']
    web_group_result[u'网页百分比'] = web_group_result[u'网页个数'] / web_group_result[u'网页个数'].sum() * 100
    print(web_group_result)
    """
         点击次数  网页个数      网页百分比
    0       1  2734  63.097161
    1       2   750  17.309024
    2       3   280   6.462036
    3       4   150   3.461805
    4  5~5000   419   9.669975

    """

    # 上面数据还差两个数据 接下来统计记录数
    # 和并数据
    print('*******' * 10)
    merge_data = pd.merge(df_result, web_click_result, on='fullURL', how='left')
    # print(merge_data)
    """
               realIP                                            fullURL   type1   type2          type3  times   range
    0          116010  http://***/info/hunyin/lhlawlhxy/2011070713769...  zhishi  hunyin      lhlawlhxy   3507  5~5000
    1          418673  http://***/info/hunyin/lihunfangchan/201103101...  zhishi  hunyin  lihunfangchan      1       1
    2         1393009  http://***/info/hunyin/hunyinfagui/20110813143...  zhishi  hunyin    hunyinfagui    190  5~5000
    3         1675790  http://***/info/hunyin/jihuashengyu/2012021516...  zhishi  hunyin   jihuashengyu    457  5~5000
    4         1885994  http://***/info/hunyin/lihunfangchan/201012218...  zhishi  hunyin  lihunfangchan      4       4

    """
    web_group_result[u'记录数'] = [merge_data[merge_data['times'] == 1].shape[0],
                                merge_data[merge_data['times'] == 2].shape[0],
                                merge_data[merge_data['times'] == 3].shape[0],
                                merge_data[merge_data['times'] == 4].shape[0],
                                merge_data[merge_data['times'] > 4].shape[0]]
    # print(web_group_result)
    """
             点击次数  网页个数      网页百分比    记录数
    0       1  2734  63.097161   2734
    1       2   750  17.309024   1500
    2       3   280   6.462036    840
    3       4   150   3.461805    600
    4  5~5000   419   9.669975  10932

    """
    web_group_result[u'记录百分比'] = web_group_result[u'记录数'] / web_group_result[u'记录数'].sum() * 100
    print(web_group_result)
    """
         点击次数  网页个数      网页百分比    记录数      记录百分比
    0       1  2734  63.097161   2734  16.463929
    1       2   750  17.309024   1500   9.032880
    2       3   280   6.462036    840   5.058413
    3       4   150   3.461805    600   3.613152
    4  5~5000   419   9.669975  10932  65.831627

    """