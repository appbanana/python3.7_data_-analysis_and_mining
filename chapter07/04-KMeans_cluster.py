import pandas as pd
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


def print_cluster_result(data, kmodel):
    # 统计各个类别的数目
    r1 = pd.Series(kmodel.labels_).value_counts()
    r2 = pd.DataFrame(kmodel.cluster_centers_)
    # 重新组合数据
    r = pd.concat([r2, r1], axis=1)
    # 添加表头
    r.columns = list(data.columns) + [u'类别数目']
    # print(r1)
    # print('****' * 10)
    # print(r2)
    print('****' * 10)
    print(r)
    """
             ZL        ZR        ZF        ZM        ZC   类别数目
        0  0.051752 -0.002774 -0.230839 -0.235029  2.177490   4232
        1  1.160380 -0.377414 -0.087010 -0.095018 -0.158447  15729
        2  0.483476 -0.799418  2.482365  2.423564  0.309430   5340
        3 -0.314116  1.686625 -0.573863 -0.536616 -0.172432  12120
        4 -0.700787 -0.415137 -0.160762 -0.160497 -0.256659  24623
    """


def plot_cluster(data, kmodel):
    # 标签
    labels = data.columns
    # 5组数据
    k = 5
    plot_data = kmodel.cluster_centers_
    # print(plot_data)
    # 指定颜色
    colors = ['b', 'g', 'r', 'c', 'y']

    angles = np.linspace(0, 2 * np.pi, k, endpoint=False)
    print('*****' * 10)
    print(angles)
    # 组成闭合的数据
    plot_data = np.concatenate((plot_data, plot_data[:, [0]]), axis=1)
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i in range(len(plot_data)):
        ax.plot(angles, plot_data[i], 'o-', color=colors[i], linewidth=2, label=u'客户群' + str(i+1), )
    ax.set_rgrids(np.arange(0.01, 3.5, 0.5), np.arange(-1, 2.5, 0.5), fontproperties="SimHei")
    ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties="SimHei")
    # plt.savefig('{0}.png'.format('./img/Figure_04'))
    plt.legend(loc=0)
    plt.show()


if __name__ == '__main__':
    file_name = './temp/core_data.xls'
    core_data = pd.read_excel(file_name)

    # 建立模型
    model = cluster.KMeans(n_clusters=5, n_jobs=-1)
    model.fit(core_data)
    print_cluster_result(core_data, model)
    plot_cluster(core_data, model)
