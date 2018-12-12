import itertools
import pandas as pd


def find_rule(input_data, mini_support, mini_confidence, ms='--->'):
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

    # 筛选出频繁项集 frequent_set_count用来记录满足最小支持度的元素和其对应的概率
    frequent_set_count = dict()
    for i in range(1, len(data_sum.index)):
        # combinations('ABCD', 2)	=> AB AC AD BC BD CD
        # 取其中任意i个元素组合起来 具体用法参考 https://docs.python.org/3.7/library/itertools.html
        temp_set = itertools.combinations(single_item_set, i)
        # 遍历组合中所有的元祖
        for item in temp_set:
            # print(item_i) => 所有的1位组合，两位组合 三位组合 四位组合 5位组合 (a, )(a, b) (a, c), (a, b, c)...
            for j in range(len(item)):
                # 取出组合中每一个元素
                item_j = item[j]
                # 这很重要 这是为了取出所有满足组合的数据 eg:(a, b, c) 先取出菜名被点即a=1的数据，temp_data = input_data[input_data[a] == 1]
                #  在a的基础上取出 b=1的数据  temp_data = temp_data[temp_data[b] == 1]
                # 再在b的基础上取出c =1的数据 temp_data = temp_data[temp_data[c] == 1]
                if j == 0:
                    temp_data = input_data[input_data[item_j] == 1]
                else:
                    temp_data = temp_data[temp_data[item_j] == 1]
            # print(sorted(item), temp_data.shape)
            # 因为每一行数据代表客人点过的菜单，列是数据特征，即菜名。 temp_data.shape[0]是多少就是有多少条数据 取出满足最小支持度的数据
            if temp_data.shape[0] / total_num >= min_support:
                frequent_set_count[','.join(sorted(item))] = temp_data.shape[0] / total_num
    # print(frequent_set_count)
    """
    {'d': 0.2, 'e': 0.3, 'a': 0.7, 'c': 0.7, 'b': 0.8, 'b,d': 0.2, 'a,e': 0.3, 'c,e': 0.3, 'a,c': 0.5, 'a,b': 0.5, 'b,c': 0.5, 'a,c,e': 0.3, 'a,b,c': 0.3}
    """

    # 从频繁项集中寻找最强规则  x -> y
    # rule_dict 用来存放'Rule', '(Support, Confidence)' eg：格式rule_dict = {'Rule': [a1, a2, ..., ak], '(Support, Confidence)': [b1, b2, ..., bk]}
    rule_dict = {}
    # 存放所有的强规则 eg: d--->b
    rule_key_list = []
    # 存放所有强规则 对应的支持度和置信度 eg: (0.2,1.0)
    rule_value_list = []
    # 最强规则肯定是从频繁项集中找出来，所以我直接从frequent_set_count中key去寻找
    # 最强规则 最少是两个元素，首先要过滤掉单个元素的 filter(lambda x: len(x) > 1, frequent_set_count.keys())
    # print(list(filter(lambda x: len(x) > 1, frequent_set_count.keys())))
    #  => ['b,d', 'a,e', 'a,c', 'a,b', 'c,e', 'b,c', 'a,c,e', 'a,b,c']
    for key in filter(lambda x: len(x) > 1, frequent_set_count.keys()):
        # 我是先把key的字符串转化为set 这样方便操作
        key_set = set(key.replace(',', ''))
        # combinations('ABCD', 2)	=> AB AC AD BC BD CD 具体用法参考 https://docs.python.org/3.7/library/itertools.html
        # len(key_set) - 1 这是因为如果key是类似'a,b'这样2个元素的 我取其中一个作为x， 如果是'a,b,c' 3个元素的 我取其中的2个作为x，这个好好体会一下
        temp_set = itertools.combinations(key_set, len(key_set) - 1)
        # 取出key对应的支持度
        support = frequent_set_count[key]
        # 遍历刚才combinations找出的组合
        for item in temp_set:
            # 我要把item 元祖转化为字符串， 因为我要判断它是否在frequent_set_count的key中
            temp_subkey_str = ','.join(sorted(item))
            # 如果temp_subkey_str在frequent_set_count.keys中的话，在frequent_set_count找出temp_subkey_str发生的概率 (ps:x -> y 就是x事件发生的概率)
            if temp_subkey_str in frequent_set_count.keys():
                # 取出x事件发生的概率
                subkey_str_support = frequent_set_count[temp_subkey_str]
                # 计算置信度并与最小置信度比较 support为x,y同时发生的概率 subkey_str_support为x发生的概率
                if support / subkey_str_support >= mini_confidence:
                    # 满足最小置信度的规则 c,e--->a
                    rule_dict_key = temp_subkey_str + ms + ','.join(key_set - set(item))
                    # 满足最小置信度时 规则对应的 支持度和置信度
                    rule_dict_value = '(' + str(support) + ',' + str(support / subkey_str_support) + ')'
                    # 把规则添加到数组中 数组是有序的 这是方便构建pandas的DataFrame
                    rule_key_list.append(rule_dict_key)
                    # 把规则对应的支持度和置信度添加到数组中 数组是有序的 这样规则和它的支持度，置信度就一一对应 添加到数组也是方便构建pandas的DataFrame
                    rule_value_list.append(rule_dict_value)
    rule_dict['Rule'] = rule_key_list
    rule_dict['(Support, Confidence)'] = rule_value_list
    return pd.DataFrame(rule_dict, columns=['Rule', '(Support, Confidence)'])


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

    result = find_rule(data, min_support, min_confidence)
    print(result)
    """
            Rule     (Support, Confidence)
    0     d--->b                 (0.2,1.0)
    1     a--->c  (0.5,0.7142857142857143)
    2     c--->a  (0.5,0.7142857142857143)
    3     a--->b  (0.5,0.7142857142857143)
    4     b--->a               (0.5,0.625)
    5     e--->a                 (0.3,1.0)
    6     b--->c               (0.5,0.625)
    7     c--->b  (0.5,0.7142857142857143)
    8     e--->c                 (0.3,1.0)
    9   a,b--->c                 (0.3,0.6)
    10  a,c--->b                 (0.3,0.6)
    11  b,c--->a                 (0.3,0.6)
    12  a,e--->c                 (0.3,1.0)
    13  c,e--->a                 (0.3,1.0)
    14  a,c--->e                 (0.3,0.6)

    """
