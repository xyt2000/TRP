# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/11 11:38
# software: PyCharm

"""
文件说明：
"""
from gensim.summarization import bm25


def gensim_bm25(path):
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
    #print(texts)
    corpus = texts
    bm25Model = bm25.BM25(corpus)
    sim_matrix = [[0 for i in range(len(texts))]for i in range(len(texts))]
    for i in range(len(texts)):
        text = texts[i]
        scores = bm25Model.get_scores(text)
        #print('测试句子：', text)
        for j in range(len(scores)):
            sim_matrix[i][j] = scores[j]
    return sim_matrix





