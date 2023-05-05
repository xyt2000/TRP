# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/9 17:15
# software: PyCharm

"""
文件说明：
"""
import numpy as np
from matplotlib import pyplot as plt, ticker
from scipy.interpolate import make_interp_spline

from evaluate.apfd import get_apfd, get_apfd_items, get_apfd_items1
from pipeline.earlyfusion_sim import sim_cat
from prioritization.art import art_sim_matrix_new, art_sim_matrix
from text_feature.distance import get_distance_cos


def add_matrix(y,x):
    result = x
    for i in range(len(x)):
        for j in range(len(x[i])):
            result[i][j] = x[i][j] + y[i][j]
    return result


def dicts(features,num):
    """
    字典序
    :param features:
    :param num:
    :return:
    """
    Sequences = []
    for i in range(len(features)):
        word_path = "../output//" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))
            matrix.append(line)
        # 1、得到序列
        sequence = art_sim_matrix_new(matrix)
        Sequences.append(sequence)
    Prioritizations = []
    for i in range(len(Sequences)):
        prioritization = []
        for j in range(len(Sequences[0])):
            prioritization.append(Sequences[i].index(j)+1)
        Prioritizations.append(prioritization)
    # 2、得到每个用例的排位 按照从小到大顺序构成字典序
    import math
    length = int(math.log10(len(Sequences[0])))+1
    from collections import defaultdict
    Dicts = defaultdict(str)
    for i in range(len(Sequences[0])):
        Dict = []
        for j in range(len(Sequences)):
            Dict.append(Prioritizations[j][i])
        list.sort(Dict)
        dict_strings = ""
        for num in Dict:
            num = str(num)
            zero = length - len(num)
            zeros = ""
            for m in range(zero):
                zeros += "0"
            dict_string = zeros + num
            dict_strings += dict_string
        Dicts[i] = dict_strings
    # 3、通过排序字典序得到结果
    sort = sorted(Dicts.items(),key= lambda x:x[1])
    res = []
    for j in range(len(sort)):
        res.append(sort[j][0])
    return res


def average(features, num):
    """
    平均排序
    :param features:
    :param num:
    :return:
    """
    Sequences = []
    for i in range(len(features)):
        word_path = "../output//" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))
            matrix.append(line)
        # 1、得到序列
        sequence = art_sim_matrix_new(matrix)
        Sequences.append(sequence)
    Prioritizations = []
    import math
    from collections import defaultdict
    Dicts = defaultdict(int)
    for i in range(len(Sequences)):
        prioritization = []
        for j in range(len(Sequences[0])):
            prioritization.append(Sequences[i].index(j)+1)
        Prioritizations.append(prioritization)
    # 2、得到每个用例的排位 按照从小到大顺序构成字典序
    for i in range(len(Sequences[0])):
        Dict = []
        for j in range(len(Sequences)):
            Dict.append(Prioritizations[j][i])
        Dicts[i] = sum(Dict)/len(Dict)
    # 3、通过排序字典序得到结果
    sort = sorted(Dicts.items(),key= lambda x:x[1])
    res = []
    for j in range(len(sort)):
        res.append(sort[j][0])
    return res





