# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/5/4 14:37
# software: PyCharm

"""
文件说明：
"""
import numpy as np

from evaluate.apfd import get_apfd
from prioritization.additional import additional
from prioritization.art import art_distance_matrix, art_sim_matrix, art_distance_matrix_new, art_sim_matrix_new
from text_feature.feature_tfidf_update import tf_idf_update, tf_idf_update_image

def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist

def read_matrix(path1):
    f1 = open(path1, "r")
    matrix = []
    for line1 in f1.readlines():
        line1 = line1.replace("\n", "")
        line1 = line1[1:-1]
        matrix.append(line1.split(", "))
    res = []
    for line in matrix:
        res.append(list(map(float, line)).copy())
    sim_res = [[0 for i in range(len(res))] for j in range(len(res))]
    for i in range(len(res)):
        sim_res[i][i] = 1
        for j in range(i + 1, len(res)):
            vec1 = np.array(res[i])
            vec2 = np.array(res[j])
            sim_res[i][j] = get_distance_cos(vec1, vec2)
            sim_res[j][i] = sim_res[i][j]
    return sim_res

solutions = ["ae_7"]
for num in range(1,21):
    #print(num)
    apfd_sum = []
    for i in range(1):
        apfds = []
        for solution in solutions:
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            data_path = "../early_data/fillzeroAE/"+ str(num) + "/"
            distance_matrix = []
            sim_matrix = []
            one_hot_matrix = []
            sequence = []

            data_path += solution + ".txt"

            sim_matrix = read_matrix(data_path)
            if len(distance_matrix) != 0:
                sequence = art_distance_matrix_new(distance_matrix)
            if len(sim_matrix) != 0:
                sequence = art_sim_matrix_new(sim_matrix)
            if len(one_hot_matrix) != 0:
                sequence = additional(one_hot_matrix)

            # print(algorithm)
            # print(sequence)
            # print("apfd:")

            apfd = get_apfd(app_path, sequence)
            print(apfd)
            apfds.append(apfd)
        apfd_sum.append(apfds)
    apfd_avg = []
    for j in range(len(apfd_sum[0])):
        apfd = 0
        for i in range(len(apfd_sum)):
            apfd += apfd_sum[i][j]
        apfd_avg.append(apfd / len(apfd_sum))