import pandas as pd


if __name__ == '__main__':
    file_name = './data/business_circle.xls'
    data = pd.read_excel(file_name, index_col=u'基站编号')
    # 最小值最大值标准化
    data = (data - data.min()) / (data.max() - data.min())
    data = data.reset_index()
    data.to_excel('./temp/standardized.xls', index=False)
    print(data)