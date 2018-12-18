from datetime import datetime
import time
import itertools
import pandas as pd


# from .apriori import find_rule


def connect_string(x, ms):
    x = list(map(lambda i: sorted(i.split(ms)), x))
    l = len(x[0])
    r = []
    for i in range(len(x)):
        for j in range(i, len(x)):
            # 如果前l-1项一样 但是最后一项不一样
            if x[i][:l - 1] == x[j][:l - 1] and x[i][l - 1] != x[j][l - 1]:
                # 保留前l-1项并把最后不一样的两项也添加到数组中 最后在添加到r中
                r.append(x[i][:l - 1] + sorted([x[j][l - 1], x[i][l - 1]]))
    return r


def find_rule(d, support, confidence, ms='---'):
    result = pd.DataFrame(index=['support', 'confidence'])
    support_series = 1.0 * d.sum() / len(d)

    # 初步筛选结果 筛选出单个元素出现的概率大于等于support的成员
    column = list(support_series[support_series >= support].index)
    # print(column)
    k = 0
    while len(column):
        k = k + 1
        print(u'\n正在进行第{0}次搜索...'.format(k))
        column = connect_string(column, ms)
        print(u'数目:{0}'.format(len(column)))
        # print(column)
        sf = lambda i: d[i].prod(axis=1, numeric_only=True)
        d_2 = pd.DataFrame(list(map(sf, column)), index=[ms.join(i) for i in column]).T
        # print('******' * 10)
        # print(d_2.head())
        support_series_2 = 1.0 * d_2.sum() / len(d)
        # support_series_2 = 1.0 * d_2[[ms.join(i) for i in column]].sum() / len(d)
        support_series = support_series.append(support_series_2)

        column = list(support_series_2[support_series_2 >= support].index)
        # print('******' * 10)
        # print(column)
        column2 = []
        # 遍历可能的推理，如{A,B,C}究竟是A+B-->C还是B+C-->A还是C+A-->B？
        # 这要注意 这有点巧妙
        for i in column:
            i = i.split(ms)
            for j in range(len(i)):
                column2.append(i[:j] + i[j + 1:] + i[j:j + 1])

        confidence_series = pd.Series(index=[ms.join(i) for i in column2])
        # 开始计算置信度
        for i in column2:
            confidence_series[ms.join(i)] = support_series[ms.join(sorted(i))] / support_series[ms.join(sorted(i[:-1]))]

        # 置信度筛选
        # for i in confidence_series[confidence_series > confidence].index:
        for i in confidence_series[confidence_series > confidence].index:  # 置信度筛选
            # 切记 这一定是0.0 不能写0  因为他会强制类型转换
            result[i] = 0.0
            result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]
            result[i]['confidence'] = confidence_series[i]
    result = result.T.sort_values(by=['confidence', 'support'], ascending=False)
    print(result)
    return result


if __name__ == '__main__':
    file_name = './data/apriori.txt'
    data = pd.read_csv(file_name, header=None)
    # 计时器
    # start = datetime.now()
    start = time.process_time()
    print('转换数据至0~1之间...')
    ct = lambda x: pd.Series(1, index=x[pd.notnull(x)])
    b = map(ct, data.values)
    data = pd.DataFrame(list(b)).fillna(0)
    # end = datetime.now()
    end = time.process_time()

    print('转换数据结束，用时{0}秒'.format(end - start))

    # print(data)
    """
          A2   B1   C3   D3   E1   F1   H1   B2   A1   C1   D1   E2   H2   A3   D2   E3   C2   H3   B4   E4   H4   D4   A4   B3   F2   C4   F3   F4
    0    1.0  1.0  1.0  1.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    1    1.0  1.0  1.0  1.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    2    1.0  1.0  1.0  1.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    3    1.0  1.0  1.0  1.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    4    1.0  0.0  1.0  1.0  1.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    """
    # 最下支持度
    mini_support = 0.06
    # 最小置信度
    mini_confidence = 0.75

    start = time.process_time()
    print('\n开始搜索关联规则...')
    find_rule(data, mini_support, mini_confidence)
    end = time.process_time()
    print('转换数据结束，用时{0}秒'.format(end - start))
