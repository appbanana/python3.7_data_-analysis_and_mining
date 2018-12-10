import pandas as pd
from sklearn import tree

if __name__ == '__main__':
    file_name = './data/sales_data.xls'
    # 读取数据 以序号为索引
    sale_data = pd.read_excel(file_name, index_col=u'序号')
    # 用1表示'好' '是' 高' -1表示'坏' '否' '低'
    sale_data[sale_data == u'好'] = 1
    sale_data[sale_data == u'是'] = 1
    sale_data[sale_data == u'高'] = 1
    sale_data[sale_data != 1] = -1
    # print(sale_data)

    X = sale_data.iloc[:, :-1].values.astype(int)
    y = sale_data.iloc[:, -1].values.astype(int)
    # 建立模型 基于信息熵
    """
    criterion   gini 基于基尼
                entropy 基于信息熵
    """
    model = tree.DecisionTreeClassifier(criterion='entropy')
    model.fit(X, y)

    # 导入决策树，可视化决策树
    # 导出的结果是一个dot文件，需要安装Graphviz才能将它转化为pdf或png等格式
    with open('tree.dot', 'w') as f:
        f = tree.export_graphviz(model, feature_names=sale_data.columns[:-1], out_file=f)

    """
    pip3 install Graphviz
    然后  dot -Tpdf tree.dot -o tree.pdf 导出决策树
      
    会报错 bash: dot: command not found
    解决方法：brew install gprof2dot 安装这个就可以了 

    """
