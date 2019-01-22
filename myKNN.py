import numpy as np
import operator


def my_KNN(test_data, train_data, labels, k=1):
    sample_size = len(train_data)
    # 让测试数据和训练样本数据拥有同样多的数据
    test_data = np.tile(test_data, (sample_size, 1))
    delta = (train_data - test_data) ** 2
    distance = (delta.sum(axis=1)) ** 0.5
    #
    sort_distanse = distance.argsort()
    class_count = {}
    for i in range(0, k):
        vote_label = labels[sort_distanse[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    result = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return result[0][0]


# training samples
sample = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])

# the labels of samples
label = ['A', 'A', 'B', 'B']
print(my_KNN([10, 0], sample, label, 3))  # test
