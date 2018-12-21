#-*- coding: utf-8 -*-
#模型检验
import pandas as pd

#参数初始化
discfile = '../data/discdata_processed.xls'
lagnum = 12 #残差延迟个数

data = pd.read_excel(discfile, index_col = 'COLLECTTIME')
data1 = data.iloc[:len(data)-5] #不使用最后5个数据
data2=data.iloc[len(data)-5:]
xdata = data1['CWXT_DB:184:D:\\']

from statsmodels.tsa.arima_model import ARIMA #建立ARIMA(0,1,1)模型

arima = ARIMA(xdata, (1, 1, 1)).fit() #建立并训练模型(p=0或者p=1都符合)

xdata_pred = arima.predict(typ = 'levels') #预测
pred_error = (xdata_pred - xdata).dropna() #计算残差

from statsmodels.stats.diagnostic import acorr_ljungbox #白噪声检验

lb, p= acorr_ljungbox(pred_error, lags = lagnum)
h = (p < 0.05).sum() #p值小于0.05，认为是非白噪声。
if h > 0:
  print(u'模型ARIMA(1,1,1)不符合白噪声检验')
else:
  print(u'模型ARIMA(1,1,1)符合白噪声检验')
#输出预测的5个数据
print(u'预测未来5天的磁盘容量为：%s' %(arima.forecast(5)[0]))

'''输出测试1,1,1模型的评价'''
xdata2=data2['CWXT_DB:184:D:\\']
abs_=(xdata2-arima.forecast(5)[0]).abs()
mae_=abs_.mean() #mae
rmse_=((abs_**2).mean())**0.5 #rmse
mape_=(abs_/xdata2).mean() #mape
print(u'平均绝对误差为：%0.4f. \n均方误差为:%0.4f. \n平均绝对百分误差为：%0.6f.'
      %(mae_,rmse_,mape_))
