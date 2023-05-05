# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/26 22:42
# software: PyCharm

"""
文件说明：
"""
import numpy as np
from gensim.models import ldamodel
from gensim import corpora
from text_feature.feature_edit_Levenshtein import edit
from text_feature.feature_one_hot_word import one_hot_word
from text_feature.feature_one_hot_sequence import one_hot_sequence
from text_feature.feature_tfidf import tfidf
from text_feature.feature_tfidf_update import tf_idf_update
from text_feature.feature_topic_lsi import lsi
from text_feature.feature_topic_lda import lda_pro_paper
from text_feature.feature_bm25 import gensim_bm25
from text_feature.feature_bert import bert
from text_feature.feature_word2vec import my_word2vec,other_word2vec
from text_feature.feature_doc2vec import doc2vec
from prioritization.art import art_sim_matrix, art_distance_matrix, art_sim_matrix_new, art_distance_matrix_new
from prioritization.additional import additional
from evaluate.apfd import get_apfd
from text_feature.feature_edit_manhattan import get_manhattan, edit_manhattan
import Params
class BowAndModelService:
    @staticmethod
    def lda(texts):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        num_topic = len(texts)//5+2
        lda = ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=(num_topic))
        feature_matrix = [[0 for _ in range(num_topic)] for _ in range(len(texts))]
        for i in range(len(texts)):
            if len(texts[i]) != 0:
                point = 1 / len(texts[i])
                for word in texts[i]:
                    word_pro = lda.get_term_topics(dictionary.token2id[word], minimum_probability=0.0000001)
                    sort = sorted(word_pro, key=lambda x: x[1], reverse=True)
                    feature_matrix[i][sort[0][0]] += point
        return feature_matrix

    def extractFeature(self,Params):
        feature = ""
        if feature == "one_hot_word":
            matrix = self.one_hot_word(Params.feature['text'])
        elif feature == "one_hot_sequence":
            matrix = self.one_hot_sequence(Params.feature['text'])
        elif feature == "tfidf":
            matrix = self.tfidf(Params.feature['text'])
        elif feature == "bm25":
            matrix = self.gensim_bm25(Params.feature['text'])
        elif feature == "lsi":
            matrix = self.lsi(Params.feature['text'])
        elif feature == "lda_pro":
            matrix = self.lda(Params.feature['text'])

class EmbeddedService:
    def extractFeature(self,Params):
        feature = ""
        if feature == "bert":
            sim_matrix = bert(Params.feature['text'])
        elif feature == "word2vec":
            sim_matrix = my_word2vec(Params.feature['text'], "data.model")
        else:
            sim_matrix = doc2vec(Params.feature['text'])
