# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/7 21:43
# software: PyCharm

"""
文件说明：
"""

def get_manhattan(str1, str2):
    asc1 = []
    for i in range(len(str1)):
        asc1.append(ord(str1[i]))
    asc2 = []
    for i in range(len(str2)):
        asc2.append(ord(str2[i]))
    return sum(map(lambda i, j: abs(i - j), asc1, asc2))

def edit_manhattan(path):
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
            sim_matrix[i][j] = round(get_manhattan(texts[i], texts[j]),6)
    return sim_matrix

if __name__ == "__main__":
    edit_manhattan("E:\TRP\data\\reports\\2\\2_text_words.txt")