import pandas as pd
from matplotlib import pyplot as plt

# 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    file_path = 'data/catering_sale.xls'
    # sale_data = pd.read_excel(file_path)
    """
        熟悉一下其他参数
        sheet_name excel中表名
        usecols=[1]  取索引为1的那一列 就是第二列
        index_col=u'日期'  拿日期当索引值, 默认是从0开始 一次递增
    """
    sale_data = pd.read_excel(file_path, sheet_name='Sheet1', index_col=u'日期')
    # print(sale_data.head())
    plt.figure(num=1)
    p = sale_data.boxplot(return_type='dict')
    # x异常值
    x = p['fliers'][0].get_xdata()
    # y 异常值
    y = p['fliers'][0].get_ydata()
    y.sort()

    # 箱型图添加annotate
    """
        plt.annotate(s=y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.05 - 0.8 / (y[i] - y[i - 1]), y[i]))
        s 是你要展示的文本, xy 是这个异常点的坐标 xytext 是文本的坐标
        arrowprops 是测试属性加上去的
    """
    for i in range(len(x)):
        if i > 0:
            plt.annotate(s=y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.05 - 0.8 / (y[i] - y[i - 1]), y[i]))
        else:
            plt.annotate(s=y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.1, y[i]),
                         arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8, headlength=10))
    plt.show()
