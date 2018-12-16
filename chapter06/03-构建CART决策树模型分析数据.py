from random import shuffle
import itertools
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
from sklearn import metrics, tree
from sklearn.externals import joblib
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


def cm_plot(y_true, y_predict):
    cm = metrics.confusion_matrix(y_true, y_predict)
    # fig, ax = plt.subplots()
    # im = ax.imshow(cm)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    print(cm)
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    
    
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    # plt.show()
    # plt.tight_layout()
    return plt
    
    # return plt


if __name__ == '__main__':
    file_name = './data/model.xls'
    # 读取数据
    data = pd.read_excel(file_name)
    # 随机打乱数据
    shuffle(data.values)
    # np.random.shuffle(data.values)
    
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
    
    # 建立决策树模型
    treefile = './tree.pkl'
    
    model = tree.DecisionTreeClassifier()
    # 训练模型
    model.fit(X_train, y_train)
    # joblib.dump(model, treefile)
    plt = cm_plot(y_train, model.predict(X_train))
    plt.savefig('{0}.png'.format('./img/Figure_03'))
    print(matplotlib.matplotlib_fname())
    

    plt.show()
