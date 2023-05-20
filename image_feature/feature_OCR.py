# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/5/5 17:19
# software: PyCharm

"""
文件说明：
"""
from text_feature.feature_tfidf import tfidf



for num in range(1,21):
    print(num)
    sim_matrix = []
    app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
    word_path = "../output//" + str(num) + "/" +"use_text" + ".txt"
    f = open(word_path, "r")
    lines = len(f.readlines())
    sim_matrix = tfidf(word_path)
    path = "..\\output" + "\\" + str(num) + "\\" + "ocr_tfidf" + ".txt"
    if len(sim_matrix) != 0:
        f = open(path, "w")
        for line in sim_matrix:
            f.write(str(line) + "\n")
        f.close()