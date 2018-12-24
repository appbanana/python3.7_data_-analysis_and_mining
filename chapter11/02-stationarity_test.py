import pandas as pd
from statsmodels.tsa import stattools

if __name__ == '__main__':
    file_name = './temp/discdata_processed.xls'
    # file_name = './data/discdata_processed.xls'
    data = pd.read_excel(file_name)
    # print(data.head())

    # 最后5条数据作为验证数据
    train_data = data.iloc[:-5, :]
    test_data = data.iloc[-5:, :]
    print(test_data)
    # 平稳性检验
    diff = 0
    adf = stattools.adfuller(train_data['CWXT_DB:184:D:\\'])
    print(adf)
    # (-2.6460462274942986, 0.08384889634121945, 0, 41, {'1%': -3.60098336718852, '5%': -2.9351348158036012, '10%': -2.6059629803688282}, 958.701132117506)
    # adf[1]为pvalue的值
    while adf[1] >= 0.05:
        diff += 1
        adf = stattools.adfuller(train_data['CWXT_DB:184:D:\\'].diff(diff).dropna())

    print(u'原始序列经过%s阶差分后归于平稳，p值为%s' % (diff, adf[1]))
    # 原始序列经过1阶差分后归于平稳，p值为4.792591263393756e-07
