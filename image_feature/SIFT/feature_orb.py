# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/2 13:39
# software: PyCharm

"""
文件说明：
"""
"""
文件说明：
"""
# coding: utf-8
import os

import pandas as pd
from matplotlib import pyplot as plt
import cv2

print('cv version: ', cv2.__version__)


def bgr_rgb(img):
    (r, g, b) = cv2.split(img)
    return cv2.merge([b, g, r])

def get_orb(image_a):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(image_a, None)
    return des1

def get_distance(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)
    # good = [[m] for m, n in matches if m.distance < 0.9 * n.distance]
    # Sort them in the order of their distance.
    # matches = sorted(matches, key=lambda x: x.distance)
    distances = 0
    for match in matches:
        distances += match.distance
    distances = distances / len(matches)
    # Draw first 100 matches.
    return distances

def orb_detect(image_a, image_b):
    # feature match
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(image_a, None)
    kp2, des2 = orb.detectAndCompute(image_b, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)
    # good = [[m] for m, n in matches if m.distance < 0.9 * n.distance]
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    distances = 0
    for match in matches:
        distances += match.distance
    distances = distances / len(matches)
    # Draw first 100 matches.
    return distances



if __name__ == "__main__":

    cur_path = "..\\..\\data"

    for num in range(1, 21):
        deses = []
        file_path = "\\reports\\" + str(num) + "\\" + "app" + str(num) + ".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        for i in range(len(number)):
            index1 = number[i]
            tmp1 = images[i].split('.')
            path1 = os.path.join(cur_path, "reports", str(num), "images", str(index1) + '.' + tmp1[len(tmp1) - 1])
            image_a = cv2.imread(path1)
            deses.append(get_orb(image_a))
        print(num)
        length = len(number)
        matrix = [[0 for i in range(length)] for j in range(length)]
        for i in range(length):
            matrix[i][i] = 0
            for j in range(i + 1, length):
                try:
                    matrix[i][j] = get_distance(deses[i], deses[j])
                    matrix[j][i] = matrix[i][j]
                except:
                    matrix[i][j] = -1
                    print(i + "," + j + "false")
            print(matrix[i])
        path = "..\\..\\output\\" + str(num) + "\\" + "orb.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(matrix[i]) + "\n")
        f.close()
