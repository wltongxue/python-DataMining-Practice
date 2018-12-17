import matplotlib.pyplot as plt #包含画图工具

'''画混淆矩阵图'''
def cm_plot(y, yp):
  
  from sklearn.metrics import confusion_matrix #导入混淆矩阵函数
  cm = confusion_matrix(y, yp) #混淆矩阵

  plt.matshow(cm, cmap=plt.cm.Greens) #画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
  plt.colorbar() #颜色标签
  
  for x in range(len(cm)): #数据标签
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
  
  plt.ylabel('True label') #坐标轴标签
  plt.xlabel('Predicted label') #坐标轴标签
  return plt

'''画ROC曲线图'''
#绘制决策树模型的ROC曲线
from sklearn.metrics import roc_curve #导入ROC曲线函数
def roc_plot(x,xp,l):
    fpr,tpr,thresholds=roc_curve(x,xp,
                             pos_label=1)
    plt.plot(fpr,tpr,linewidth=2,label=l) #做出ROC曲线
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.ylim(0,1.05)#边界范围
    plt.xlim(0,1.05)#边界范围
    plt.legend(loc=4)#图列
    plt.show() #显示作图结果
    return plt
