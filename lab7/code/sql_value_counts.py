#-*- coding:utf-8 -*-
#访问数据库
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pymysql?charset=utf8')
sql=pd.read_sql('all_gzdata',engine,chunksize=10000)
'''
用create_engine建立连接，链接地址的意思一次为“数据库格式mysql+程序名pymysql+
账号密码@地址端口/数据库名(pymysql)”,最后指定编码为utf8
all_gzdata是表名，engine是连接数据的殷勤，chunksize指定每次读取1万条记录。这时候
sql是一个容器，并未真正读取数据.
'''
'''

#分块统计各种网页类型访问量
counts=[i['fullURLId'].value_counts() for i in sql] #逐块统计
counts=pd.concat(counts).groupby(level=0).sum() #合并统计结果，把相同的统计项合并
#（即按index分组并求和）
counts=counts.reset_index() #重新设置index,将原来的index作为counts的一列
counts.columns=['index','num'] #重新设置列名，主要是第二列，默认为0
counts['type']=counts['index'].str.extract('(\d{3})') #提取前三个数字作为类别id
counts_=counts[['type','num']].groupby('type').sum() #按类别合并
counts_['percent'] = counts_['num']/counts_['num'].sum() #计算占比
print counts_.sort_values('num',ascending=False) #降序排列

#统计101咨讯类别内部统计
counts2=counts.copy()
counts2['type'] = counts['index'].str.extract('(\d{6})') #取前6个数字作为类别
counts2['type']=counts2['type'][counts2['type'].str.contains('101')] #筛选出是101咨询类别的
counts_2=counts2[['type','num']].groupby('type').sum() #按类别合并
counts_2['percent'] = counts_2['num']/counts_2['num'].sum() #计算占比
print counts_2.sort_values('num',ascending=False) #降序排列

#这个代码要单独跑

#统计107类别的情况
def count107(i): #自定义统计函数
  j = i[['fullURL']][i['fullURLId'].str.contains('107')].copy() #找出类别包含107的网址
  j['type'] = None #添加空列
  j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
  j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
  j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'
  return j['type'].value_counts()

counts3 = [count107(i) for i in sql] #逐块统计
counts3 = pd.concat(counts3).groupby(level=0).sum() #合并统计结果
counts3=counts3.reset_index() #重新设置index,将原来的index作为counts的一列
counts3.columns=['index','num']
counts3['percent']=counts3['num']/counts3['num'].sum() #计算占比
print counts3


#统计用户点击次数
c=[i['realIP'].value_counts() for i in sql] #分块统计各个IP的出现次数
count4 = pd.concat(c).groupby(level=0).sum()  #合并统计结果，level=0表示按index分组
count4=count4.reset_index() #重新设置index,将原来的index作为counts的一列
count4.columns=['index','clicknum']
count4=pd.DataFrame(count4) #Series转为DataFrame
count4['usernum']=1 #添加一列，全为1
count4['userpercent']=count4['usernum']/count4['usernum'].sum()
print count4.groupby('clicknum').sum() #统计各个“不同的点击次数” 分别出现的次数

'''
#统计点击率排名网址
addr=[i['fullURL'][i['fullURL'].str.contains('html')].value_counts() for i in sql]#分块统计各个网址html出现次数
addr= pd.concat(addr).groupby(level=0).sum()  #合并统计结果，level=0表示按index分组
addr=addr.reset_index() #重新设置index,将原来的index作为counts的一列
addr.columns=['addr','clicknum']
count5=addr.copy()
count5=pd.DataFrame(count5) #Series转为DataFrame
count5.groupby('addr').sum() #按照点击数合并
print count5.sort_values('clicknum',ascending=False) #降序排列

