import pandas as pd
from sklearn import cluster
import numpy as np

# import matplotlib.pyplot as plt
#
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


if __name__ == '__main__':
    file_name = './data/data.xls'
    core_data = pd.read_excel(file_name)
    typelabel = {u'肝气郁结证型系数': 'A', u'热毒蕴结证型系数': 'B', u'冲任失调证型系数': 'C',
                 u'气血两虚证型系数': 'D', u'脾胃虚弱证型系数': 'E', u'肝肾阴虚证型系数': 'F'}
    keys = list(typelabel.keys())
    result = pd.DataFrame()

    for i in range(len(keys)):
        # 建立模型 利用KMeans算法对每一列数据聚类离散化
        kmodel = cluster.KMeans(n_clusters=4, n_jobs=-1)
        # core_data[keys[i]].shape与core_data[[keys[i]]].shape 前者是一维数据  后者是二维数据
        kmodel.fit(core_data[[keys[i]]])
        print('******' * 10)
        # print(kmodel.cluster_centers_)
        value = typelabel[keys[i]]
        r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[value])
        r2 = pd.Series(kmodel.labels_).value_counts()
        r2 = pd.DataFrame(r2, columns=[value + 'n'])
        # 这样出来的数据并不是按照一定的顺序输出 还需要排序 eg:例如A数据
        # r = pd.concat([r1, r2], axis=1)
        """
                  A   An
            0  0.408679   53
            1  0.137643  244
            2  0.295406  278
            3  0.221225  355

        """
        # 按升序排列数据  下面的数据与上面数据对比就清楚了
        r = pd.concat([r1, r2], axis=1).sort_values(by=value)
        """
                  A   An
            3  0.137643  244
            0  0.220912  352
            2  0.295007  281
            1  0.408679   53

        """
        r.index = [1, 2, 3, 4]
        r[value] = r[value].rolling(2).mean()
        print(r)
        """
        1       NaN  240
        2  0.178698  356
        3  0.257724  281
        4  0.351843   53

        """
        # 此时还需把 NAN置位0
        r.loc[1, value] = 0.0
        """
                  A   An
        1  0.000000  240
        2  0.178698  356
        3  0.257724  281
        4  0.351843   53

        """
        result = result.append(r.T)
    print(result)
    """
            1           2           3           4
    A     0.0    0.179278    0.257960    0.351843
    An  244.0  352.000000  281.000000   53.000000
    B     0.0    0.147818    0.284702    0.450267
    Bn  316.0  391.000000  169.000000   54.000000
    C     0.0    0.202149    0.289061    0.423537
    Cn  297.0  394.000000  204.000000   35.000000
    D     0.0    0.172505    0.252279    0.359726
    Dn  283.0  379.000000  224.000000   44.000000
    E     0.0    0.152698    0.257873    0.376062
    En  273.0  319.000000  245.000000   93.000000
    F     0.0    0.179143    0.261386    0.354643
    Fn  200.0  237.000000  265.000000  228.000000

    """
    result.to_excel('./temp/data_processed.xls')
