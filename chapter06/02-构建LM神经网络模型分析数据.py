import pandas as pd
import itertools
# import matplotlib
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from keras import models
from keras.layers import core
from sklearn import metrics
from random import shuffle


# python-3.7.0环境下安装tensorflow
#  pip3 install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl

def cm_plot(y, yp):
    cm = metrics.confusion_matrix(y, yp)
    plt.matshow(cm, cmap=plt.cm.Greens)
    plt.colorbar()
    # for x in range(len(cm)):
    #     for y in range(len(cm)):
    #         plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')

    # 使用上面的也可以
    for x, y in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return plt


if __name__ == '__main__':
    file_name = './data/model.xls'
    # 读取数据
    data = pd.read_excel(file_name)
    # 随机打乱数据
    shuffle(data.values)

    # p 为获取训练数据的比例
    p = 0.8
    # 去前 80% 的数据为训练数据
    train_num = int(len(data) * p)
    train_data = data.iloc[: train_num, :]
    test_data = data.iloc[: (len(data) - train_num), :]
    #
    X_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]
    X_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1]
    # print(test_data)

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
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # 训练模型
    model.fit(X_train, y_train, epochs=100, batch_size=1)
    model.save_weights('./net.model')

    predict_result = model.predict_classes(X_train).reshape(len(X_train))

    plt = cm_plot(y_train, predict_result)
    plt.savefig('{0}.png'.format('./img/Figure_02_1'))

    plt.show()

    # 下面绘制LM神经网络的ROC曲线
    predict_result = model.predict(X_test).reshape(len(X_test))
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predict_result, pos_label=1)
    plt.plot(fpr, tpr, linewidth=2, label='ROC of LM')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    """
    Location String	Location Code
    'best'	0
    'upper right'	1
    'upper left'	2
    'lower left'	3
    'lower right'	4
    'right'	5
    'center left'	6
    'center right'	7
    'lower center'	8
    'upper center'	9
    'center'	10
    """
    plt.legend(loc=4)
    plt.savefig('{0}.png'.format('./img/Figure_02_2'))
    plt.show()
    print(thresholds)
