import pandas as pd
# import numpy as np
from sqlalchemy import create_engine


def handle_data(p):
    p = p.copy()
    p['type'] = 1  # 添加空列
    p.loc[p['fullURL'].str.contains('ask', na=False, regex=True), 'type'] = u'咨询类'
    # 含有zhishi faguizt /info/ 都是知识类型的
    p.loc[p['fullURL'].str.contains('(zhishi)|(faguizt)|(\/info\/)', na=False, regex=True), 'type'] = u'知识类'
    p.loc[p['type'] == 1, 'type'] = u'其他类型'
    return p['type'].value_counts()


def handle_web_data(p):
    p = p[['realIP', 'fullURL']].copy()
    # 打第一个标签 zhishi zixun
    p['type1'] = None
    p.loc[p['fullURL'].str.contains('(zhishi)|(faguizt)|(\/info\/)', na=False, regex=True), 'type1'] = 'zhishi'
    p.loc[p['fullURL'].str.contains('ask', na=False, regex=True), 'type1'] = 'zixun'

    # 接着打第二标签
    p['type2'] = None
    p['type3'] = None

    # 主要处理第一标签为zhishi类的
    # 处理info类的
    temp_type2_1 = p['fullURL'].str.extract('/info/(.*?)/(.*?)/')
    # 处理zhishiku的 已经查看过 info类和zhishiku类这两个没有交集
    temp_type2_2 = p['fullURL'].str.extract('/zhishiku/(.*?)/(.*?)/')

    # 接着temp_type2_1和temp_type2_2开始合并 demo 详见10-test.py
    temp_type2_1[temp_type2_2[0].notna()] = temp_type2_2[temp_type2_2[0].notna()]
    temp_type2_1[temp_type2_2[1].notna()] = temp_type2_2[temp_type2_2[1].notna()]

    p['type2'] = temp_type2_1[0]
    p['type3'] = temp_type2_1[1]

    return p


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
    sql = pd.read_sql('cleaned_gzdata_one', engine, chunksize=1024 * 5)
    result = [handle_data(i) for i in sql]
    df_result = pd.concat(result).reset_index()
    df_result.columns = [u'类型', u'数量']

    # 分组统计求和
    df_result = df_result.groupby(by=[u'类型']).sum()
    df_result = df_result.reset_index()

    df_result[u'百分比'] = df_result[u'数量'] / df_result[u'数量'].sum() * 100
    print(df_result)
    """
         类型      数量        百分比
    0  其他类型  117322  22.085014
    1   咨询类  392196  73.828048
    2   知识类   21711   4.086938

    """

    # 网页分类表
    sql = pd.read_sql('cleaned_gzdata_one', engine, chunksize=1024 * 5)
    result = [handle_web_data(i) for i in sql]
    web_type_result = pd.concat(result)
    web_type_result = web_type_result.sort_values(by=['realIP', 'fullURL'])
    web_type_result['fullURL'] = web_type_result['fullURL'].str.replace('www.lawtime.cn', '***', regex=True)
    # 写入数据库 方便查看
    web_type_result.to_sql('cleaned_type_data', engine, index=False, if_exists='append')
    print(web_type_result)

    """
                  realIP                                            fullURL   type1       type2             type3
    2364       82033               http://***/ask/question_3565164.html   zixun         NaN               NaN
    1005       82033      http://***/info/shuifa/zzs/2012010776727.html  zhishi      shuifa               zzs
    4283       95502               http://***/ask/question_7882607.html   zixun         NaN               NaN
    1328      103182               http://***/ask/question_7174864.html   zixun         NaN               NaN
    5020      116010  http://***/info/hunyin/lhlawlhxy/2011070713769...  zhishi      hunyin         lhlawlhxy
    2366      136206               http://***/ask/question_8246285.html   zixun         NaN               NaN
    680       140151  http://***/info/gongsi/slbgfgs/2011012596695.html  zhishi      gongsi           slbgfgs
    ...
    """