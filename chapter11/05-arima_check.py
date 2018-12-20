import pandas as pd
from statsmodels.tsa import arima_model
from statsmodels.stats import diagnostic

if __name__ == '__main__':
    file_name = './temp/discdata_processed.xls'
    # file_name = './data/discdata_processed.xls'
    data = pd.read_excel(file_name, index_col='COLLECTTIME')

    # 最后5条数据作为验证数据
    train_data = data.iloc[:-5, :]
    test_data = data.iloc[-5:, :]
    # print(test_data)
    xdata = train_data['CWXT_DB:184:D:\\']

    # 定阶
    pmax = len(xdata) // 10
    qmax = len(xdata) // 10

    # 建立训练模型
    arima = arima_model.ARIMA(xdata, (0, 1, 1)).fit()
    xdata_pred = arima.predict(typ='levels')
    # 计算残差
    pred_error = (xdata_pred - xdata).dropna()

    # 再次检验白噪声
    lb, p = diagnostic.acorr_ljungbox(pred_error, lags=12)

    h = (p < 0.05).sum()
    if h > 0:
        print(u'模型ARIMA(0,1,1)不符合白噪声检验')
    else:
        print(u'模型ARIMA(0,1,1)符合白噪声检验')

    # 预测接下来的5天的数据
    test_pred = arima.forecast(5)[0]
    # 预测和实际的对比
    real_pred = pd.DataFrame(columns=[u'预测值', u'实际值'], index=test_data.index)
    real_pred[u'预测值'] = test_pred / 2 ** 20
    real_pred[u'实际值'] = test_data['CWXT_DB:184:D:\\'] / 2 ** 20
    real_pred.to_excel('./temp/predicted.xls')
    print(real_pred)





