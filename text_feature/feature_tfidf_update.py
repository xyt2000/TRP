# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/11 22:01
# software: PyCharm

"""
文件说明：
"""
import math
from collections import defaultdict

import numpy as np


def tf_idf(raw_list, k, b):
    len_c = 0
    word_in_doc = defaultdict(list)
    word_dict = defaultdict(int)
    num1 = 0
    num2 = 0
    word_list = []
    for raw in raw_list:
        raw = raw.replace("\n","")
        words = raw.split(" ")
        for word in words:
            word_in_doc[word].append(num1) #num1表示词在哪些文档存
            if word not in word_list:
                word_list.append(word)
                word_dict[word] = num2 #num2表示词汇表
                num2 += 1
        num1 += 1
        len_c += len(raw)
    len_c = len_c // len(raw_list)
    dicts = []
    for raw in raw_list:
        dict = [0 for i in range(len(word_list))]
        raw = raw.replace("\n","")
        words = raw.split(" ")
        raw_word_dict = defaultdict(int)
        for word in words:
            raw_word_dict[word] += 1
        for word in raw_word_dict.keys():
            x = raw_word_dict[word] / len(words)
            tf = (k * x) / (x + k*(1-b+b*(len(raw)/len_c)))
            idf = math.log((len(raw_list)+1)/(len(word_in_doc[word])+0.5))
            dict[word_dict[word]] = tf * idf
        dicts.append(dict)
    return dicts


def get_sim_matrix(feature_matrix):
    height = len(feature_matrix)
    sim_matrix = [[0 for _ in range(height)]for _ in range(height)]
    for i in range(height):
        for j in range(height):
            sim_matrix[i][j] = get_distance_cos(feature_matrix[i],feature_matrix[j])
    return sim_matrix


def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist


def tf_idf_update(path):
    """
    输出cos距离矩阵 类似相似度矩阵
    :param path:
    :return:
    """
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        raw_list.append(line)
    dicts = tf_idf(raw_list, 1, 0.3)
    sim_matrix = get_sim_matrix(dicts)
    return sim_matrix

def write_tf_idf_update(path):
    """
    输出cos距离矩阵 类似相似度矩阵
    :param path:
    :return:
    """
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        raw_list.append(line)
    dicts = tf_idf(raw_list, 1, 0.3)
    return dicts

def tf_idf_update_image(path):
    """
    输出cos距离矩阵 类似相似度矩阵
    :param path:
    :return:
    """
    f = open(path, "r",encoding="utf-8")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        raw_list.append(line)
    dicts = tf_idf(raw_list, 1, 0.3)
    sim_matrix = get_sim_matrix(dicts)
    return sim_matrix

if __name__ == '__main__':
    for num in range(1,21):
        path = "E:\TRP\output"+"\\"+str(num)+"\\"+"use_text.txt"
        texts = write_tf_idf_update(path)
        path = "E:\TRP\output" + "\\" + str(num) + "\\"+ "ocr_tfidf_vector.txt"
        f = open(path,"w")
        for line in texts:
            f.write(str(line)+"\n")
        f.close()