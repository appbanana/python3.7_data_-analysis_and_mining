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
    # adf[1]为pvalue的值
    while adf[1] >= 0.05:
        diff += 1
        adf = stattools.adfuller(train_data['CWXT_DB:184:D:\\'].diff(diff).dropna())

    print(u'原始序列经过%s阶差分后归于平稳，p值为%s' % (diff, adf[1]))
