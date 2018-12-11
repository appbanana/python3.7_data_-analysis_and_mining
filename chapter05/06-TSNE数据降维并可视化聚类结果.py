import pandas as pd
from sklearn import manifold, cluster
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    file_name = './data/consumption_data.xls'
    out_file = 'temp.xls'
    # 读取数据
    data = pd.read_excel(file_name, index_col='Id')
    # 分三类
    k = 3
    # 最大循环次数 500次
    interation = 500
    # 零均值 数据标准化
    data_zs = (data - data.mean()) / data.std()
    model = cluster.KMeans(n_clusters=k, max_iter=interation, n_jobs=-1)
    model.fit(data_zs)
    # print(model.labels_)

    # tsne
    tsne = manifold.TSNE()
    tsne.fit_transform(data_zs)
    # print('****' * 5)
    # print(tsne.embedding_)
    tsne = pd.DataFrame(tsne.embedding_, index=data.index)
    tsne[u'聚类类别'] = pd.Series(model.labels_, index=data.index)
    # print(tsne.head())

    plt.figure(num=6)
    # 绘画
    d = tsne[tsne[u'聚类类别'] == 0]
    plt.plot(d[0], d[1], 'r.')

    d = tsne[tsne[u'聚类类别'] == 1]
    plt.plot(d[0], d[1], 'go')

    d = tsne[tsne[u'聚类类别'] == 2]
    plt.plot(d[0], d[1], 'b*')
    plt.savefig('{0}.png'.format('./img/Figure_6'))
    plt.show()

