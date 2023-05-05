# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/3 19:43
# software: PyCharm

"""
文件说明：
计算cedd color相似度矩阵
"""
import numpy as np


def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist
for num in range(1, 21):
    path1 = "E:\TRP\output\\" + str(num) + "\\" + "CEDD.txt"
    path2 = "E:\TRP\output\\" + str(num) + "\\" + "Color.txt"
    f1 = open(path1, "r")
    f2 = open(path2, "r")
    colors = []
    cedds = []
    for line1,line2 in list(zip(f1.readlines(),f2.readlines())):
        line1 = line1[1:-2].replace("\n","")
        line2 = line2[1:-2].replace("\n","")
        cedds.append(line1.split(", "))
        colors.append(line2.split(", "))
    cedds_ = []
    for cedd in cedds:
        cedds_.append(list(map(float,cedd)).copy())
    colors_ = []
    for color in colors:
        colors_.append(list(map(float,color)).copy())
    f1.close()
    f2.close()
    cedd_res = [[0 for i in range(len(cedds))] for j in range(len(cedds))]
    for i in range(len(cedds)):
        cedd_res[i][i] = 1
        for j in range(i+1, len(cedds)):
            vec1 = np.array(cedds_[i])
            vec2 = np.array(cedds_[j])
            cedd_res[i][j] = get_distance_cos(vec1, vec2)
            cedd_res[j][i] = cedd_res[i][j]
    color_res = [[0 for i in range(len(colors))] for j in range(len(colors))]
    for i in range(len(colors)):
        color_res[i][i] = 1
        for j in range(i + 1, len(colors)):
            vec1 = np.array(colors_[i])
            vec2 = np.array(colors_[j])
            color_res[i][j] = get_distance_cos(vec1, vec2)
            color_res[j][i] = color_res[i][j]



    path3 = "E:\TRP\output\\" + str(num) + "\\" + "CEDD_RES.txt"
    f3 = open(path3,"w")
    for cedd in cedd_res:
        f3.write(str(cedd)+"\n")
    f3.close()

    path4 = "E:\TRP\output\\" + str(num) + "\\" + "Color_RES.txt"
    f4 = open(path4, "w")
    for color in color_res:
        f4.write(str(color) + "\n")
    f4.close()