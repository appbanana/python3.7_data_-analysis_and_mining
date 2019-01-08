import time
import pandas as pd
import numpy as np


def xietong_result(K, recomMatrix):
    recomMatrix.fillna(0.0, inplace=True)  # 将表格中的空值用0填充
    n = range(1, K + 1)
    recommends = ['xietong' + str(y) for y in n]
    # 取recomMatrix.columns(网址)作索引  'xietong1'， 'xietong2'， 'xietong3' 作为列
    currentemp = pd.DataFrame([], index=recomMatrix.columns, columns=recommends)
    for i in range(len(recomMatrix.columns)):
        # 取出每一个用户与所有网址的数据 然后降序排列
        temp = recomMatrix.sort_values(by=recomMatrix.columns[i], ascending=False)
        k = 0
        # 取出相似度比较高的前3个
        while k < K:
            currentemp.iloc[i, k] = temp.index[k]
            if temp.iloc[k, i] == 0.0:
                currentemp.iloc[i, k:K] = np.nan
                break
            k = k + 1

    return currentemp


if __name__ == '__main__':
    file_name = './data/recommend_matrix.csv'
    rec_result = pd.read_csv(file_name, index_col=[0])
    print(rec_result.head())
    start = time.process_time()
    xietong_result = xietong_result(3, rec_result)
    end = time.process_time()
    # 协同算法推荐网址 花费时间 15.635650
    print('协同算法推荐网址 花费时间 %f' % (end - start))

    print(xietong_result)
    """
                                                             xietong1                                           xietong2                                           xietong3
    827687543   http://***/info/hunyin/shouyangfagui/201312172...  http://***/info/hunyin/ccfglhccfg/201408063305...  http://***/info/hunyin/ccfglhccfg/201108161441...
    1069718030  http://***/info/hunyin/lhlawlhss/2013122628763...  http://***/info/hunyin/lhlawlhss/2009020621988...  http://***/info/hunyin/lhlawlhss/2011012511474...
    21327886    http://***/info/hunyin/lihunshouxu/20131204287...  http://***/info/hunyin/lhlawlhxy/2014031828831...  http://***/info/hunyin/lhlawlhxy/2013121328751...
    603395956   http://***/info/hunyin/lihunshouxu/20131204287...  http://***/info/hunyin/lhlawlhxy/2014031828831...  http://***/info/hunyin/lhlawlhxy/2013121328751...
    1695186702  http://***/info/hunyin/lihunshouxu/20131204287...  http://***/info/hunyin/lhlawlhxy/2014031828831...  http://***/info/hunyin/lhlawlhxy/2013121328751...
    90652218    http://***/info/hunyin/feihunshengzinv/2011092...  http://***/info/hunyin/feihunshengzinv/2012091...  http://***/info/hunyin/feihunshengzinv/2012022...
    4202370830  http://***/info/hunyin/jiehun/hunjia/201312182...  http://***/info/hunyin/jiehun/hunjia/201305211...  http://***/info/hunyin/jiehun/hunjia/201109201...
    3712559419  http://***/info/hunyin/lhlawlhss/2012070216475...  http://***/info/hunyin/wangshangjiehun/2011061...  http://***/info/hunyin/hunfang/hunqiangoufang/...
    1857051504  http://***/info/hunyin/feihunshengzinv/2014011...  http://***/info/hunyin/lhlawlhss/2011090815081...  http://***/info/hunyin/lihunzhengju/2015010533...
    2217747319  http://***/info/hunyin/lhlawlhss/2014012028782...  http://***/info/hunyin/lhlawlhss/2011011194870...  http://***/info/hunyin/hunyindiaochaquzheng/20...
    2850210015   http://***/info/hunyin/hyflws/2011011397512.html  http://***/info/hunyin/hunyinfagui/20101010604...  http://***/info/hunyin/ccfglhccfg/201101129726...
    1969986574                                                NaN                                                NaN                                                NaN
    1801527673  http://***/info/hunyin/hunyinfagui/20100913472...  http://***/info/hunyin/hunwaitongji/2011100815...  http://***/info/hunyin/hunyinfagui/20131211287...
    352293902   http://***/info/hunyin/jiatingbaoli/2015010733...  http://***/info/hunyin/lhlawlhss/2011090815081...  http://***/info/hunyin/lihunzhengju/2015010533...

    """