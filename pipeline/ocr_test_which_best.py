# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/8 17:17
# software: PyCharm

from text_feature.feature_edit_Levenshtein import edit
from text_feature.feature_one_hot_word import one_hot_word
from text_feature.feature_one_hot_sequence import one_hot_sequence
from text_feature.feature_tfidf import tfidf
from text_feature.feature_tfidf_update import tf_idf_update, tf_idf_update_image, tf_idf
from text_feature.feature_topic_lsi import lsi
from text_feature.feature_topic_lda import lda_pro,lda_pro_01,lda_pro_paper
from text_feature.feature_bm25 import gensim_bm25
from text_feature.feature_bert import bert
from text_feature.feature_word2vec import my_word2vec,other_word2vec
from text_feature.feature_doc2vec import doc2vec
from prioritization.art import art_sim_matrix, art_distance_matrix, art_distance_matrix_new, art_sim_matrix_new
from prioritization.additional import additional
from evaluate.apfd import get_apfd
from text_feature.feature_edit_manhattan import get_manhattan, edit_manhattan
"""
文件说明：
algorithms = ["edit",
              "one_hot_word","one_hot_sequence",
              "tfidf", "tifidf_update", "bm25",
              "lsi","lda_pro","lda_pro_01","lda_pro_spectrum",
              "bert","word2vec","doc2vec"
             ]
"""
algorithms = ["edit","manhattan",
              "one_hot_word","one_hot_sequence",
              "tfidf", "tifidf_update", "bm25",
              "lsi","lda_pro","lda_pro_01","lda_pro_spectrum",
              "bert","word2vec","doc2vec"
             ]
for num in range(1,21):
    print(num)
    apfd_sum = []
    for i in range(1):
        apfds = []
        for algorithm in algorithms:
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            word_path = "../output//" + str(num) + "/" +"use_text" + ".txt"
            f = open(word_path, "r")
            lines = len(f.readlines())
            sim_matrix = []
            one_hot_matrix = []
            sequence = []
            distance_matrix = []
            if algorithm == "ocr_tfidf":
                sim_matrix = tfidf(word_path)
                path = "E:\TRP\output" + "\\" + str(num) + "\\" + algorithm + ".txt"
                if len(sim_matrix) != 0:
                    f = open(path, "w")
                    for line in sim_matrix:
                        f.write(str(line) + "\n")
                    f.close()
            elif algorithm == "edit":
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
                sim_matrix = lda_pro(word_path, lines // 5+1)
            elif algorithm == "lda_pro_01":
                one_hot_matrix = lda_pro_01(word_path, lines // 5+1)
            elif algorithm == "lda_pro_spectrum":
                sim_matrix = lda_pro_paper(word_path, lines // 5+1)
            elif algorithm == "bert":
                sim_matrix = bert(word_path)
            elif algorithm == "word2vec":
                sim_matrix = my_word2vec(word_path,"ocr.model")
            else:
                sim_matrix = doc2vec(word_path)

            if len(distance_matrix) != 0:
                sequence = art_distance_matrix_new(distance_matrix)
            if len(sim_matrix) != 0:
                sequence = art_sim_matrix_new(sim_matrix)
            if len(one_hot_matrix) != 0:
                sequence = additional(one_hot_matrix)

            # print(algorithm)
            # print(sequence)
            # print("apfd:")

            apfd = get_apfd(app_path, sequence)
            # print(apfd)
            apfds.append(apfd)
            """
        """
        apfd_sum.append(apfds)
        apfd_avg = []
        for j in range(len(apfd_sum[0])):
            apfd = 0
            for i in range(len(apfd_sum)):
                apfd += apfd_sum[i][j]
            apfd_avg.append(apfd / len(apfd_sum))
        print(apfd_avg)
