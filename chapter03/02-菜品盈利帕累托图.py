import pandas as pd
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    file_path = './data/catering_dish_profit.xls'
    # 读取菜品盈利表数据
    profit_data = pd.read_excel(file_path, index_col=u'菜品名')
    profit_data.sort_values(by=u'盈利', ascending=False, )
    profit_data = profit_data[u'盈利']
    print(profit_data.head())

    # 使用pandas 开始绘制条形图
    plt.figure(num=2)
    profit_data.plot(kind='bar')
    plt.ylabel(u'盈利(元)')

    # 在绘制一条累加的盈利
    p = 1.0 * profit_data.cumsum() / profit_data.sum()
    p.plot(color='r', style='-o', linewidth=2, secondary_y=True)
    plt.annotate(format(p[6], '.2%'),
                 xy=(6, p[6]),
                 xytext=(5.8, p[6] * 0.9),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    plt.show()
