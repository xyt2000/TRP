# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/11 15:58
# software: PyCharm

"""
文件说明：
"""
def one_hot_sequence1(sequence_dict, raw_list):
    length = len(sequence_dict.keys())
    one_hot_list = []
    for raw in raw_list:
        dict = [0 for j in range(length)]
        if len(raw) == 0:
            one_hot_list.append(dict)
        else:
            words = raw
            for i in range(len(words)):
                if i == len(words) - 1:
                    sequence = words[i] + "-" + "end"
                else:
                    sequence = words[i] + "-" + words[i + 1]
                dict[sequence_dict[sequence]] = 1
        one_hot_list.append(dict)
    return one_hot_list

def one_hot_sequence(path):
    f = open(path, "r")
    raw_list = []
    word_list = []
    from collections import defaultdict
    sequence_dict = defaultdict(int)
    num = 0
    sequence_set = set()
    for line in f.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            raw_list.append([])
        else:
            words = line.split(" ")
            raw_list.append(words)
            for i in range(len(words)):
                if i == len(words) - 1:
                    sequence = words[i] + "-" + "end"
                else:
                    sequence = words[i] + "-" + words[i + 1]
                if sequence not in sequence_dict.keys():
                    sequence_dict[sequence] = num
                    num += 1
    import random
    nums = [i for i in range(len(sequence_dict.keys()))]
    random.shuffle(nums)
    i = 0
    for key in sequence_dict.keys():
        sequence_dict[key] = nums[i]
        i += 1

    one_hot_list = one_hot_sequence1(sequence_dict, raw_list)
    return one_hot_list

