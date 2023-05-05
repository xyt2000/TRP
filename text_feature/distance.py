# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/14 11:03
# software: PyCharm

"""
文件说明：
"""
import numpy as np


def get_sim_matrix(feature_matrix, distance="cos"):
    height = len(feature_matrix)
    sim_matrix = [[0 for _ in range(height)]for _ in range(height)]
    for i in range(height):
        for j in range(height):
            if distance == "cos":
                sim_matrix[i][j] = get_distance_cos(feature_matrix[i],feature_matrix[j])
            else:
                sim_matrix[i][j] = get_distance(feature_matrix[i], feature_matrix[j])
    return sim_matrix


def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist

def get_distance(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.sqrt(np.sum((v1 - v2) ** 2))