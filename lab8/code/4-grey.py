#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from GM11 import GM11 #引入自己编写好的灰色预测函数

inputfile='../data/data4.csv' #输入的数据文件
outputfile='../tmp/data4_GM11.xls' #灰色预测后保存的路径

data=pd.read_csv(inputfile) #读取数据
data.index = range(2002,2014)

data.loc[2014]=None
data.loc[2015]=None
l=['x1','x2','x3','x4','x6','x7','x9','x10'] #AdaptiveLasso选择的因素

#分别对选择因素进行预测
for i in l:
    gm = GM11(data[i][range(2002,2014)].as_matrix()) #获取GM11的所有结果
    f = gm[0]#获取灰色预测函数
    data[i][2014] = f(len(data)-1) #使用灰色预测函数预测2014年结果
    data[i][2015] = f(len(data)) #使用灰色预测函数预测2015年结果
    data[i] = data[i].round(2) #两位小数
    #输出验差检验
    print u'方差比：'+str(gm[4])
    print u'小残差：'+str(gm[5])
    

data[l+['y']].to_excel(outputfile) #结果输出

