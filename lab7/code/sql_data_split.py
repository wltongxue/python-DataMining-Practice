#-*- coding:utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pymysql?charset=utf8')
sql=pd.read_sql('changed_gzdata',engine,chunksize=10000)

for i in sql: #逐块增加类别
    d=i.copy()
    d['type']=d['fullURL'] #复制一列，也可以创建空的，一会要更改
    #将含有ask、askzt关键字的网址的类别归为咨询
    d['type'][d['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun'
    #将含有info、zhishi、fagui的网址类别归为知识类
    d['type'][d['fullURL'].str.contains('(info)|(zhishi)|(fagui)')] = 'zhishi'
    d.to_sql('splited_gzdata',engine,index=False,if_exists='append')#保存
