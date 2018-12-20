import pandas as pd

if __name__ == '__main__':
    file_name = './temp/predicted.xls'
    data = pd.read_excel(file_name)

    # 计算误差
    abs_ = (data[u'预测值'] - data[u'实际值']).abs()
    # 平均绝对误差
    mae_ = abs_.mean()
    # 均方根误差
    rmse_ = ((abs_ ** 2).mean()) ** 0.5
    # 平均绝对误差
    mape_ = (abs_ / data[u'实际值']).mean()
    print(u'平均绝对误差为：%0.4f，\n均方根误差为：%0.4f，\n平均绝对百分误差为：%0.6f。' % (mae_, rmse_, mape_))