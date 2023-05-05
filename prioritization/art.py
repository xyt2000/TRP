# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/7 17:25
# software: PyCharm

"""
文件说明：
"""
import random
import sys
# 输入为向量矩阵，转为距离矩阵：


# 输入为距离矩阵，输出art排序结果
from collections import defaultdict

import numpy as np


def get_sim_matrix(feature_matrix):
    height = len(feature_matrix)
    sim_matrix = [[0 for _ in range(height)]for _ in range(height)]
    for i in range(height):
        for j in range(height):
            sim_matrix[i][j] = get_distance(feature_matrix[i],feature_matrix[j])
    return sim_matrix


def get_distance(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.sqrt(np.sum((v1 - v2) ** 2))


def art_distance_matrix(sim_matrix):
    num = len(sim_matrix)
    select = []
    suite = [i for i in range(num)]
    first = random.randint(0, len(sim_matrix)-1)
    select.append(first)
    suite.remove(first)
    while len(suite) != 0:
        candidate = defaultdict(int)
        for r1 in suite:
            temp = sys.maxsize
            for r2 in select:
                if sim_matrix[r1][r2] < temp:
                    temp = sim_matrix[r1][r2]
                    candidate[r1] = temp
        sort = sorted(candidate.items(), key=lambda x: x[1], reverse=True)
        select_case = int(sort[0][0])
        select.append(select_case)
        suite.remove(select_case)
    return select

def art_sim_matrix(sim_matrix):
    num = len(sim_matrix)
    select = []
    suite = [i for i in range(num)]
    first = random.randint(0,len(sim_matrix)-1)
    select.append(first)
    suite.remove(first)
    while len(suite) != 0:
        candidate = defaultdict(int)
        for r1 in suite:
            temp = -100000000
            for r2 in select:
                if sim_matrix[r1][r2] > temp:
                    temp = sim_matrix[r1][r2]
                    candidate[r1] = temp
        sort = sorted(candidate.items(), key=lambda x: x[1])
        select_case = int(sort[0][0])
        select.append(select_case)
        suite.remove(select_case)
    return select


def art_distance_matrix_new(sim_matrix):
    """
    选择离其他元素最远的那个做第一个
    :param sim_matrix:
    :return:
    """
    num = len(sim_matrix)
    select = []
    suite = [i for i in range(num)]
    first = select_max_distance(sim_matrix)
    select.append(first)
    suite.remove(first)
    while len(suite) != 0:
        candidate = defaultdict(int)
        for r1 in suite:
            temp = sys.maxsize
            for r2 in select:
                if sim_matrix[r1][r2] < temp:
                    temp = sim_matrix[r1][r2]
                    candidate[r1] = temp
        sort = sorted(candidate.items(), key=lambda x: x[1],reverse=True)
        select_case = int(sort[0][0])
        select.append(select_case)
        suite.remove(select_case)
    return select

def art_sim_matrix_new(sim_matrix):
    """
    选择离其他元素最远的那个做第一个
    :param sim_matrix:
    :return:
    """
    num = len(sim_matrix)
    select = []
    suite = [i for i in range(num)]
    first = select_max_sim(sim_matrix)
    select.append(first)
    suite.remove(first)
    while len(suite) != 0:
        candidate = defaultdict(int)
        for r1 in suite:
            temp = -100000000
            for r2 in select:
                if sim_matrix[r1][r2] > temp:
                    temp = sim_matrix[r1][r2]
                    candidate[r1] = temp
        sort = sorted(candidate.items(), key=lambda x: x[1])
        select_case = int(sort[0][0])
        select.append(select_case)
        suite.remove(select_case)
    return select

def select_max_distance(matrix):
    max_ = defaultdict(int)
    for i in range(len(matrix)):
        temp = sys.maxsize
        for j in range(len(matrix)):
            if j != i:
                if matrix[i][j] < temp:
                    temp = matrix[i][j]
                    max_[i] = temp
    sort = sorted(max_.items(), key=lambda x:x[1], reverse=True)
    return sort[0][0]

def select_max_sim(matrix):
    max_ = defaultdict(int)
    for i in range(len(matrix)):
        temp = -sys.maxsize
        for j in range(len(matrix)):
            if j != i:
                if matrix[i][j] > temp:
                    temp = matrix[i][j]
                    max_[i] = temp
    sort = sorted(max_.items(), key=lambda x:x[1])
    return sort[0][0]


