# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/10 22:34
# software: PyCharm

"""
文件说明：
"""
# Author Hans

import sys
import gensim
import jieba
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from jieba import analyse

TaggededDocument = gensim.models.doc2vec.TaggedDocument


def jieba_cut(content, stop_words):
    '''jieba精准分词(常用)

    :param content: 要分词的句子
    :param stop_words: 停用词集合或者列表
    :return: 返回一个列表，包含content所分出来的词
    '''

    word_list = []

    if content != '' and content is not None:
        seg_list = jieba.cut(content)
        for word in seg_list:
            if word not in stop_words:
                word_list.append(word)

    return word_list


def get_fencihou_dataset(path):
    f = open(path, 'r', encoding='gbk')
    lines = f.readlines()
    corpus = []
    documents = []

    # 建立语料库list文件（list中是已经分词后的）
    for i, each in enumerate(lines):
        text = list(each.replace('\n', '').split(' '))
        # print(text)
        document = TaggededDocument(text, tags=[i])
        corpus.append(document)
    print('语料库句子数：', len(corpus))

    return corpus


def train(x_train, model_path, size=200, epoch_num=100, dm=1):
    # print('开始训练')
    model_dm = Doc2Vec(x_train, min_count=1, window=3, vector_size=size, sample=1e-3, negative=3, workers=4, dm=dm)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=epoch_num)
    model_dm.save(model_path)
    # print('训练结束')

    return model_dm


def testDoc(model_path, str,num):
    model_dm = Doc2Vec.load(model_path)
    test_text = str.split(" ")
    #print('test_text:', test_text)
    inferred_vector_dm = model_dm.infer_vector(test_text)
    #print('inferred_vector_dm:', inferred_vector_dm)
    # Gensim 中有内置的 most_similar，得到向量后，可以计算相似性
    sims = model_dm.docvecs.most_similar([inferred_vector_dm],topn=num)

    return sims

def doc2vec(path):
    """
    返回相似度矩阵
    :param path:
    :return:
    """
    model_path = 'doc2vec_model_sum.model'
    f = open(path, 'r', encoding='gbk')
    lines = f.readlines()
    corpus = []
    documents = []
    texts = []
    # 建立语料库list文件（list中是已经分词后的）
    for i, each in enumerate(lines):
        texts.append(each)
        text = list(each.replace('\n', '').split(' '))
        # print(text)
        document = TaggededDocument(text, tags=[i])
        corpus.append(document)
    # 训练数据
    model_dm = train(corpus, model_path=model_path,epoch_num=2000)
    sim_matrix = [[0 for _ in range(len(texts))] for _ in range(len(texts))]
    for m in range(len(texts)):
        text = texts[m].replace("\n", "")
        sims = testDoc(model_path=model_path, str=text, num=len(corpus))
        for tu in sims:
            sim_matrix[m][tu[0]] = tu[1]
    return sim_matrix

def doc2vec_use(path):
    """
    返回相似度矩阵
    :param path:
    :return:
    """
    model_path = 'doc2vec_model.model'
    f = open(path, 'r', encoding='gbk')
    lines = f.readlines()
    corpus = []
    documents = []
    texts = []
    # 建立语料库list文件（list中是已经分词后的）
    for i, each in enumerate(lines):
        texts.append(each)
        text = list(each.replace('\n', '').split(' '))
        # print(text)
        document = TaggededDocument(text, tags=[i])
        corpus.append(document)
    # 训练数据
    # model_dm = train(corpus, model_path=model_path,epoch_num=1000)
    sim_matrix = [[0 for _ in range(len(texts))] for _ in range(len(texts))]
    for m in range(len(texts)):
        text = texts[m].replace("\n", "")
        sims = testDoc(model_path=model_path, str=text, num=len(corpus))
        for tu in sims:
            sim_matrix[m][tu[0]] = tu[1]
    return sim_matrix

# doc2vec("E:\TRP\data\\all_text_words.txt")