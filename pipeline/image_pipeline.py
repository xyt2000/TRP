# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/3 19:40
# software: PyCharm

"""
文件说明：
"""
from evaluate.apfd import get_apfd
from prioritization.additional import additional
from prioritization.art import art_distance_matrix, art_sim_matrix, art_distance_matrix_new, art_sim_matrix_new
from text_feature.feature_tfidf_update import tf_idf_update, tf_idf_update_image


def read_matrix(path1):
    f1 = open(path1, "r")
    matrix = []
    for line1 in f1.readlines():
        line1 = line1.replace("\n", "")
        line1 = line1[1:-1]
        matrix.append(line1.split(", "))
    res = []
    for line in matrix:
        res.append(list(map(float, line)).copy())
    return res
#solutions = ["gist", "cedd", "color", "sift", "surf", "orb", "ssim", "ocr","vgg19","spm"]
solutions = ["vgg19"]
for num in range(1,21):
    #print(num)
    apfd_sum = []
    for i in range(1):
        apfds = []
        for solution in solutions:
            app_path = "../data/reports/" + str(num) + "/" + "app" + str(num) + ".csv"
            data_path = "../output/"+ str(num) + "/"
            distance_matrix = []
            sim_matrix = []
            one_hot_matrix = []
            sequence = []
            if solution == "gist":
                data_path += "gist_res.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "cedd":
                data_path += "CEDD_RES.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "color":
                data_path += "Color_RES.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "sift":
                data_path += "sift.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "spm":
                data_path += "spm_RES.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "surf":
                data_path += "surf.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "orb":
                data_path += "orb.txt"
                distance_matrix = read_matrix(data_path)
            elif solution == "ssim":
                data_path += "ssim.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "spm_32":
                data_path += "CEDD_RES_new.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "mpeg7":
                data_path += "mpeg7_RES.txt"
                sim_matrix = read_matrix(data_path)
            elif solution == "vgg19":
                data_path += "vgg19_RES.txt"
                sim_matrix = read_matrix(data_path)
            else:
                data_path += "use_text.txt"
                sim_matrix = tf_idf_update(data_path)
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
            print(apfd)
            apfds.append(apfd)
        apfd_sum.append(apfds)
    apfd_avg = []
    for j in range(len(apfd_sum[0])):
        apfd = 0
        for i in range(len(apfd_sum)):
            apfd += apfd_sum[i][j]
        apfd_avg.append(apfd / len(apfd_sum))

    #print(apfd_avg)