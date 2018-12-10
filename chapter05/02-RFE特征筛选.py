import pandas as pd
from sklearn import linear_model
from sklearn import feature_selection

if __name__ == '__main__':
    file_path = './data/bankloan.xls'
    bank_data = pd.read_excel(file_path)
    X = bank_data.iloc[:, :-1]
    y = bank_data.iloc[:, -1]

    lr = linear_model.LogisticRegression()
    selector = feature_selection.RFE(lr, step=1)
    selector.fit(X, y)
    print('***11111**' * 5)
    print(u'有效特征:%s' % ','.join(bank_data.columns[0:-1][selector.support_]))
    print('*****' * 5)
    print(u'模型的平均正确率:%s' % selector.score(X, y))
    print('*****' * 5)
    print(selector.support_)
    print('*****' * 5)
    print(selector.n_features_)
    print('*****' * 5)
    print(selector.estimator_)
    print('*****' * 5)
    print(selector.ranking_)
    """
    ***11111*****11111*****11111*****11111*****11111**
    有效特征:工龄,地址,负债率,信用卡负债
    *************************
    模型的平均正确率:0.8142857142857143
    *************************
    [False False  True  True False  True  True False]
    *************************
    4
    *************************
    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='warn',
              n_jobs=None, penalty='l2', random_state=None, solver='warn',
              tol=0.0001, verbose=0, warm_start=False)
    *************************
    [4 2 1 1 5 1 1 3]

    """


