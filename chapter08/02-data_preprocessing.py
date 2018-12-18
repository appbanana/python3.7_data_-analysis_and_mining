import copy
import pandas as pd
from sklearn import cluster

if __name__ == '__main__':
    file_name = './data/data.xls'
    core_data = pd.read_excel(file_name)
    copy_data = copy.deepcopy(core_data)
    typelabel = {u'肝气郁结证型系数': 'A', u'热毒蕴结证型系数': 'B', u'冲任失调证型系数': 'C',
                 u'气血两虚证型系数': 'D', u'脾胃虚弱证型系数': 'E', u'肝肾阴虚证型系数': 'F'}
    keys = list(typelabel.keys())
    result = pd.DataFrame()

    for i in range(len(keys)):
        # 建立模型 利用KMeans算法对每一列数据聚类离散化
        kmodel = cluster.KMeans(n_clusters=4, n_jobs=-1)
        # core_data[keys[i]].shape与core_data[[keys[i]]].shape 前者是一维数据  后者是二维数据
        kmodel.fit(core_data[[keys[i]]])
        value = typelabel[keys[i]]
        r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[value])
        r2 = pd.Series(kmodel.labels_).value_counts()
        temp = map(lambda x: value + str(x + 1), kmodel.labels_)
        copy_data[keys[i]] = list(temp)

    print(copy_data)
    copy_data.to_csv('./temp/apriori.txt', index=False)
