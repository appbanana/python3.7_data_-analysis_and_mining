import itertools
import collections
import pandas as pd


# import numpy as np
# from  .apriori import *


def find_rule(input_data, mini_support, mini_confidence, ms='---'):
    # data_sum 总共有10位客人点的菜单，统计各个菜被点的次数
    data_sum = input_data.sum()
    # print(data_sum)
    # a    7.0
    # c    7.0
    # e    3.0
    # b    8.0
    # d    2.0
    
    # 总共10个菜单  input_data.shape = (10, 5)
    total_num = input_data.shape[0]
    # data_sum 计算每个菜的被点的概率
    data_sum = data_sum / total_num
    # print(data_sum)
    # a    0.7
    # c    0.7
    # e    0.3
    # b    0.8
    # d    0.2
    
    # 获取满足最小支持度的单个项集 此时data_sum为L1
    data_sum = data_sum[data_sum >= min_support]
    # # 获取餐馆所有的菜名 L1 eg：总共5个菜 {'c', 'b', 'a', 'e', 'd'}
    single_item_set = set(data_sum.index)
    # print(itertools.combinations(single_item_set, 2))
    for i in range(2, len(data_sum.index)):
        temp_set = itertools.combinations(single_item_set, i)
        temp_data = input_data
        for item_i in temp_set:
            # print(item_i) => 所有的两位组合 三位组合 四位组合 5位组合
            for item_j in item_i:
                print(input_data[])
        
        
    # for (x, y) in itertools.combinations(single_item_set, 2):
    #     print(single_item_set - set(x, y))
    # item_set_list = [single_item_set]
    # current_set = single_item_set
    # # for i in range(len(data_sum.index)):
    # for item_x in current_set:
    #     for item_y in single_item_set:
    #     # temp_set = set(item)
    #         print(set(item_x) | set(item_y))
            
        
    # for i in single_item_set:
    #     print(single_item_set - i)
        # itertools.combinations(single_item_set - i)
    # print(single_item_set)


if __name__ == '__main__':
    file_name = './data/menu_orders.xls'
    order_data = pd.read_excel(file_name, header=None)
    ct = lambda x: pd.Series(1, index=x[pd.notna(x)])
    b = map(ct, order_data.values)
    """
        a = pd.Series(1, index=['a', 'b', 'c'])
        b = pd.Series(1, index=['a', 'b', 'd'])
        pd = pd.DataFrame([a, b])
             a    b    c    d
        0  1.0  1.0  1.0  NaN
        1  1.0  1.0  NaN  1.0
    """
    data = pd.DataFrame(list(b)).fillna(0)
    # print('****' * 6)
    # print(data)
    """
         a    c    e    b    d
    0  1.0  1.0  1.0  0.0  0.0
    1  0.0  0.0  0.0  1.0  1.0
    2  0.0  1.0  0.0  1.0  0.0
    3  1.0  1.0  0.0  1.0  1.0
    4  1.0  0.0  0.0  1.0  0.0
    5  0.0  1.0  0.0  1.0  0.0
    6  1.0  0.0  0.0  1.0  0.0
    7  1.0  1.0  1.0  1.0  0.0
    8  1.0  1.0  0.0  1.0  0.0
    9  1.0  1.0  1.0  0.0  0.0

    """
    # 最小支持度
    min_support = 0.2
    # 最小置信度
    min_confidence = 0.5
    
    find_rule(data, min_support, min_confidence)
