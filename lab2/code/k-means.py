#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('ISO-8859-1')
#K-means聚类算法

import pandas as pd
from sklearn.cluster import KMeans #导入K均值聚类算法（欧式距离）

inputfile='../tmp/zscoreddata.xls'#待聚类的数据文件
outputfile='../tmp/kmeans_result.xls'

k=5 #需要进行的聚类类别数

#读取数据并进行聚类分析
data=pd.read_excel(inputfile)#读取数据

#调用K-means算法，进行聚类分析
kmodel=KMeans(n_clusters=k,n_jobs=4)#n_jobs是并行数，一般等于CPU数比较好
kmodel.fit(data)#训练模型

#详细输出客户聚类结果
r1=pd.Series(kmodel.labels_).value_counts() #统计各个类别的数目
r2=pd.DataFrame(kmodel.cluster_centers_)#找出聚类中心
r=pd.concat([r2,r1],axis=1) #横向连接（0是纵向），得到聚类中心对应的类别下的数目
r.columns=list(data.columns)+[u'类别数目'] #重命名表头
r.to_excel(outputfile)#保存结果
                               
#绘制雷达图
import matplotlib.pyplot as plt #包含画图工具
import numpy as np
#设置ggplot的绘画风格
plt.style.use('ggplot')
plt.rcParams['font.sans-serif']='simkai'#用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
#标签
labels=np.array(data.columns)
#数据个数
dataLenth=5
N=len(r2)
angles=np.linspace(0,2*np.pi,N,endpoint=False)
data=pd.concat([r2,r2.ix[:,0]],axis=1)
angles=np.concatenate((angles,[angles[0]]))#使雷达图一圈封闭起来

fig=plt.figure(figsize=(6,6))
ax=fig.add_subplot(111,polar=True)#这里一定要设置为极坐标格式

for i in range(0,5):
    j=i+1
    ax.plot(angles,data.ix[i,:],'o-',linewidth=2,label="Customers{0}".format(j))#画线

ax.set_thetagrids(angles *180/np.pi,labels)#添加每个特征的标签
ax.set_title("Customers Analysis",va='bottom',fontproperties="SimHei")#添加标题
ax.set_rlim(-1,2.5)#设置雷达图范围
ax.grid(True)#添加网格
plt.legend()
plt.show()
