# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/5/4 14:44
# software: PyCharm

"""
文件说明：
"""
import numpy as np
from matplotlib import pyplot as plt, ticker
from scipy.interpolate import make_interp_spline

from evaluate.apfd import get_apfd, get_apfd_items, get_apfd_items1
from fusion.late.late_fusion import average, dicts
from prioritization.art import art_sim_matrix_new, art_sim_matrix
from text_feature.distance import get_distance_cos


if __name__ == "__main__":
    test1 = ["ocr_tfidf", "tfidf"]
    test2 = ["bert", "word2vec"]
    test3 = ["bert", "word2vec", "ocr_tfidf", "tfidf"]
    test4 = ["gist_res", "CEDD_RES"]
    test5 = ["gist_res", "CEDD_RES","spm_RES"]
    test6 = ["gist_res", "CEDD_RES", "Color_RES", "spm_RES"]
    test7 = ["bert", "word2vec", "gist_res", "CEDD_RES", "spm_RES"]
    test8 = ["bert", "word2vec", "ocr_tfidf", "tfidf", "gist_res", "spm_RES"]
    test9 = ["bert", "word2vec", "ocr_tfidf", "tfidf", "gist_res", "CEDD_RES", "spm_RES"]
    test10 = ["bert", "word2vec", "ocr_tfidf", "tfidf", "gist_res", "Color_RES", "spm_RES"]
    #all_list = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10]
    test11 = ["bert", "word2vec", "gist_res", "tfidf", "CEDD_RES", "ocr_tfidf", "spm_RES"]
    test12 = ["gist_res", "CEDD_RES", "ocr_tfidf", "spm_RES"]
    test13 = ["bert", "word2vec", "ocr_tfidf", "tfidf", "gist_res", "CEDD_RES", "spm_RES"]
    test14 = ["bert", "word2vec", "ocr_tfidf", "tfidf", "gist_res", "CEDD_RES", "spm_RES"]
    all_list = [test11]
    matrix = []
    for uses in all_list:
        print(uses)
        for num in range(1,21):
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            sequence = average(test13,1)#平均排序
            sequence = dicts(test13,1)#字典序排序挑选即可
            apfd = get_apfd(app_path, sequence)
            print(apfd)