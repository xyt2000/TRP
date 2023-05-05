# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/11 18:33
# software: PyCharm

"""
文件说明：
""""""
文件说明：
"""
import math

import cv2
import numpy as np
def get_average(records):
    return sum(records) / len(records)


def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)


def get_standard_deviation(records):
    variance = get_variance(records)
    return math.sqrt(variance)

def get_z_score(records):
    avg = get_average(records)
    stan = get_standard_deviation(records)
    scores = [(i-avg)/stan for i in records]
    return scores

def get_distance_chi(vec1, vec2):
    vec1 = np.asarray(vec1, np.float)
    vec2 = np.asarray(vec2, np.float)
    res = 0
    for i in range(len(vec1)):
        if vec1[i] == vec2[i] and vec1[i] == 0:
            res += 0
        else:
            res += (vec1[i]-vec2[i])*(vec1[i]-vec2[i])/(vec1[i]+vec2[i])
    return 1 / (res/2)

def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist
for num in range(1, 21):
    path1 = "E:\TRP\output\\" + str(num) + "\\" + "spm.txt"
    f1 = open(path1, "r")
    spms = []
    for line1 in f1.readlines():
        line1 = line1[1:-2].replace("\n","")
        spms.append(line1.split(", "))
    spms_ = []
    for spm in spms:
        spms_.append(list(map(float,spm)).copy())

    f1.close()
    spm_res = [[0 for i in range(len(spms))] for j in range(len(spms))]
    for i in range(len(spms)):
        spm_res[i][i] = 1
        for j in range(i+1, len(spms)):
            vec1 = np.array(spms_[i])
            vec2 = np.array(spms_[j])
            spm_res[i][j] = get_distance_chi(get_z_score(vec1),get_z_score(vec2))
            spm_res[j][i] = spm_res[i][j]
        print(i)

    path3 = "E:\TRP\output\\" + str(num) + "\\" + "spm_RES_new.txt"
    f3 = open(path3,"w")
    for spm in spm_res:
        f3.write(str(spm)+"\n")
    f3.close()
