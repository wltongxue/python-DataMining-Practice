#-*- coding:utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pymysql?charset=utf8')
sql=pd.read_sql('all_gzdata',engine,chunksize=10000)


for i in sql:
    #删除律师助手页面、资讯发布、快搜页面等其他类型页面
    #免费发布咨询、快搜等实际上都不是html
    d =i[['realIP','fullURL']][~(i['pageTitle'].str.contains(u'律师助手')|
                                       i['pageTitle'].str.contains(u'咨询发布成功')|
                                    i['pageTitle'].str.contains(u'快搜'))] #只要网址列
    #删除中间页面
    d = d[~d['fullURL'].str.contains('midques_')]
    d = d[d['fullURL'].str.contains('\.html')].copy() #只要含有.html的网址
    #保存到数据库
    d.to_sql('cleaned_gzdata',engine,index=False,if_exists='append')
