# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/31 16:23
# software: PyCharm

"""
文件说明：
"""

path1 = "E:\TRP\output\\2\\word2vec_vector.txt"
path2 = "E:\TRP\output\\2\\CEDD.txt"
f1 = open(path1, "r")
f2 = open(path1, "r")
colors = []
cedds = []
lines = f1.readlines()
line1 = lines[97][1:-2].replace("\n", "").split(", ")
line1 = list(map(float, line1))
line2 = lines[83][1:-2].replace("\n", "").split(", ")
line2 = list(map(float, line2))
x_tfidf = [i for i in range(1,len(line2)+1)]

f1.close()
f2.close()
import matplotlib.pyplot as plt
import numpy as np

# epoch,acc,loss,val_acc,val_loss


# 画图
plt.plot(x_tfidf, line1, 'ro--', alpha=1, linewidth=1, label='report-1347')  # '
plt.plot(x_tfidf, line2, 'bo--', alpha=1, linewidth=1, label='report-1374')
#plt.plot(x_axis_data, y_axis_data3, 'go--', alpha=0.5, linewidth=1, label='acc')

plt.legend()  # 显示上面的label
plt.xlabel('feature dimension')
plt.ylabel('feature value')  # accuracy
plt.savefig('E:\TRP\early_data\word2vec.png')
# plt.ylim(-1,1)#仅设置y轴坐标范围
plt.show()
