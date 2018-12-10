import pandas as pd
from sklearn import linear_model

if __name__ == '__main__':
    file_path = './data/bankloan.xls'
    bank_data = pd.read_excel(file_path)
    # print(bank_data.head())
    """
       年龄  教育  工龄  地址   收入   负债率      信用卡负债      其他负债  违约
    0  41   3  17  12  176   9.3  11.359392  5.008608   1
    1  27   1  10   6   31  17.3   1.362202  4.000798   0
    2  40   1  15  14   55   5.5   0.856075  2.168925   0
    3  41   1  15  14  120   2.9   2.658720  0.821280   0
    4  24   2   2   0   28  17.3   1.787436  3.056564   1

    """
    X = bank_data.iloc[:, :8]
    y = bank_data.iloc[:, 8]
    # 建立逻辑回归模型 帅选变量 RandomizedLogisticRegression 即将在0.21中弃掉
    rlr = linear_model.RandomizedLogisticRegression()
    # 训练模型
    rlr.fit(X, y)
    print(u'有效特征:%s' % ','.join(bank_data.columns[0:-1][rlr.get_support()]))

    # 建立逻辑货柜模型
    # penalty='l2', n_jobs=-1, solver='sag'
    lr = linear_model.LogisticRegression(solver='lbfgs')
    X = bank_data[bank_data.columns[0:-1][rlr.get_support()]]
    lr.fit(X, y)
    # (700, 4)
    print(X.shape)
    # 模型的平均正确率: 0.8142857142857143
    print(u'模型的平均正确率:%s' % lr.score(X, y))

