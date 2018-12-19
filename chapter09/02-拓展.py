import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm, metrics
from matplotlib import pyplot as plt

# # 指定默认字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# https://blog.csdn.net/chenxiqilin/article/details/50395809
def cm_plot(y_true, y_predict):
    cm = metrics.confusion_matrix(y_true, y_predict)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    return plt


if __name__ == '__main__':
    file_name = './data/moment.csv'
    data = pd.read_csv(file_name, encoding='gbk')
    # shuffle(data.values)
    # 构建特征和标签
    X = data.iloc[:, 2:] * 30
    y = data[u'类别'].astype(int)
    # 去其中20%当做测试数据 80%当做训练数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)

    # 构建模型 训练模型
    model = svm.SVC(gamma='scale')
    model.fit(X_train, y_train)
    scores = model.score(X_train, y_train)
    mean_score = np.mean(scores)
    print(u'正确率%f' % mean_score)

    # 混淆矩阵
    plt = cm_plot(y_train, model.predict(X_train))
    plt.savefig('{0}.png'.format('./img/Figure_01_1'))
    plt.show()

    # 验证模型
    plt = cm_plot(y_test, model.predict(X_test))
    plt.savefig('{0}.png'.format('./img/Figure_01_2'))
    plt.show()
    scores = model.score(X_test, y_test)
    mean_score = np.mean(scores)
    print(u'正确率%f' % mean_score)


