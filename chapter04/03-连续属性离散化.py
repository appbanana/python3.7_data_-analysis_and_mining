import pandas as pd
from sklearn import cluster
import numpy as np
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


def equal_width(input_data, bins, labels=None):
    """
    等宽离散化
    :param data: 待分离的数据
    :param bins: 参考pd.cut参数的bins
    :param labels: 参考pd.cut参数的labels
    :return: 返回数据
    """
    """
        x 必须是一位数组 eg:data.iloc[:, 0]与data[u'肝气郁结证型系数'] 代表同一个意思
        bins 可以是一个区间的list eg：bins=[0, 100, 200, 300]，也可以是一个int，eg:3代表等宽的区间的数量
        labels
    """
    # 等宽离散化 等宽分成4个区间
    result_data = pd.cut(x=input_data, bins=bins, labels=labels)
    return result_data


def equal_frequency(input_data, num):
    # 等频离散化 每个区间内的元素个数相等
    w = [1.0 * i / num for i in range(num + 1)]
    # percentiles 默认为[.25, .5, .75] 只有上四分位 中位 下四分位 现在相当于增加了0分位 100分位
    w = input_data.describe(percentiles=w)
    # print(w)
    """
             肝气郁结证型系数
        count  930.000000
        mean     0.232154
        std      0.078292
        min      0.026000
        0%       0.026000
        25%      0.176250
        50%      0.231000
        75%      0.281750
        100%     0.504000
        max      0.504000

    """
    # 取出分位数的值
    w = w[4:4 + num + 1]
    # print(w)
    """
          肝气郁结证型系数
    0%     0.02600
    25%    0.17625
    50%    0.23100
    75%    0.28175
    100%   0.50400

    """
    w.iloc[0] = w.iloc[0] * (1 - 1e-10)
    return pd.cut(x=input_data.iloc[:, 0], bins=w[u'肝气郁结证型系数'], labels=range(num))


def cluster_analysis(input_data, num):
    # 建立模型 n_jobs一般等于cpu数比较好， -1为使用所有的处理器，开足马力工作
    kModel = cluster.KMeans(n_clusters=num, n_jobs=-1)
    kModel.fit(np.array(input_data).reshape((len(input_data), 1)))
    cluster_centers = pd.DataFrame(kModel.cluster_centers_).sort_values(by=0)
    # print(cluster_centers)
    # 滚动窗口每两项求平均值 见下面输出值
    w = cluster_centers.rolling(window=2).mean()
    print(w)
    """
              0
    2  0.136954
    1  0.220441
    0  0.295007
    3  0.408679
    
              0
    2       NaN
    1  0.178698
    0  0.257724
    3  0.351843

    """
    # 过滤掉第一项 因为第一项为空值
    w = w.iloc[1:, :]
    # 将首末边界加上去
    w = [0] + list(w[0]) + [input_data.max()]
    return pd.cut(x=input_data.iloc[:, 0], bins=w, labels=range(num))


def cluster_plot(d, num):
    plt.figure(num='聚类分析离散化', figsize=(8, 3))
    """
    有一点需要注意的就是 data和d的维度不一样  下面是我打印的结果 data是二维数组 d为一维数组
    把d转置一下就可以输出了 
    ******************************************************
    (112, 1) (112,)
    ******************************************************
    (508, 1) (508,)
    ******************************************************
    (275, 1) (275,)
    ******************************************************
    (35, 1) (35,)

    """
    for j in range(0, num):
        # print('*********' * 6)
        # print(data[d == j].shape, d[d == j].shape)
        # 这句应该是书中写错了
        # plt.plot(data[d == j], [i for i in d[d == j]], 'o')
        temp = d[d == j]
        # x 为excel中肝气郁结证型系数 y为你对数据的标记的label 其实就是 0, 1, 2, 3
        plt.plot(data[d == j], np.array(temp).reshape(len(temp), 1), 'o')
    plt.ylim(-0.5, num - 0.5)
    plt.title('聚类分析离散化')
    return plt


if __name__ == '__main__':
    file_path = './data/discretization_data.xls'
    data = pd.read_excel(file_path)
    # print(data.head())
    # print(data[u'肝气郁结证型系数'])
    k = 4
    # 等宽离散化
    d1 = equal_width(input_data=data[u'肝气郁结证型系数'], bins=k, labels=range(k))
    # print(d1)
    # plt = cluster_plot(d1, k)
    # plt.show()

    # 等频离散化
    d2 = equal_frequency(input_data=data, num=k)
    plt = cluster_plot(d2, num=k)
    plt.show()

    # 基于聚类对数据进行离散化
    # result = cluster_analysis(input_data=data, num=k)
    # print(result)
