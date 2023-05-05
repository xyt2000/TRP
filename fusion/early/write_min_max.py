# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/31 20:38
# software: PyCharm

"""
文件说明：
写入minmax
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


def write_min_max(features, num):
    sum_matrix = []
    for i in range(len(features)):
        word_path = "../early_data/pca/" + str(num) + "/" + features[i] + ".txt"
        matrix = []
        f = open(word_path, "r")
        for line in f.readlines():
            line = line.replace("\n", "")
            line = line[1:-1]
            line = line.split(", ")
            line = list(map(float, line))

            # line = get_z_score(line)
            matrix.append(line)
        matrix = normalization_minmax(matrix)
        write_path("pca_minmax", features[i], num, matrix)
    return sum_matrix

if __name__ == '__main__':
    test1 = ["ocr_tfidf_vector", "tfidf_vector"]
    test2 = ["bert_vector", "word2vec_vector"]
    test3 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector"]
    test4 = ["gist", "CEDD", "color", "spm"]
    test5 = ["gist", "CEDD", "color"]
    test6 = ["gist", "CEDD", "spm"]
    test7 = ["bert_vector", "word2vec_vector", "gist", "CEDD", "spm"]
    test8 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD", "spm"]
    test9 = ["gist", "CEDD", "color", "spm"]
    test10 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD", "color", "spm"]
    #all_list = [test1,test2,test3,test4,test5,test6,test7,test8,test9,test10]
    all_list = test10
    matrix = []
    for num in range(1,21):
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            matrix = write_min_max(all_list, num)
            print(num)
