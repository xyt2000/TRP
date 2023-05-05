# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/14 11:14
# software: PyCharm

"""
文件说明：
矩阵归一化
"""
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

from evaluate.apfd import get_apfd
from pipeline.fileUtils import write_path
from prioritization.art import art_sim_matrix_new
from text_feature.distance import get_distance_cos, get_sim_matrix


def normalization_z(data):
    """
    归一化处理 z
    :return:None
    """
    return preprocessing.scale(data)


def normalization_minmax(data):
    """
    归一化处理 minmax
    :return:None
    """
    # 归一化到[0,1]
    data = np.array(data)
    mm = MinMaxScaler((0, 1))
    data = mm.fit_transform(data)
    return data.tolist()

import math


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


def vector_add(features, num):
    sum_matrix = []
    for i in range(len(features)):
        word_path = "../output//" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))

            line = get_z_score(line)
            matrix.append(line)
        matrix = normalization_minmax(matrix)
        if i == 0:
            sum_matrix = matrix
        else:
            add_matrix(sum_matrix,matrix)
    return sum_matrix


def vector_add_new(features, num, path1):
    sum_matrix = []
    for i in range(len(features)):
        word_path = "../early_data/"+path1+"/"+ "/" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))

            # line = get_z_score(line) 要不要归一化
            matrix.append(line)
        if i == 0:
            sum_matrix = matrix
        else:
            sum_matrix = add_matrix(sum_matrix,matrix)
    return sum_matrix

def vector_cat_new(features, num, path):
    sum_matrix = []
    for i in range(len(features)):
        word_path = "../early_data/"+path+ "/" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))

            line = get_z_score(line)
            matrix.append(line)
        if i == 0:
            sum_matrix = matrix
        else:
            sum_matrix = cat_matrix(sum_matrix,matrix)
    return sum_matrix

def add_matrix(matrix1,matrix2):
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            matrix1[i][j] = matrix1[i][j] + matrix2[i][j]
    return matrix1

def cat_matrix(matrix1,matrix2):
    for i in range(len(matrix1)):
        matrix1[i] = matrix1[i] + matrix2[i]
    return matrix1
if __name__ == '__main__':
    test1 = ["ocr_tfidf_vector", "tfidf_vector"]
    test2 = ["bert_vector", "word2vec_vector"]
    test3 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector"]
    test4 = ["gist", "CEDD"]
    test5 = ["gist", "CEDD", "spm"]
    test6 = ["gist", "CEDD", "color", "spm"]
    test7 = ["bert_vector", "word2vec_vector", "gist", "CEDD", "spm"]
    test8 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "spm"]
    test9 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD", "spm"]
    test10 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD", "color", "spm"]
    test11 = ["word2vec_vector","spm"]
    #all_list = [test1,test2,test3,test4,test5,test6,test7,test8,test9,test10,test11]
    all_list = test9
    matrix = []
    #for uses in all_list:
    uses =  all_list
    print(uses)
    for num in range(1,21):
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            matrix = vector_cat_new(uses, num, "pca")
            matrix = get_sim_matrix(matrix)
            sequence = art_sim_matrix_new(matrix)
            apfd = get_apfd(app_path, sequence)
            print(apfd)
