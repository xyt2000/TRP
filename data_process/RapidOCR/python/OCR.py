# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/1 20:58
# software: PyCharm

"""
文件说明：
"""
import os

import cv2

# 基于onnxruntime引擎推理
import pandas as pd

from rapidocr_onnxruntime import RapidOCR

# 基于openvino引擎推理
# from rapidocr_openvino import RapidOCR

rapid_ocr = RapidOCR()



#cur_path = "E:\TRP\data"
cur_path = "..\\..\\..\\data"
if __name__ == "__main__":
    for num in range(1, 21):
        texts = []
        print(num)
        file_path = "\\reports\\" + str(num) + "\\" + "app" + str(num)+".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        # download screenshots of all reports and return the local image path
        length = len(number)
        matrix = [[0 for i in range(length)]for j in range(length)]
        for i in range(length):
            index1 = number[i]
            tmp1 = images[i].split('.')
            path1 = os.path.join(cur_path, "reports", str(num), "images", str(index1) + '.' + tmp1[len(tmp1) - 1])
            img = cv2.imread(path1)
            result = rapid_ocr(img)
            res = str(index1) + "&"
            for text in result[0]:
                res += text[1]
            print(res)
            texts.append(res)
        path = "..\\..\\..\\output\\" + str(num) + "\\" + "text.txt"
        f = open(path, "w",encoding="utf-8")
        for i in range(length):
            f.write(texts[i] + "\n",)
        f.close()


