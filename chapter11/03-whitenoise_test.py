import pandas as pd
from statsmodels.stats import diagnostic

if __name__ == '__main__':
    file_name = './temp/discdata_processed.xls'
    # file_name = './data/discdata_processed.xls'
    data = pd.read_excel(file_name)
    # print(data.head())

    # 最后5条数据作为验证数据
    train_data = data.iloc[:-5, :]
    test_data = data.iloc[-5:, :]
    # print(test_data)

    # 白噪声检验
    # (array([19.51936427]), array([9.95850373e-06]))
    ([lb], [p]) = diagnostic.acorr_ljungbox(train_data['CWXT_DB:184:D:\\'], lags=1)
    diff = 0
    while p >= 0.05:
        diff = diff + 1
        ([lb], [p]) = diagnostic.acorr_ljungbox(train_data['CWXT_DB:184:D:\\'].diff(diff).dropna(), lags=1)

    # print(result)
    print(u'原始序列经过%s阶差分后归于平稳，p值为%s' % (diff, p))
