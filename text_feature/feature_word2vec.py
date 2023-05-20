# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/3 22:30
# software: PyCharm

"""
文件说明：

"""
import pandas as pd
import re
import jieba
import os
import numpy as np
from gensim.models import word2vec

# step 1: segmentation
# step 2: remove stop words
# step 3:  SYNONYM REPLACEMENT
# perform word segment and return word token list
from gensim.models import Word2Vec
from text_feature.distance import get_distance_cos, get_distance, get_sim_matrix

def train(path):
    f = open(path, "r",encoding="utf-8")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for word in words:
                word_list.append(word)
    print(word_list)
    model = word2vec.Word2Vec(raw_list, hs=1, min_count=1, window=3, size=100, iter=1000)
    print(model.get_latest_training_loss())
    model.save('ocr.model')
    # 保存模型
#train("E:\TRP\data\ocr_texts")
def my_word2vec(path, model_path):
    """
    测试自己的模型
    :param path:
    :return:
    """
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for word in words:
                word_list.append(word)
    # print(word_list)
    # model = word2vec.Word2Vec(raw_list, hs=1, min_count=1, window=3, size=100, iter=1000)
    # print(model.get_latest_training_loss())
    # model.save('data.model')
    # 保存模型
    model = Word2Vec.load(model_path)
  #  for val in model.wv.similar_by_word("打开", topn=10):
   #     print(val[0], val[1])
    vecs = []
    for res in raw_list:
        if len(res) != 0 :
            words = res
            v = np.zeros(100)
            length = len(words)
            for word in words:
                try:
                    v += model[word]
                except:
                    length -= 1
            if length == 0:
                length += 1
            v /= length
        else:
            v = np.zeros(100)
        vecs.append(v)
    dicts = get_sim_matrix(vecs)
    return dicts

def write_word2vec(path, model_path):
    """
    :param path:
    :return:
    """
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for word in words:
                word_list.append(word)
    # print(word_list)
    # model = word2vec.Word2Vec(raw_list, hs=1, min_count=1, window=3, size=100, iter=1000)
    # print(model.get_latest_training_loss())
    # model.save('data.model')
    # 保存模型
    model = Word2Vec.load('E:\TRP\\text_feature\\'+model_path)
  #  for val in model.wv.similar_by_word("打开", topn=10):
   #     print(val[0], val[1])
    vecs = []
    for res in raw_list:
        if len(res) != 0 :
            words = res
            v = np.zeros(100)
            length = len(words)
            for word in words:
                try:
                    v += model[word]
                except:
                    length -= 1
            if length == 0:
                length += 1
            v /= length
        else:
            v = np.zeros(100)
        vecs.append(v)
    return vecs

def other_word2vec(path):
    """
    测试别人的模型
    :param path:
    :return:
    """
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for word in words:
                word_list.append(word)
    # print(word_list)
    # model = word2vec.Word2Vec(raw_list, hs=1, min_count=1, window=3, size=100, iter=1000)
    # print(model.get_latest_training_loss())
    # model.save('data.model')
    # 保存模型
    model = Word2Vec.load('E:\TRP\model\\baike_26g_news_13g_novel_229g.model')
    #for val in model.wv.similar_by_word("打开", topn=10):
    #     print(val[0], val[1])
    vecs = []
    vec_len = len(model["打开"])
    #print(vec_len)
    for res in raw_list:
        if len(res) != 0 :
            words = res
            v = np.zeros(vec_len)
            length = len(words)
            for word in words:
                try:
                    v += model[word]
                except:
                    length -= 1
            if length == 0:
                length += 1
            v /= length
        else:
            v = np.zeros(vec_len)
        vecs.append(v)
    #print(vecs)
    dicts = get_sim_matrix(vecs, "cos")
    return dicts



# print(other_word2vec("E:\TRP\data\\all_text_words.txt"))
if __name__ == "__main__":
    for num in range(1,21):
        path = "E:\TRP\data\\reports"+"\\"+str(num)+"\\"+str(num)+"_text_words.txt"
        texts = write_word2vec(path,"data.model")
        for i in range(len(texts)):
            texts[i] = texts[i].tolist()
        path = "E:\TRP\output" + "\\" + str(num) + "\\"+ "word2vec_vector.txt"
        f = open(path,"w")
        for line in texts:
            f.write(str(line)+"\n")
        f.close()