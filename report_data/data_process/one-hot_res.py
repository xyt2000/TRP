# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/2/27 22:53
# software: PyCharm

"""
文件说明：
"""
import cv2
import numpy as np

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
    path1 = "E:\TRP\output\\" + str(num) + "\\" + "one_hot_word.txt"
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
            spm_res[i][j] = get_distance_chi(vec1,vec2)
            spm_res[j][i] = spm_res[i][j]
        print(i)

    path3 = "E:\TRP\output\\" + str(num) + "\\" + "one_hot_res.txt"
    f3 = open(path3,"w")
    for spm in spm_res:
        f3.write(str(spm)+"\n")
    f3.close()