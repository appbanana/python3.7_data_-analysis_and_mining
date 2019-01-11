import pandas as pd
from matplotlib import pyplot as plt
from sklearn import cluster

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


if __name__ == '__main__':
    file_name = './temp/standardized.xls'
    data_df = pd.read_excel(file_name, index_col=u'基站编号')

    k = 3
    model = cluster.AgglomerativeClustering(n_clusters=k)
    model.fit(data_df)
    # 实际上就是添加一列，这一列用来标识它是哪一类别
    data = pd.concat([data_df, pd.Series(model.labels_, index=data_df.index)], axis=1)
    # data.columns = list(data_df.columns) + [u'聚类类别']
    data.columns = [u'工作日人均停留时间', u'凌晨人均停留时间', u'周末人均停留时间', u'日均人流量', u'聚类类别']
    print(data.head())
    """
       工作日上班时间人均停留时间  凌晨人均停留时间  周末人均停留时间     日均人流量  聚类类别
    基站编号                                                    
    36902       0.103865  0.856364  0.850539  0.169153     1
    36903       0.263285  1.000000  0.725732  0.118210     1
    36904       0.144928  0.740000  0.644068  0.038909     1
    36905       0.082126  0.992727  0.993837  0.020031     1
    36906       0.374396  0.867273  0.987673  0.102217     1


    """

    styles = ['ro-', 'go-', 'bo-']
    features = [u'工作日人均停留时间', u'凌晨人均停留时间', u'周末人均停留时间', u'日均人流量']
    for i in range(k):
        # 取出对应类别的数据
        temp_data = data[data[u'聚类类别'] == i][features]
        for j in range(len(temp_data)):
            plt.plot(range(1, 5), temp_data.iloc[j], styles[i])
        plt.xticks(ticks=range(1, 5), labels=features)
        # temp_data[features].plot(style=styles[i])
        plt.savefig('{0}_{1}.png'.format('./img/Figure_03', str(i+1)))
        plt.show()

    # Z = hierarchy.linkage(data, method='ward', metric='euclidean')
    # p = hierarchy.dendrogram(Z, 0)
    # plt.savefig('{0}.png'.format('./img/Figure_02'))
    #
    # plt.show()
