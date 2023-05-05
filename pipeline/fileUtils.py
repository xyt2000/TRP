# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/31 21:03
# software: PyCharm

"""
文件说明：
"""


def write_path(path1, path2, num, matrix):
    """
    :param path1: 1
    :param path2: 2
    :param num: app
    :param matrix: data
    :return:
    """
    path = "../early_data//"+path1+"//" + str(num) + "/" + path2 + ".txt"
    f = open(path, "w")
    for line in matrix:
        f.write(str(line) + "\n")
    f.close()

def read_path(path1, path2, num):
    """
    :param path1: 1
    :param path2: 2
    :param num: app
    :param matrix: data
    :return:
    """
    path = "E:\TRP\early_data\\"+path1+"\\" + str(num) + "\\" + path2 + ".txt"
    f1 = open(path, "r")
    reses = []
    for line1 in f1.readlines():
        line1 = line1[1:-2].replace("\n", "")
        reses.append(line1.split(", "))
    matrix = []
    for res in reses:
        matrix.append(list(map(float, res)).copy())
    return matrix