#-*- coding:utf-8 -*-
import pandas as pd
inputfile='../tmp/data2_GM11.xls' #灰色预测后保存的路径
outputfile='../data/VAT.xls' #神经网络预测后保存的路径
modelfile='../tmp/2-net.model' #模型保存路径
data=pd.read_excel(inputfile) #读取数据
feature=['x1','x3','x5'] #特征所在列

data_train=data.loc[range(1999,2014)].copy() #取2014年前的数据
data_mean=data_train.mean()
data_std = data_train.std()
data_train=(data_train - data_mean)/data_std #数据标准化
x_train =  data_train[feature].as_matrix() #特征数据
y_train = data_train['y'].as_matrix() #标签数据

from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras import losses

model = Sequential() #建立模型
model.add(Dense(input_dim=3,output_dim=6))
model.add(Activation('relu'))#用relu函数作为激活函数，能够大幅提供准确度
model.add(Dense(input_dim=6,output_dim=1))
'''
#编译模型
model.compile(loss=losses.mean_squared_error,optimizer='adam') #编译模型
model.fit(x_train,y_train,nb_epoch=10000,batch_size=16) #训练模型,学习一万次
model.save_weights(modelfile) #保存模型参数
'''
model.load_weights(modelfile)#导入训练好的model_weights


#预测，并还原结果
x=((data[feature]-data_mean[feature])/data_std[feature]).as_matrix()
data[u'y_pred'] = model.predict(x) * data_std['y'] +data_mean['y']
data[u'y_pred']=data[u'y_pred'].round()
data.to_excel(outputfile)

import matplotlib.pyplot as plt
p=data[['y','y_pred']].plot(subplots=True,style=['b-o','r-*'])
plt.show()
