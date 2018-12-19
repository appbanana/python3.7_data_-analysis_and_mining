from datetime import datetime
import time
import itertools
import pandas as pd
import apriori

if __name__ == '__main__':
    file_name = './data/apriori.txt'
    data = pd.read_csv(file_name, header=None)
    # 计时器
    # start = datetime.now()
    start = time.process_time()
    print('转换数据至0-1之间...')
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
    apriori.find_rule(data, mini_support, mini_confidence)
    end = time.process_time()
    print('转换数据结束，用时{0}秒'.format(end - start))
