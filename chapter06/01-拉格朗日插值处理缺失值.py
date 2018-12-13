import pandas as pd
from scipy import interpolate


def ployinterp_column(s, n, k=5):
    """
    自定义插值函数
    :param s: 列向量数据
    :param n: 被插值的位置
    :param k: 取出需要被插值前后数据的个数
    :return: 返回数据
    """

    # 取出缺失值前后k个数据
    y = s.reindex(list(range(n - k, n)) + list(range(n + 1, n + 1 + k)))
    # 剔除空的数据
    y = y[y.notna()]
    return interpolate.lagrange(y.index, list(y))(n)


def handle_missing_value(input_data):
    """
    预处理数据
    :param input_data: 输入的数据
    :return: 返回处理好的数据
    """
    for i in input_data.columns:
        for j in range(len(input_data)):
            if (input_data[i].isna())[j]:
                input_data[i][j] = ployinterp_column(input_data[i], j)
        input_data.to_excel('./temp.xls', header=None, index=False)
    return input_data


if __name__ == '__main__':
    file_name = './data/missing_data.xls'
    # 读取数据
    data = pd.read_excel(file_name, header=None)
    # 预处理数据
    data = handle_missing_value(data)

