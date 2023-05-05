# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/7 13:44
# software: PyCharm

"""
文件说明：
"""


def one_hot(word_list, raw_list):
    length = len(word_list)
    one_hot_list = []
    for raw in raw_list:
        dict = [0 for j in range(length)]
        if len(raw) == 0:
            one_hot_list.append(dict)
        else:
            for word in raw:
                index = word_list.index(word)
                dict[index] = 1
        one_hot_list.append(dict)
    return one_hot_list

def one_hot_word(path):
    f = open(path, "r")
    raw_list = []
    word_list = []
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for word in words:
                word_list.append(word)
    import random
    random.shuffle(word_list)

    one_hot_list = one_hot(word_list, raw_list)
    return one_hot_list

