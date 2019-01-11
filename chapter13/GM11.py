import numpy as np

# 自定义灰色预测函数
# 灰色模型GM(1, 1)  参考链接：https://blog.csdn.net/qq547276542/article/details/77865341

def GM11(x0):
    # 累加生成AGO
    x1 = x0.cumsum()
    # 紧邻两项求和在求平均数
    z1 = (x1[:len(x1) - 1] + x1[1:]) / 2.0  # 紧邻均值（MEAN）生成序列
    # 然后变成一列的二维数组
    z1 = z1.reshape((len(z1), 1))
    # 在原有的基础上再增加一列1 19 * 2的矩阵
    B = np.append(-z1, np.ones_like(z1), axis=1)

    # 输入数据x0从第1项开始取值 然后变成一个二维数组
    Yn = x0[1:].reshape((len(x0) - 1, 1))

    """
    1. 就我测试的数据来说 np.dot(B.T, B) 出来一个2 * 2的矩阵 np.dot(B.T, B)的结果如下
        [[6.80831876e+16 - 9.73196848e+08]
         [-9.73196848e+08  1.90000000e+01]]
    2. np.linalg.inv 使用inv函数计算逆矩阵
    """
    [[a], [b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Yn)  # 计算参数
    f = lambda k: (x0[0] - b / a) * np.exp(-a * (k - 1)) - (x0[0] - b / a) * np.exp(-a * (k - 2))  # 还原值
    delta = np.abs(x0 - np.array([f(i) for i in range(1, len(x0) + 1)]))
    C = delta.std() / x0.std()
    P = 1.0 * (np.abs(delta - delta.mean()) < 0.6745 * x0.std()).sum() / len(x0)
    return f, a, b, x0[0], C, P  # 返回灰色预测函数、a、b、首项、方差比、小残差概率
