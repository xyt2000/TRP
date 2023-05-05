# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/11 16:45
# software: PyCharm

"""
文件说明：
"""
import os

import pandas as pd

cur_path = "E:\TRP\data"
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
        img_path = []
        for i in range(length):
            index1 = number[i]
            tmp1 = images[i].split('.')
            path1 = os.path.join(cur_path, "reports", str(num), "images", str(index1) + '.' + tmp1[len(tmp1) - 1])
            img_path.append(path1)
        path = "E:\TRP\data\\reports\\" + str(num) + "\\" + "image_path.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(img_path[i]) + "\n")
        f.close()