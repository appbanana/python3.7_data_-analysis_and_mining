import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy

if __name__ == '__main__':
    file_name = './temp/standardized.xls'
    data = pd.read_excel(file_name, index_col=u'基站编号')

    Z = hierarchy.linkage(data, method='ward', metric='euclidean')
    p = hierarchy.dendrogram(Z, 0)
    plt.savefig('{0}.png'.format('./img/Figure_02'))

    plt.show()
