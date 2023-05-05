# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/6 20:52
# software: PyCharm

"""
文件说明：
"""
import gensim
import pandas as pd
from gensim import similarities

def tfidf(path):
    """
    返回相似度矩阵
    :param path:
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
    # print(texts)
    dictionary = gensim.corpora.Dictionary(texts)
    # 词库，以（词，词频方式存储）
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = gensim.models.TfidfModel(corpus)
    # 使用tfidf模型将自身的词库转换成tf-idf表示
    corpus_tfidf = tfidf[corpus]
    feature_cnt = len(dictionary.token2id)

    # 构建距离矩阵
    sim_matrix = [[0 for _ in range(len(texts))] for _ in range(len(texts))]
    for i in range(len(texts)):
        kw_vector = dictionary.doc2bow(texts[i])
        # 6、对【稀疏向量集】建立【索引】
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
        # 7、相似度计算
        sim = index[tfidf[kw_vector]]
        for j in range(len(sim)):
            sim_matrix[i][j] = round(sim[j], 6)
    return sim_matrix


def wirte_tfidf(path):
    """
    返回相似度矩阵
    :param path:
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
    # print(texts)
    dictionary = gensim.corpora.Dictionary(texts)
    # 词库，以（词，词频方式存储）
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = gensim.models.TfidfModel(corpus)
    # 使用tfidf模型将自身的词库转换成tf-idf表示
    corpus_tfidf = tfidf[corpus]
    index = 1
    matrix = [[0 for _ in range(len(dictionary))] for _ in range(len(corpus))]
    for i in range(len(corpus_tfidf)):
        for tuple in corpus_tfidf[i]:
            matrix[i][tuple[0]] = tuple[1]
    return matrix
