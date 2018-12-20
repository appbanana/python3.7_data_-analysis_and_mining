import pandas as pd
import numpy as np
from statsmodels.tsa import arima_model

if __name__ == '__main__':
    file_name = './temp/discdata_processed.xls'
    # file_name = './data/discdata_processed.xls'
    data = pd.read_excel(file_name, index_col='COLLECTTIME')
    print(data.head())

    # 最后5条数据作为验证数据
    train_data = data.iloc[:-5, :]
    test_data = data.iloc[-5:, :]
    # print(test_data)

    # 定阶
    pmax = len(train_data['CWXT_DB:184:D:\\']) // 10
    qmax = len(train_data['CWXT_DB:184:D:\\']) // 10
    bic_matrix = []
    for p in range(pmax):
        temp = []
        for q in range(qmax):
            try:
                result = arima_model.ARIMA(train_data['CWXT_DB:184:D:\\'], (p, 1, q)).fit().bic
                # result if np.isnan(result) else None
                temp.append(None if pd.isna(result) else result)
                # temp.append(result)
            except:
                temp.append(None)
        bic_matrix.append(temp)

    bic_matrix = pd.DataFrame(bic_matrix)
    # 平铺 找最小值的位置
    print(bic_matrix)
    print(pd.isna(bic_matrix))
    p, q = bic_matrix.stack().idxmin()
    # BIC最小的p值和q值为：1、1
    print(u'BIC最小的p值和q值为：%s、%s' % (p, q))

