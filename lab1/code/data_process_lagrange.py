#-*-coding:utf-8 -*-
#拉格朗日插值代码
import pandas as pd #导入数据分析库
from scipy.interpolate import lagrange #导入拉格朗日函数

inputfile = '../data/missing_data.xls'#输入数据路径，需要使用ecel格式
outputfile= '../tmp/missing_data_processed.xls' #输出数据路径，需要使用Excel格式

data=pd.read_excel(inputfile,header=None) #读入数据

#自定义列向量插值函数
#s为列向量（表中某个字段的所有数据），n为被插值的位置，k为取前后的数据个数，默认为5
#取总共11个数据构建拉格朗日函数
def ployinterp_column(s,n,k=5):
	y=s[list(range(n-k,n)) + list(range(n+1,n+1+k))]
	y=y[y.notnull()]#剔除空值
	return lagrange(y.index,list(y))(n) #插值并返回插值结果

#逐个元素判断是否需要插值
for i in data.columns:
	for j in range(len(data)):
		if(data[i].isnull())[j]:#如果为空即插值
			data[i][j]=ployinterp_column(data[i],j)

#输出结果
data.to_excel(outputfile,header=None,index=False)
