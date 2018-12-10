import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Activation

if __name__ == '__main__':
    file_name = './data/sales_data.xls'
    sale_data = pd.read_excel(file_name)
    # 读取数据 以序号为索引
    sale_data = pd.read_excel(file_name, index_col=u'序号')

    sale_data[sale_data == u'好'] = 1
    sale_data[sale_data == u'是'] = 1
    sale_data[sale_data == u'高'] = 1
    sale_data[sale_data != 1] = -1

    X = sale_data.iloc[:, :-1].values.astype(int)
    y = sale_data.iloc[:, -1].values.astype(int)

    # 建立模型
    model = Sequential()
    model.add(Dense(input_dim=3, units=10))
    # # 用relu函数作为激活函数，能够大幅提高准确度
    # model.add(Activation('relu'))
    # model.add(Dense(input_dim=10, units=1))
    # 用于是0~1的输出， 用sigmoid函数作为激活函数
    # model.add(Activation('sigmoid'))
    # model.compile(loss='binary_crossentropy', optimizer='adam', class_mode='binary')
    # 训练模型 学习1000次
    # model.fit(X, y, nb_epoch=1000, batch_size=10)
    # # 分类预测
    # yp = model.predict_classes(x=X).reshape(len(y))