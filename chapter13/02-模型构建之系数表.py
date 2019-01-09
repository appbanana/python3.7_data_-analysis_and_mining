import pandas as pd
from sklearn import linear_model


if __name__ == '__main__':
    file_name = './data/data1.csv'
    data = pd.read_csv(file_name)
    print(data)
    print(data.columns[:-1])

    model = linear_model.Lasso(alpha=1, max_iter=1000)
    model.fit(data.iloc[:, 0:13], data['y'])
    df = pd.DataFrame(model.coef_, index=data.columns[:-1])
    # print(model.coef_)
    """
    [-1.85085555e-04 -3.15519378e-01  4.32896206e-01 -3.15753523e-02
      7.58007814e-02  4.03145358e-04  2.41255896e-01 -3.70482514e-02
     -2.55448330e+00  4.41363280e-01  5.69277642e+00 -0.00000000e+00
     -3.98946837e-02]
    """

    print(df.T)
    """
         x1        x2        x3        x4        x5        x6        x7        x8        x9       x10       x11  x12       x13
    0 -0.000185 -0.315519  0.432896 -0.031575  0.075801  0.000403  0.241256 -0.037048 -2.554483  0.441363  5.692776 -0.0 -0.039895

    """