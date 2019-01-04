import pandas as pd


if __name__ == '__main__':
    a = ['http://www.lawtime.cn/info/minshi/fagui/2013051382463.html',
         'http://www.lawtime.cn/info/minshi/fagui/2012111982349.html',
         'http://www.lawtime.cn/ask/question_3565164.html',
         'http://www.lawtime.cn/zhishiku/laodong/zixun/2108.html']

    a = pd.Series(a)
    temp_a = a.str.extract('/info/(.*?)/(.*?)/')
    # print(temp_a)
    """
            0      1
    0  minshi  fagui
    1  minshi  fagui
    2     NaN    NaN
    3     NaN    NaN
    """
    temp_b = a.str.extract('/zhishiku/(.*?)/(.*?)/')
    # print(temp_b)
    """
             0      1
    0      NaN    NaN
    1      NaN    NaN
    2      NaN    NaN
    3  laodong  zixun
    """
    # 这种方法走不通 不行
    # c = pd.merge(temp_a, temp_b, on=a.index)
    # print(c)
    """
           key_0     0_x    1_x      0_y    1_y
    0      0  minshi  fagui      NaN    NaN
    1      1  minshi  fagui      NaN    NaN
    2      2     NaN    NaN      NaN    NaN
    3      3     NaN    NaN  laodong  zixun

    """
    # 确认过数据 因为我的数据 这两类没有交集 所以可以这样做
    temp_a[temp_b[0].notna()] = temp_b[temp_b[0].notna()]
    temp_a[temp_b[1].notna()] = temp_b[temp_b[1].notna()]
    print(temp_a)
    """
             0      1
    0   minshi  fagui
    1   minshi  fagui
    2      NaN    NaN
    3  laodong  zixun

    """