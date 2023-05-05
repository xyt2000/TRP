# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/11 15:58
# software: PyCharm

"""
文件说明：
"""
from gensim.similarities import MatrixSimilarity

def lsi(path):
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
    from gensim import corpora

    #统计所有独有的词

    dictionary = corpora.Dictionary(texts)

    #print(dictionary)
    dictionary.filter_n_most_frequent(20)
    dictionary.compactify()
    #把语料变成每个词对应的ID和出现的次数

    corpus = [dictionary.doc2bow(text) for text in texts]
    # [(0, 1), (1, 1), (2, 1)]
    from gensim import models

    #这个模型可以把语料中的稀疏的变量编程一个密集的向量，使用一个密集的向量可以表示这个句子

    lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=50)

    documents = lsi_model[corpus]

    #print(documents[0])

    num_t = 20
    index = MatrixSimilarity(documents)
    #print(lsi_model.print_topics(num_topics=num_t, num_words=20))  # 把所有的主题打印出来看看
    lsi_model.show_topics()
    sim_matrix = []
    for i in range(len(texts)):
        bow = dictionary.doc2bow(texts[i])
        query_vec = lsi_model[bow]
        sims = index[query_vec]
        sim_matrix.append(list(sims))
    return sim_matrix

