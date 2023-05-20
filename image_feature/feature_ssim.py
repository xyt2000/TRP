# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/30 19:29
# software: PyCharm

"""
文件说明：
"""
import os

import numpy as np
import cv2
import pandas as pd
from skimage.metrics import structural_similarity as ssim

def getres(img, kernel, i, j):
    k_w, k_d = kernel.shape
    res = np.sum(img[i:i + k_w, j:j + k_d] * kernel)
    return res


def conv2d(img, kernel):
    img_w, img_d = img.shape
    k_w, k_d = kernel.shape
    res = [[getres(img, kernel, i, j) for j in range(img_d - k_d + 1)] for i in range(img_w - k_w + 1)]
    return np.array(res, dtype=np.float32)




#首先读取两张图片，因为opencv是按照BGR读入的所以我就先进行了color的cvt。
#要是引用的该函数的话只用调用ssim(x,y)即可，里面的其他变量我已经在函数里面设置好了。
#可以更改的就是高斯核的大小即参数k, 已经高斯核的标准差sigma
def get_ssim(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    x1, y1 = img1.shape[0], img1.shape[1]
    x2, y2 = img2.shape[0], img2.shape[1]
    x = min(x1, x2)
    y = min(y1, y2)
    img1 = cv2.resize(img1, (x, y))
    img2 = cv2.resize(img2, (x, y))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    ssim_res = ssim(img1, img2, multichannel=True)
    print(ssim_res)
    return ssim_res

get_ssim("E:\TRP\data\\reports\\1\images\\424.png","E:\TRP\data\\reports\\1\images\\426.png")

cur_path = "..\\data"
if __name__ == "__main__":
    for num in range(1, 21):
        print(num)
        file_path = "\\reports\\"+ str(num) + "\\" + "app" + str(num)+".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        # download screenshots of all reports and return the local image path
        length = len(number)
        matrix = [[0 for i in range(length)]for j in range(length)]
        for i in range(length):
            matrix[i][i] = 1

            for j in range(i+1,length):
                index1 = number[i]
                index2 = number[j]
                tmp1 = images[i].split('.')
                tmp2 = images[j].split('.')
                path1 = os.path.join(cur_path, "reports", str(num), "images",str(index1) + '.' + tmp1[len(tmp1) - 1])
                path2 = os.path.join(cur_path, "reports", str(num), "images", str(index2) + '.' + tmp2[len(tmp2) - 1])
                try:
                    matrix[i][j] = get_ssim(path1,path2)
                    matrix[j][i] = matrix[i][j]
                except:
                    matrix[i][j] = -1
                    print(str(i)+"," + str(j))
            print(matrix[i])
        path = "..\\output\\" + str(num)+ "\\" + "ssim.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(matrix[i])+"\n")
        f.close()
