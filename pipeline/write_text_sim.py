# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/8 22:14
# software: PyCharm

"""
文件说明：
"""

from text_feature.feature_edit_Levenshtein import edit
from text_feature.feature_one_hot_word import one_hot_word
from text_feature.feature_one_hot_sequence import one_hot_sequence
from text_feature.feature_tfidf import tfidf
from text_feature.feature_tfidf_update import tf_idf_update
from text_feature.feature_topic_lsi import lsi
from text_feature.feature_topic_lda import lda_pro,lda_pro_01,lda_pro_paper
from text_feature.feature_bm25 import gensim_bm25
from text_feature.feature_bert import bert
from text_feature.feature_word2vec import my_word2vec,other_word2vec
from text_feature.feature_doc2vec import doc2vec
from prioritization.art import art_sim_matrix,art_distance_matrix
from prioritization.additional import additional
from evaluate.apfd import get_apfd
from text_feature.feature_edit_manhattan import get_manhattan, edit_manhattan
"""
algorithms = ["edit",
              "one_hot_word","one_hot_sequence",
              "tfidf", "tifidf_update", "bm25",
              "lsi","lda_pro","lda_pro_01","lda_pro_spectrum",
              "bert","word2vec","doc2vec"
             ]
"""
algorithms = ["word2vec"]
word_types = ["text_words"]
for num in range(1,21):
    #print(num)
    for type in word_types:
        # print(type)
        apfd_sum = []
        for i in range(1):
            apfds = []
            for algorithm in algorithms:
                app_path = "../data/reports/"+str(num)+"/"+"app"+str(num)+".csv"
                word_path = "../data/reports/"+str(num)+"/"+str(num)+"_"+type+".txt"
                f = open(word_path,"r")
                lines = len(f.readlines())
                distance_matrix = []
                sim_matrix = []
                one_hot_matrix = []
                try:
                    if algorithm == "edit":
                        distance_matrix = edit(word_path)
                    elif algorithm == "manhattan":
                        distance_matrix = edit_manhattan(word_path)
                    elif algorithm == "one_hot_word":
                        one_hot_matrix = one_hot_word(word_path)
                    elif algorithm == "one_hot_sequence":
                        one_hot_matrix = one_hot_sequence(word_path)
                    elif algorithm == "tfidf":
                        sim_matrix = tfidf(word_path)
                    elif algorithm == "tifidf_update":
                        sim_matrix = tf_idf_update(word_path)
                    elif algorithm == "bm25":
                        sim_matrix = gensim_bm25(word_path)
                    elif algorithm == "lsi":
                        sim_matrix = lsi(word_path)
                    elif algorithm == "lda_pro":
                        sim_matrix = lda_pro(word_path,lines//5+1)
                    elif algorithm == "lda_pro_01":
                        one_hot_matrix = lda_pro_01(word_path,lines//5+1)
                    elif algorithm == "lda_pro_spectrum":
                        sim_matrix = lda_pro_paper(word_path,lines//5+1)
                    elif algorithm == "bert":
                        sim_matrix = bert(word_path)
                    elif algorithm == "word2vec":
                        sim_matrix = my_word2vec(word_path,"data.model")
                    else:
                        sim_matrix = doc2vec(word_path)
                    path = "E:\TRP\output" + "\\" + str(num)+"\\" + algorithm+".txt"
                    if len(distance_matrix) != 0:
                        f = open(path,"w")
                        for line in distance_matrix:
                            f.write(str(line)+"\n")
                        f.close()
                    if len(sim_matrix) != 0:
                        f = open(path, "w")
                        for line in sim_matrix:
                            f.write(str(line) + "\n")
                        f.close()
                    if len(one_hot_matrix) != 0:
                        f = open(path, "w")
                        for line in one_hot_matrix:
                            f.write(str(line) + "\n")
                        f.close()
                except:
                    print(num + algorithm)