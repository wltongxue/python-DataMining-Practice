#-*- coding:utf-8 -*-
#删除同一网页或其翻页的情况
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pymysql?charset=utf8')
sql=pd.read_sql('cleaned_gzdata',engine,chunksize=10000)

for i in sql: #逐块变换并去重
    d=i.copy()
    #将下划线后面部分去掉，规范为标准网址
    d['fullURL'] = d['fullURL'].str.replace('_\d{0,2}.html','.html')
    d =d.drop_duplicates() #删除重复记录
    d.to_sql('changed_gzdata',engine,index=False,if_exists='append') #保存
