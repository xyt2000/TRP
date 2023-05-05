# contact: 1026310947@qq.com
# datetime:2023/1/3 12:41
# software: PyCharm

"""
文件说明：
"""
import numpy as np

def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist
for num in range(1, 21):
    path1 = "E:\TRP\output\\" + str(num) + "\\" + "ColorLayout.txt"
    path2 = "E:\TRP\output\\" + str(num) + "\\" + "ScalableColor.txt"
    path3 = "E:\TRP\output\\" + str(num) + "\\" + "EdgeHistogram.txt"
    f1 = open(path1, "r")
    f2 = open(path2, "r")
    f3 = open(path3, "r")
    colors = []
    mpeg7s = []
    for line1,line2 in list(zip(f1.readlines(),f2.readlines())):
        line1 = line1.replace("\n","")
        line2 = line2[1:-1]
        line1 = line1[:-1] + ", "+line2
        colors.append(line1)
    f1.close()
    f2.close()
    for line1, line2 in list(zip(colors, f3.readlines())):
        line2 = line2[1:-1]
        line1 = line1[:-1] + ", " + line2
        mpeg7s.append(line1)
    f3.close()  
    path4 = "E:\TRP\output\\" + str(num) + "\\" + "mpeg7.txt"
    f4 = open(path4,"w")
    for mpeg in mpeg7s:
        f4.write(mpeg+"\n")
    f4.close()
    mpeg7s_ = []
    for mpeg7 in mpeg7s:
        mpeg7s_.append(list(map(float, mpeg7[1:-1].split(","))).copy())
    mpeg7s_res = [[0 for i in range(len(mpeg7s_))] for j in range(len(mpeg7s_))]
    for i in range(len(mpeg7s_)):
        mpeg7s_res[i][i] = 1
        for j in range(i + 1, len(mpeg7s_)):
            vec1 = np.array(mpeg7s_[i])
            vec2 = np.array(mpeg7s_[j])
            mpeg7s_res[i][j] = get_distance_cos(vec1, vec2)
            mpeg7s_res[j][i] = mpeg7s_res[i][j]

    path3 = "E:\TRP\output\\" + str(num) + "\\" + "mpeg7_RES.txt"
    f3 = open(path3, "w")
    for mpeg7 in mpeg7s_res:
        f3.write(str(mpeg7) + "\n")
    f3.close()