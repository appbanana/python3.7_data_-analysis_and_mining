import pandas as pd

if __name__ == '__main__':
    file_name = './data/air_data.csv'
    air_data = pd.read_csv(file_name, encoding='utf-8', memory_map=True,)
    # explore = air_data.describe(percentiles=[], include='all').T
    # include='all' 所有的列都将被输出
    explore = air_data.describe(include='all').T
    # print('*****' * 10)
    # print(explore)
    """
                             count unique         top   freq      mean       std   min       25%       50%       75%       max
    MEMBER_NO                62988    NaN         NaN    NaN   31494.5   18183.2     1   15747.8   31494.5   47241.2     62988
    FFP_DATE                 62988   3068  2011/01/13    184       NaN       NaN   NaN       NaN       NaN       NaN       NaN
    FIRST_FLIGHT_DATE        62988   3406  2013/02/16     96       NaN       NaN   NaN       NaN       NaN       NaN       NaN
    GENDER                   62985      2           男  48134       NaN       NaN   NaN       NaN       NaN       NaN       NaN
    FFP_TIER                 62988    NaN         NaN    NaN   4.10216  0.373856     4         4         4         4         6

    """
    # 手动计算每一列中空值个数
    explore['null'] = len(air_data) - explore['count']

    explore = explore[['null', 'max', 'min']]
    explore.columns = [u'空值数', u'最大值', u'最小值']
    # print(explore)
    # print('*****' * 10)
    # print(explore)
    explore.to_excel('./temp/explore.xls')

