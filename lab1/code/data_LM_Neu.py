#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('ISO-8859-1')

'''读取数据，设置数据'''
import pandas as pd #导入数据分析库
from random import shuffle #导入随机函数shuffle,用来打乱数据

datafile='../data/model.xls' #数据名
data=pd.read_excel(datafile) #读取数据，数据的前三列是特征，第四列是标签
data=data.as_matrix() #将表格转换为矩阵
shuffle(data) #随机打乱数据

p = 0.8 #设置训练数据比例
train=data[:int(len(data)*p),:]#前80%为训练集
test=data[int(len(data)*p):,:]#后20%为测试集

#########构建LM神经网络模型##########
from keras.models import Sequential #导入神经网络初始化函数
from keras.layers.core import Dense,Activation #导入神经网络层函数、激活函数
from keras.models import load_model

netfile='../tmp/net.model' #构建的神经网络模型存储路径

net = Sequential() #简历神经网络
net.add(Dense(input_dim=3,output_dim=10)) #添加输入层（3节点）到隐藏层（10节点）的连接
net.add(Activation('relu')) #隐藏层使用relu激活函数
net.add(Dense(input_dim=10,output_dim=1)) #添加隐藏层（10节点）到输出层（1节点）的连接
net.add(Activation("sigmoid"))#输出层使用sigmoid激活函数
#导入训练好的model_weights
net.load_weights(netfile)
'''
#编译模型，使用adam方法求解
net.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

#:3标识前3列（因为第四列是标签）
net.fit(train[:,:3],train[:,3],nb_epoch=1000,batch_size=1)#训练模型，循环1000次
net.save_weights(netfile) #保存模型
'''
predict_result = net.predict_classes(train[:,:3]).reshape(len(train))#预测结果变形
'''这里要提醒的是，keras用predict给出预测概率，predict_class才是给出预测类别，
    而且两者的预测结果都是n x 1维数组，而不是通常的1 下n'''

from cm_plot import * #导入自行编写的混淆矩阵可视化函数（）
cm_plot(train[:,3],predict_result).show() #显示混淆矩阵可视化结果
#显示ROC曲线
predict_result_test=net.predict(test[:,:3]).reshape(len(test)) #预测结果变形
roc_plot(test[:,3],predict_result_test ,'ROC of LM')


