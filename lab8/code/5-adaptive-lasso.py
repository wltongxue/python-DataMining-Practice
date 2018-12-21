#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd

inputfile='../data/data5.csv' #导入元数据
data=pd.read_csv(inputfile) #读取数据


#导入AdaptiveLasso算法，要在较新的scikit中
from sklearn.linear_model import LassoLars
model = LassoLars(alpha=1)
model.fit(data.iloc[:,0:7],data['y'])
co = model.coef_ #各个特征的系数
print co
