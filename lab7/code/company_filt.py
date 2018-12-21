#-*- coding:utf-8 -*-
#协同过滤推荐
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pymysql?charset=utf8')
sql=pd.read_sql('changed_gzdata',engine,chunksize=10000)

data=[i.copy() for i in sql ] #获取数据
data=pd.concat(data)

import time

start0 = time.clock()
print '开始转0-1'+str(start0)
#data从小到大依次排序
data.sort_values(by=['realIP','fullURL'],ascending=[True,True],inplace=True)
realIP = data['realIP'].value_counts().index #统计（合并相同）
realIP = np.sort(realIP)#排序
fullURL = data['fullURL'].value_counts().index #统计（合并相同）
fullURL = np.sort(fullURL)#排序
D = DataFrame( np.arange(len(realIP[:40])*len(fullURL[:20])).reshape(len(realIP[:40]),len(fullURL[:20])),
               index=realIP[:40],columns=fullURL[:20] )#创建dataframe以用户为行，商品为列
#转0-1矩阵，存在的标为1，其他填充为0
for i in range(len(data)):
    a = data.iloc[i,0] # 用户名
    b = data.iloc[i,1] # 网址
    D.loc[a,b] = 1 
D.fillna(0,inplace = True)
end0 = time.clock()
print '转成0、1矩阵所花费的时间为'+ str(end0-start0) +'s!'
D.to_csv('../tmp/zero_one.csv')#存储矩阵


#随机打乱数据
df=D.copy()
simpler = np.random.permutation(len(df)) 
df = df.take(simpler)# 打乱数据

#将数据集分为10份，前9为训练集，后1为测试集
train = df.iloc[:int(len(df)*0.9), :]
test = df.iloc[int(len(df)*0.9):, :]

#由于基于物品的推荐，对于矩阵，根据上面的推荐函数，index为网址，因此需要进行转置
df_train = df_train.T
df_test = df_test.T

import Recommender

#建立相似矩阵,训练模型
start1 = time.clock()
r=Recommender()
sim=r.fit(df_train) #计算物品的相似度矩阵
a=DataFrame(sim) #保存相似度矩阵
a.index=train.columns
a.columns=train.index
end1 = time.clock()
print u'建立相似矩阵耗时'+str(end1-start1)+'s!'
a.to_csv('../tmp/similarityMatrix.csv')

#使用测试机进行预测
start2 = time.clock()
result=r.recommend(df_test)
result1 = DataFrame(result)
result1.index = test.columns
result1.columns = test.index
end2 = time.clock()
print u'推荐函数耗时'+str(end2-start2)+'s!'
#保存预测结果
result1.to_csv('../tmp/recommendresult.csv')


# 定义展现具体协同推荐结果的函数，K为推荐的个数，recomMatrix为协同过滤算法算出的推荐矩阵的表格化
# type(K):int, type(recomMatrix):DataFrame

def xietong_result(K, recomMatrix ): 
    recomMatrix.fillna(0.0,inplace=True)# 将表格中的空值用0填充
    n = range(1,K+1)
    recommends = ['xietong'+str(y) for y in n]
    currentemp = DataFrame([],index = recomMatrix.columns, columns = recommends)#用户为行，推荐为列
    for i in range(len(recomMatrix.columns)):
        temp = recomMatrix.sort_values(by = recomMatrix.columns[i], ascending = False)
        k = 0 
        while k < K:
            currentemp.iloc[i,k] = temp.index[k]
            if temp.iloc[k,i] == 0.0:
                currentemp.iloc[i,k:K] = np.nan
                break
            k = k+1

    return currentemp

start3 = time.clock()
xietong_result = xietong_result(3, result1)
end3 = time.clock()
print '按照协同过滤推荐方法为用户推荐3个未浏览过的网址耗时为' + str(end3 - start3)+'s!'
xietong_result.to_csv('../tmp/xietong_result.csv')
