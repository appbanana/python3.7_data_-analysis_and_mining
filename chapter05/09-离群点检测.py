import pandas as pd
import numpy as np
from sklearn import cluster
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    file_name = './data/consumption_data.xls'
    data = pd.read_excel(file_name, index_col='Id')
    # print(data.head())

    # 零均值标准化数据
    data_zs = (data - data.mean()) / data.std()

    # KMeans 聚类
    k = 3
    # 离群点阈值
    threshold = 2
    model = cluster.KMeans(n_clusters=k, max_iter=500, n_jobs=-1)
    model.fit(data_zs)
    data_zs[u'聚类类别'] = model.labels_

    # print(data_zs)
    # print(model.labels_)
    norm = []
    for i in range(k):
        norm_temp = data_zs[['R', 'F', 'M']][data_zs[u'聚类类别'] == i] - model.cluster_centers_[i]
        # 求出绝对距离
        norm_temp = norm_temp.apply(np.linalg.norm, axis=1)
        # 求相对距离
        norm.append(norm_temp / norm_temp.median())
    norm = pd.concat(norm)
    # 正常点
    norm[norm <= threshold].plot(style='go')

    discrete_points = norm[norm > threshold]
    discrete_points.plot(style='bo')
    for i in range(len(discrete_points)):
        id = discrete_points.index[i]
        point = discrete_points.iloc[i]
        plt.annotate('(%s, %.2f)' % (id, point), xy=(id, point), xytext=(id + 10, point - 0.1))
    plt.savefig('{0}.png'.format('./img/Figure_9'))
    plt.xlabel(u'编号')
    plt.ylabel(u'相对距离')
    plt.show()
    print(norm)
