# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/30 19:39
# software: PyCharm

"""
文件说明：
"""
import os
from urllib.request import urlretrieve
import pandas as pd

cur_path = os.path.dirname(os.path.realpath(__file__))
if __name__ == "__main__":

    for i in range(1,21):
        file_path = "\\reports\\"+str(i) + "\\"+ "app" + str(i)+".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        # download screenshots of all reports and return the local image path
        def download_img(image_url, index, num):
            tmp = image_url.split('.')
            path = os.path.join(cur_path, "../reports", str(num), "images", str(index) + '.' + tmp[len(tmp) - 1])
            urlretrieve(image_url, path)
            print("download img to {}".format(path))
            return path

        img_path = []
        for j in range(len(number)):
            img_path.append(download_img(images[j], number[j], i))