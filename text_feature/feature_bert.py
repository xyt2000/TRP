# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/11 17:35
# software: PyCharm

"""
文件说明：
"""
# -*- coding:utf-8 -*-
import numpy as np
from bert_serving.client import BertClient
from scipy import linalg
# 先命令行启动服务
# bert-serving-start -model_dir E:\TRP\model\chinese_L-12_H-768_A-12 -num_worker=1

# print(vec1)
def compute_kernel_bias(vecs, n_components=256):
    """计算kernel和bias
    vecs.shape = [num_samples, embedding_size]，
    最后的变换：y = (x + bias).dot(kernel)
    """
    mu = vecs.mean(axis=0, keepdims=True)
    cov = np.cov(vecs.T)
    u, s, vh = linalg.svd(cov)
    W = np.dot(u, np.diag(1 / np.sqrt(s)))
    return W[:, :n_components], -mu


def transform_and_normalize(vecs, kernel=None, bias=None):
    """ 最终向量标准化
    """
    if not (kernel is None or bias is None):
        vecs = (vecs + bias).dot(kernel)
    return vecs / (vecs**2).sum(axis=1, keepdims=True)**0.5

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

def get_distance(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.sqrt(np.sum((v1 - v2) ** 2))

def bert(path):
    bc = BertClient(check_length=False)
    texts = []
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        raw_list.append(line)
    vec1 = bc.encode(raw_list)
    v_data = np.array(vec1)
    # kernel,bias=compute_kernel_bias(v_data,700)
    # v_data=transform_and_normalize(v_data, kernel=kernel, bias=bias)
    # print(v_data)
    sim_matrix = get_sim_matrix(v_data)
    return sim_matrix

if __name__ == "__main__":
    for num in range(1,21):
        path = "E:\TRP\data\\reports"+"\\"+str(num)+"\\"+str(num)+"_text_words.txt"
        bc = BertClient(check_length=False)
        texts = []
        f = open(path, "r")
        raw_list = []
        word_list = []
        for line in f.readlines():
            line = line.replace("\n", "")
            raw_list.append(line)
        vec1 = bc.encode(raw_list)
        vec1 = vec1.tolist()
        path = "E:\TRP\output" + "\\" + str(num) + "\\"+ "bert_vector.txt"
        f = open(path,"w")
        for line in vec1:
            f.write(str(line)+"\n")
        f.close()