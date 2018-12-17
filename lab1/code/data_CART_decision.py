#进行重新编码
import sys
reload(sys)
sys.setdefaultencoding('ISO-8859-1')

import pandas as pd #导入数据分析库
from random import shuffle #导入随机函数shuffle,用来打乱数据

datafile='../data/model.xls' #数据名
data=pd.read_excel(datafile) #读取数据，数据的前三列是特征，第四列是标签
data=data.as_matrix() #将表格转换为矩阵
shuffle(data) #随机打乱数据

p = 0.8 #设置训练数据比例
train=data[:int(len(data)*p),:]#前80%为训练集
test=data[int(len(data)*p):,:]#后20%为测试集

#构建CART决策树模型
from sklearn.tree import DecisionTreeClassifier #导入决策树模型

treefile='../tmp/tree.pk1'#模型输出名字
tree = DecisionTreeClassifier() #建立决策树模型
tree.fit(train[:,:3],train[:,3]) #训练

#保存模型
from sklearn.externals import joblib
joblib.dump(tree,treefile)

from cm_plot import * #导入画混淆矩阵和ROC曲线的模块（自定义模块）
cm_plot(train[:,3],tree.predict(train[:,:3])).show() #显示混淆矩阵
#注意到Scikit-Learn使用predict方法直接给出预测结果
#显示roc曲线
roc_plot(test[:,3],tree.predict_proba(test[:,:3])[:,1],'ROC of CART')

