# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/23 21:05
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



cur_path = "E:\TRP\data"
if __name__ == "__main__":
        img = cv2.imread("7.png")
        result = rapid_ocr(img)
        res = ""
        for text in result[0]:
                res += text[1]
        print(res)