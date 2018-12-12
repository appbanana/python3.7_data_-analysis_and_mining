import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics import tsaplots
from statsmodels.tsa import stattools
from statsmodels.stats import diagnostic
from statsmodels.tsa import arima_model

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    file_name = './data/arima_data.xls'
    # 取数据 以日期为索引
    arima_data = pd.read_excel(file_name, index_col=u'日期')
    print(arima_data.head())
    """
    日期         销量
    2015-01-01  3023
    2015-01-02  3039
    2015-01-03  3056
    2015-01-04  3138
    2015-01-05  3188
    """
    # 时序图
    # arima_data.plot()
    # plt.savefig('{0}.png'.format('./img/Figure_8_1'))
    # plt.show()

    # 自相关图
    # tsaplots.plot_acf(arima_data)
    # plt.savefig('{0}.png'.format('./img/Figure_8_2'))
    # plt.show()

    # 平稳性检测
    print(stattools.adfuller(arima_data[u'销量']))
    """
    (1.8137710150945285, 0.9983759421514264, 10, 26, {'1%': -3.7112123008648155, '5%': -2.981246804733728, '10%': -2.6300945562130176}, 299.46989866024177)
    """

    # 差分后的结果
    diff_data = arima_data.diff().dropna()
    diff_data.columns = [u'销量差分']
    diff_data.plot()
    # plt.savefig('{0}.png'.format('./img/Figure_8_3'))

    # 差分后的自相关图
    tsaplots.plot_acf(diff_data)
    # plt.savefig('{0}.png'.format('./img/Figure_8_4'))

    # 差分后偏相关图
    tsaplots.plot_pacf(diff_data)
    # plt.savefig('{0}.png'.format('./img/Figure_8_5'))
    # plt.show()

    # 白噪声检验
    print(u'差分序列白噪声检验结果:', diagnostic.acorr_ljungbox(diff_data, lags=1))

    # 定阶
    pmax = int(len(diff_data) / 10)
    qmax = int(len(diff_data) / 10)
    bic_matrix = []
    for p in range(pmax):
        temp = []
        for q in range(qmax):
            try:
                temp.append(arima_model.ARIMA(arima_data, (p, 1, q)).fit().bic)
            except:
                temp.append(None)
        bic_matrix.append(temp)
    bic_matrix = pd.DataFrame(bic_matrix)
    p, q = bic_matrix.stack().idxmin()
    # print(bic_matrix.stack())
    print(u'BIC最小的P值和q值: %s %s' % (p, q))

    model = arima_model.ARIMA(arima_data, (p, 1, q)).fit()
    print('****' * 10)
    print(model.summary2())
    """
    ****************************************
                                   Results: ARIMA
    ====================================================================
    Model:              ARIMA            BIC:                 422.5101  
    Dependent Variable: D.销量             Log-Likelihood:      -205.88   
    Date:               2018-12-12 16:22 Scale:               1.0000    
    No. Observations:   36               Method:              css-mle   
    Df Model:           2                Sample:              01-02-2015
    Df Residuals:       34                                    02-06-2015
    Converged:          1.0000           S.D. of innovations: 73.086    
    No. Iterations:     12.0000          HQIC:                419.418   
    AIC:                417.7595                                        
    ----------------------------------------------------------------------
                   Coef.    Std.Err.     t      P>|t|     [0.025    0.975]
    ----------------------------------------------------------------------
    const         49.9561    20.1390   2.4806   0.0182   10.4844   89.4278
    ma.L1.D.销量     0.6710     0.1648   4.0712   0.0003    0.3480    0.9941
    -----------------------------------------------------------------------------
                     Real           Imaginary          Modulus          Frequency
    -----------------------------------------------------------------------------
    MA.1           -1.4902             0.0000           1.4902             0.5000
    ====================================================================

    """
    print('****' * 10)
    print(model.forecast(5))
    """
    ****************************************
    (array([4873.9665477 , 4923.92261622, 4973.87868474, 5023.83475326,
           5073.79082178]), array([ 73.08574262, 142.32680643, 187.54283213, 223.80283273,
           254.95705912]), array([[4730.72112437, 5017.21197102],
           [4644.96720157, 5202.87803086],
           [4606.3014882 , 5341.45588128],
           [4585.18926146, 5462.48024505],
           [4574.0841683 , 5573.49747526]]))

    """