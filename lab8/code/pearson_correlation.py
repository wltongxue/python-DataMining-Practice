#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd

inputfile='../data/data1.csv' #导入元数据
data=pd.read_csv(inputfile) #读取数据
p = np.round(data.corr(method='pearson'),2) #计算相关系数矩阵，保留两位小数
print p
