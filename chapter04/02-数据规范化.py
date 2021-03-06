import pandas as pd
import numpy as np

if __name__ == '__main__':
    file_path = './data/normalization_data.xls'
    data = pd.read_excel(file_path, header=None)
    print(data.head())
    # 最小~最大值规范话
    min_max_data = (data - data.min()) / (data.max() - data.min())
    print(min_max_data)
    """
              0         1         2         3
        0  0.074380  0.937291  0.923520  1.000000
        1  0.619835  0.000000  0.000000  0.850941
        2  0.214876  0.119565  0.813322  0.000000
        3  0.000000  1.000000  1.000000  0.563676
        4  1.000000  0.942308  0.996711  0.804149
        5  0.264463  0.838629  0.814967  0.909310
        6  0.636364  0.846990  0.786184  0.929571

    """
    # 零均值标准化
    mean_data = (data - data.mean()) / data.std()
    print('*********' * 5)
    print(mean_data)
    """
              0         1         2         3
        0 -0.905383  0.635863  0.464531  0.798149
        1  0.604678 -1.587675 -2.193167  0.369390
        2 -0.516428 -1.304030  0.147406 -2.078279
        3 -1.111301  0.784628  0.684625 -0.456906
        4  1.657146  0.647765  0.675159  0.234796
        5 -0.379150  0.401807  0.152139  0.537286
        6  0.650438  0.421642  0.069308  0.595564

    """
    # 小数定标标准化
    temp_data = data / 10 ** np.ceil(np.log10(data.abs().max()))
    print('*********' * 5)
    print(temp_data)
    """
           0      1      2       3
        0  0.078  0.521  0.602  0.2863
        1  0.144 -0.600 -0.521  0.2245
        2  0.095 -0.457  0.468 -0.1283
        3  0.069  0.596  0.695  0.1054
        4  0.190  0.527  0.691  0.2051
        5  0.101  0.403  0.470  0.2487
        6  0.146  0.413  0.435  0.2571

    """