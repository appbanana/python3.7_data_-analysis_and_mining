import pandas as pd

if __name__ == '__main__':
    file_name = './data/zscoredata.xls'
    core_data = pd.read_excel(file_name)

    # 零均值标准化数据
    core_data = (core_data - core_data.mean(axis=0)) / core_data.std(axis=0)
    core_data.columns = ['Z' + i for i in core_data.columns]
    core_data.to_excel('./temp/core_data.xls', index=False)

    # print(core_data1 == core_data2)

    # print(core_data.head())
