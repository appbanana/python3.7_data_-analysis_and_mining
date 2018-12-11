import pandas as pd
from sklearn import cluster
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


def density_plot(input_data):
    plt.figure()
    # for i in range(len(input_data.columns)):
    #     column_name = input_data.columns[i]
    #     input_data[column_name].plot(kind='kde', linewidth=2, label=column_name)
    input_data.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    plt.ylabel(u'密度')
    # plt.xlabel(u'人数')
    # plt.title(u'聚类类别%s各属性的密度曲线' % title)
    plt.legend()
    plt.grid()
    return plt


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

    # 简单打印结果
    # 统计各个类别的数目
    r1 = pd.Series(model.labels_).value_counts()
    r2 = pd.DataFrame(model.cluster_centers_)
    r = pd.concat([r2, r1], axis=1)
    r.columns = list(data.columns) + [u'聚类类别']
    # print(r)
    """
              R         F         M  聚类类别
    0 -0.160451  1.114802  0.392844   341
    1 -0.149353 -0.658893 -0.271780   559
    2  3.455055 -0.295654  0.449123    40

    """

    # 详细输出原始数据及其类别
    new_data = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)
    # Index(['R', 'F', 'M', '聚类类别'], dtype='object')
    new_data.columns = list(data.columns) + [u'聚类类别']

    # print(new_data[u'聚类类别'].head() == 2)

    print(new_data.head())
    """
    Id      R   F        M   聚类类别                     
    1    27   6   232.61  1
    2     3   5  1507.11  1
    3     4  16   817.62  2
    4     3  11   232.81  1
    5    14   7  1913.05  1

    """
    new_data.to_excel(out_file)

    # 遍历这个三个类别
    for i in range(k):
        # 取出每个类别的下的数据  聚类类别:0, 1, 2
        temp_data = new_data[new_data[u'聚类类别'] == i]
        # 这要注意 这用的是data.columns  不是new_data.columns
        for j in range(len(data.columns)):
            # 取出对应类别下 列的数据 绘图 保存
            column_name = data.columns[j]
            # pd_类别_列名 eg: pd_0_R， pd_0_M
            density_plot(temp_data[column_name]).savefig('{0}{1}{2}.png'.format('./img/pd_', i, '_' + column_name))
