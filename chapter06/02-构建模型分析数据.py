import pandas as pd
from keras import models
from keras.layers import core

# 注意 tensorflow在python-3.7.0虚拟的环境下没有找到对应的版本 我在这个文件切换到我的虚拟3.6.1环境

if __name__ == '__main__':
    file_name = './data/model.xls'
    # 读取数据
    data = pd.read_excel(file_name)
    # print(data)
    # 随机取其中的80%的数据作为训练数据 剩下的作为测试数据
    train_data = data.sample(frac=0.8)
    # 取出剩下的数据作为 测试数据
    """
    a = pd.Series(np.arange(10))
    b = a - a.sample(frac=0.3)
    c = a[b.isna()]
    以下是b的数据 Nan的为随机没有取到的数据 0为随机取到是数据
    0    NaN
    1    NaN
    2    NaN
    3    0.0
    4    NaN
    5    0.0
    6    NaN
    7    NaN
    8    NaN
    9    0.0
    """
    test_data = data[(data - train_data).isna()]

    # 建立模型
    model = models.Sequential()
    # 添加输入层（3个点）到 隐藏层（10个点）的连接
    model.add(core.Dense(input_dim=3, units=10))
    # 隐藏层使用relu激活函数
    model.add(core.Activation('relu'))
    # 添加隐藏层（10个点）到输出层（1个点）的连接
    model.add(core.Dense(input_dim=10, units=1))
    # 输出层使用sigmoid激活函数
    model.add(core.Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', class_mode='binary')
    # 训练模型
    # model.fit(train_data.iloc[:, :-1], train_data.iloc[:, -1], nb_epoch=1000, batch_size=1)
    # model.save_weights('./net.model')
