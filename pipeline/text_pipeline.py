# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/14 11:41
# software: PyCharm

"""
文件说明：
"""
import csv

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

app = [i for i in range(1, 21)]
word_types = ["text_words"]


algorithms = ["edit",
              "one_hot_word","one_hot_sequence",
              "tfidf", "bm25",
              "lsi","lda_pro_spectrum",
              "bert","word2vec","doc2vec"
             ]
"""
algorithms = ["lda_pro_spectrum"]
"""
for num in range(1,21):
    print(num)
    app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
    for type in word_types:
        # print(type)
        apfd_sum = []
        for i in range(1):
            apfds = []
            for algorithm in algorithms:
                def get_apfd(report_file, sequence):
                    result = [[row[0] for row in csv.reader(open(report_file, 'r', encoding='UTF-8'))],
                              [row[2] for row in csv.reader(open(report_file, 'r', encoding='UTF-8'))]]
                    result[0] = result[0][1:]
                    result[1] = result[1][1:]
                    apfd_item = []
                    full_category = list(set(result[1]))
                    for report in sequence:
                        real_index = result[0][report]
                        # real_index = str(report)
                        category = result[1][result[0].index(real_index)]
                        if category in full_category:
                            apfd_item.append(sequence.index(report))
                            full_category.remove(category)
                    apfd = 1 + 1 / (2 * len(result[0])) - sum(apfd_item) / (len(set(result[1])) * len(result[0]))
                    return apfd
                word_path = "../data/reports/"+str(num)+"/"+str(num)+"_"+type+".txt"
                f = open(word_path,"r")
                lines = len(f.readlines())
                distance_matrix = []
                sim_matrix = []
                one_hot_matrix = []
                sequence = []
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
                    elif algorithm == "lda_pro_spectrum":
                        sim_matrix = lda_pro_paper(word_path,lines//5+2)
                    elif algorithm == "bert":
                        # 先命令行启动服务
                        # bert-serving-start -model_dir ..\model\chinese_L-12_H-768_A-12 -num_worker=1
                        sim_matrix = bert(word_path)
                    elif algorithm == "word2vec":
                        sim_matrix = my_word2vec(word_path,"data.model")
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
                    apfd = get_apfd(app_path,sequence)
                    #print(algorithm)
                    #print(apfd)
                    apfds.append(apfd)
                except:
                    print(algorithm + "出现错误")
                    apfds.append(0)
            apfd_sum.append(apfds)
        apfd_avg = []
        for j in range(len(apfd_sum[0])):
            apfd = 0
            for i in range(len(apfd_sum)):
                apfd += apfd_sum[i][j]
            apfd_avg.append(apfd/len(apfd_sum))
        print(apfd_avg)