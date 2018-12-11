import itertools
import collections
import pandas as pd
# import numpy as np


# def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support):
#     counts = defaultdict(int)
#     # 遍历所有用户和打过分的电影
#     for user, reviews in favorable_reviews_by_users.items():
#         for itemset in k_1_itemsets:
#             # 如果一个集合的子集不是频繁项集 那么这个子集的超集一定不是频繁项集
#             if itemset.issubset(reviews):
#                 # 用户打过分 但没有出现在itemset子集中 然后在itemset和剩下的元素进行组合
#                 for other_review_moive in (reviews - itemset):
#                     current_superset = itemset | frozenset((other_review_moive,))
#                     counts[current_superset] += 1
#     return dict([(itemset, frequent) for itemset, frequent in counts.items() if frequent >= min_support])


def find_max_frequent_set(input_data, input_set, k_1_itemsets, support):

    for cur_set in input_set:
        for item in k_1_itemsets:
            temp_set = cur_set | item

            print(cur_set, item)


    # print(data_sum['a'])
    #
    # print(input_data.shape)
    # print(set(input_data))
    return 0


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

    # data_sum 总共有10位客人点的菜单，统计各个菜被点的次数
    # a    7.0
    # c    7.0
    # e    3.0
    # b    8.0
    # d    2.0
    data_sum = data.sum()
    # 总共10个菜单  input_data.shape = (10, 5)
    total_num = data.shape[0]
    # data_sum 计算每个菜的被点的概率
    # a    0.7
    # c    0.7
    # e    0.3
    # b    0.8
    # d    0.2
    data_sum = data / total_num

    # 获取满足最小支持度的单个项集 此时data_sum为L1
    data_sum = data_sum[data >= min_support]
    # 获取餐馆所有的菜名 eg：总共5个菜 {'c', 'b', 'a', 'e', 'd'}
    single_item_set = set(data_sum)
    current_frequent_set = [single_item_set]
    print(dict(data_sum))

    # frequent_itemsets = {}
    # frequent_itemsets[1] = dict(data_sum[data >= min_support])
    #
    # current_frequent_set[1] = find_max_frequent_set(data, current_frequent_set, single_item_set, min_support)

    # 寻找最大频繁项集 连接步 剪纸步
    # for i in range(2, len(data.columns)):
    #     if len(current_frequent_set) == 0:
    #         break
    #     else:
    #         current_frequent_set = find_max_frequent_set(current_frequent_set, single_item_set, min_support)

        # result = get_rule(data, min_support, min_confidence)
    # print(result)
