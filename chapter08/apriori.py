import pandas as pd


def connect_string(x, ms):
    x = list(map(lambda i: sorted(i.split(ms)), x))
    l = len(x[0])
    r = []
    for i in range(len(x)):
        # for j in range(i, len(x)):
        # 我认为这还以改进 可以从i+1开始
        for j in range(i + 1, len(x)):
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
        # 这用的也很巧妙 eg：column = [['A1', 'B2', 'C1], ['A1', 'B3', 'D1], ...]， d['A1'] * d['B2'] * d['C1'] 就可以取出同时是A1, B2, C1是数据
        sf = lambda i: d[i].prod(axis=1, numeric_only=True)
        d_2 = pd.DataFrame(list(map(sf, column)), index=[ms.join(i) for i in column]).T
        # print('******' * 10)
        # print(d_2.head())
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
