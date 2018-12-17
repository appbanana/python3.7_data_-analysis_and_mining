import pandas as pd

if __name__ == '__main__':
    file_name = './data/air_data.csv'
    air_data = pd.read_csv(file_name, encoding='utf-8', memory_map=True, )
    print(air_data.describe().T)
    # print(len(air_data))
    # 过滤掉票价为空的记录
    air_data = air_data[air_data['SUM_YR_1'].notna()]
    # print(len(air_data))
    air_data = air_data[air_data['SUM_YR_2'].notna()]

    # 丢弃票价为0的数据
    index1 = air_data['SUM_YR_1'] > 0
    index2 = air_data['SUM_YR_2'] > 0
    index3 = air_data['avg_discount'] == 0 & air_data['SEG_KM_SUM']
    # 丢弃折扣为0 但总飞行公里数同时为0的数据
    air_data = air_data[index1 | index2 | index3]
    air_data.to_excel('./temp/clean.xls')