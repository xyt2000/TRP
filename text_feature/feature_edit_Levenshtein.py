# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/7 15:22
# software: PyCharm

"""
文件说明：
"""
def Levenshtein_Distance(str1, str2):
    """
    计算字符串 str1 和 str2 的编辑距离
    :param str1
    :param str2
    :return:
    """
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if (str1[i - 1] == str2[j - 1]):
                d = 0
            else:
                d = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    return matrix[len(str1)][len(str2)]

def edit(path):
    texts = []
    f = open(path, "r")
    raw_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            texts.append("")
        else:
            texts.append(str(line).replace(" ", ""))
    #print(texts)
    sim_matrix = [[0 for _ in range(len(texts))] for _ in range(len(texts))]
    for i in range(len(texts)):
        for j in range(len(texts)):
            sim_matrix[i][j] = round(Levenshtein_Distance(texts[i], texts[j]), 6)
    return sim_matrix



