#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd

inputfile='../data/data1.csv' #导入元数据
data=pd.read_csv(inputfile) #读取数据
r=[data.min(),data.max(),data.mean(),data.std()] #依次统计最小值、最大值、均值、标准差
r=pd.DataFrame(r,index=['Min','Max','Mean','STD']).T #构建统计量矩阵
np.round(r,2)
print r
