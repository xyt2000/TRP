# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/6 11:19
# software: PyCharm

"""
文件说明：
"""
from collections import defaultdict


import numpy as np
from gensim.models import ldamodel
from gensim import corpora
from gensim.similarities import MatrixSimilarity


def get_sim_matrix(feature_matrix):
    height = len(feature_matrix)
    sim_matrix = [[0 for _ in range(height)]for _ in range(height)]
    for i in range(height):
        for j in range(height):
            sim_matrix[i][j] = get_distance(feature_matrix[i],feature_matrix[j])
    return sim_matrix


def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist

def get_distance(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.sqrt(np.sum((v1 - v2) ** 2))

def lda_pro_paper(path, num):
    """
    相似度矩阵
    :param path:
    :param num:
    :return:
    """
    texts = []
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            texts.append([])
        else:
            words = line.split(" ")
            texts.append(words)
            for word in words:
                word_list.append(word)
    # 去掉只出现一次的单词
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    num_t = num
    lda = ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_t)
    lda.show_topics()
    # 保存模型
    # lda.save('zhutimoxing.model')
    # 加载模型
    # lda = ldamodel.LdaModel.load('zhutimoxing.model')
    # 最后得出属于这三个主题的概率为[(4, 0.6081926), (11, 0.1473181), (12, 0.13814318)]
    feature_matrix_paper = [[0 for _ in range(num_t)] for _ in range(len(texts))]
    # 论文做法
    for i in range(len(texts)):
        if len(texts[i]) != 0:
            point = 1 / len(texts[i])
            for word in texts[i]:
                word_pro = lda.get_term_topics(dictionary.token2id[word], minimum_probability=0.0000001)
                sort = sorted(word_pro, key=lambda x:x[1], reverse=True)
                feature_matrix_paper[i][sort[0][0]] += point
    dicts = get_sim_matrix(feature_matrix_paper)
    return dicts

if __name__ == "__main__":
    lda_pro_paper("E:\TRP\data\\reports\\1\\1_text_words.txt", 30)

