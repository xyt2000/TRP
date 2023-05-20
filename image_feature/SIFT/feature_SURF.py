# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/2 13:33
# software: PyCharm

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

    # Draw first 100 matches.
    img3 = cv2.drawMatches(image_a, kp1, image_b, kp2, matches[:387], None, flags=2)

    return bgr_rgb(img3)


def get_surf(img1):
    sift = cv2.xfeatures2d.SURF_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    return des1

def get_distance(des1, des2):
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = [[m] for m, n in matches if m.distance < 0.9 * n.distance]

    # cv2.drawMatchesKnn expects list of lists as matches.
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

    return len(good) / len(matches)
def sift_detect(img1, img2, detector='surf'):
    if detector.startswith('si'):
        #print("sift detector......")
        sift = cv2.xfeatures2d.SIFT_create()
    else:
        #print("surf detector......")
        sift = cv2.xfeatures2d.SURF_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = [[m] for m, n in matches if m.distance < 0.9 * n.distance]

    # cv2.drawMatchesKnn expects list of lists as matches.
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

    return len(good) / len(matches)


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
            deses.append(get_surf(image_a))
        print(num)
        length = len(number)
        matrix = [[0 for i in range(length)] for j in range(length)]
        for i in range(length):
            matrix[i][i] = 1
            for j in range(i + 1, length):
                try:
                    matrix[i][j] = get_distance(deses[i], deses[j])
                    matrix[j][i] = matrix[i][j]
                except:
                    matrix[i][j] = -1
                    print(i + "," + j + "false")
            print(matrix[i])
        path = "..\\..\\output\\" + str(num) + "\\" + "surf.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(matrix[i]) + "\n")
        f.close()
    """
    # load image
    image_a = cv2.imread('E:\TRP\images\\0.png')
    image_b = cv2.imread('E:\TRP\images\\0.png')

    """
    # SIFT or SURF
    # print(sift_detect(image_a, image_b, detector="sift"))

    # ORB
    # img = orb_detect(image_a, image_b)


    # plt.imshow(img)
    # plt.show()
