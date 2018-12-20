import pandas as pd
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


def attr_trans(x):
    result = pd.Series(index=['SYS_NAME', 'CWXT_DB:184:C:\\', 'CWXT_DB:184:D:\\', 'COLLECTTIME'])
    result['SYS_NAME'] = x['SYS_NAME'].iloc[0]
    result['COLLECTTIME'] = x['COLLECTTIME'].iloc[0]
    result['CWXT_DB:184:C:\\'] = x['VALUE'].iloc[0]
    result['CWXT_DB:184:D:\\'] = x['VALUE'].iloc[1]

    return result


if __name__ == '__main__':
    file_name = './data/discdata.xls'
    data = pd.read_excel(file_name, )
    data = data[data['TARGET_ID'] == 184].copy()
    print(data.head())
    """
      SYS_NAME     NAME  TARGET_ID DESCRIPTION ENTITY        VALUE COLLECTTIME
    0   财务管理系统  CWXT_DB        184     磁盘已使用大小    C:\  34270787.33  2014-10-01
    1   财务管理系统  CWXT_DB        184     磁盘已使用大小    D:\  80262592.65  2014-10-01
    4   财务管理系统  CWXT_DB        184     磁盘已使用大小    C:\  34328899.02  2014-10-02
    5   财务管理系统  CWXT_DB        184     磁盘已使用大小    D:\  83200151.65  2014-10-02
    8   财务管理系统  CWXT_DB        184     磁盘已使用大小    C:\  34327553.50  2014-10-03

    """
    # 以时间分组
    data_group = data.groupby('COLLECTTIME')
    # print(list(data_group))
    data_processed = data_group.apply(attr_trans)
    # print(data_processed)
    data_processed.to_excel('./temp/discdata_processed.xls', index=False)

    c_data = data[data[u'ENTITY'] == 'C:\\']
    plt.plot(c_data['COLLECTTIME'], c_data['VALUE'], 'ro-')
    plt.title(u'C盘已使用空间的时序图')
    plt.xlabel('日期')
    plt.ylabel(u'磁盘使用大小')
    plt.xticks(rotation=30)
    # plt.xticks(pd.date_range(c_data['COLLECTTIME'].date().min(), c_data['COLLECTTIME'].date().max(), periods=7), rotation=30)  # 设置时间标签显示格式

    plt.savefig('{0}.png'.format('./img/Figure_01_1'))
    plt.show()

    d_data = data[data[u'ENTITY'] == 'D:\\']
    plt.plot(d_data['COLLECTTIME'], d_data['VALUE'], 'ko-')
    plt.title(u'D盘已使用空间的时序图')
    plt.xlabel('日期')
    plt.ylabel(u'磁盘使用大小')
    plt.xticks(rotation=30)
    # plt.xticks(pd.date_range(start=d_data['COLLECTTIME'].min(), end=d_data['COLLECTTIME'].max()), rotation=30)  # 设置时间标签显示格式

    plt.savefig('{0}.png'.format('./img/Figure_01_2'))
    plt.show()
    # print(d_data['COLLECTTIME'].min().date())
    # print(d_data['COLLECTTIME'][0], d_data['COLLECTTIME'][-1])
    # print(pd.date_range(start=d_data['COLLECTTIME'].min().date(), end=d_data['COLLECTTIME'].max().date(), periods=7))

