import pandas as pd


def find_rule(d, support, confidence, ms=u'---'):
    result = pd.DataFrame(index=['support', 'confidence'])
    support_series = 1.0 * d.sum() / len(d)
    # 初步筛选结果 筛选出单个元素出现的概率大于等于support的成员
    column = list(support_series[support_series >= support].index)
    k = 0
    print(column)


if __name__ == '__main__':
    find_rule()
