import pandas as pd
from scipy import interpolate

def ployinterp_column(s, n, k=5):
    """
    自定义插值函数
    :param s: 待测数据
    :param n: 异常值的下标
    :param k: k为前后数据的个数
    :return: 返回正常的竖直
    """
    y = s[list(range(n - k, n)) + list(range(n, n + k))]
    # 把空的值踢出去 只要非空值
    y = y[y.notnull()]
    return interpolate.lagrange(y.index, list(y))(n)


if __name__ == '__main__':
    file_path = './data/catering_sale.xls'
    sale_data = pd.read_excel(file_path)
    # 取出销量位于400~5000的数据
    # print(sale_data[(sale_data[u'销量'] > 400) & (sale_data[u'销量'] < 5000)])
    # 将异常数据变为空值
    sale_data[u'销量'][(sale_data[u'销量'] < 400) | (sale_data[u'销量'] > 5000)] = None
    print(sale_data.head())
    
    for i in sale_data.columns:
        for j in range(len(sale_data)):
            # pd.Index([5.2, 6.0, None]).isna() => array([False, False,  True], dtype=bool)
            # 找出空值的位置
            if sale_data[i].isna()[j]:
                # 如果为空进项拉格朗日插值
                sale_data[i][j] = ployinterp_column(sale_data[i], j)

    print('-----*****------' * 3)
    print(sale_data.head())
    # 保存数据
    sale_data.to_excel('./temp.xls')
