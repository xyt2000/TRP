# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/4/14 11:17
# software: PyCharm

"""
文件说明：
"""
import math
from collections import defaultdict
def Lexicographic(sequences):
    prioritizations = []
    # 1、收集每个测试报告在不同排序结果的排序位置
    for i in range(len(sequences)):
        prioritization = []
        for j in range(len(sequences[0])):
            prioritization.append(sequences[i].index(j)+1)
        prioritizations.append(prioritization)
    # 2、构建表示排序位置的字符串
    length = int(math.log10(len(sequences[0])))+1
    Dicts = defaultdict(str)
    for i in range(len(sequences[0])):
        Dict = []
        for j in range(len(sequences)):
            Dict.append(prioritizations[j][i])
        list.sort(Dict)
        dict_strings = ""
        for num in Dict:
            num = str(num)
            zero = length - len(num)
            zeros = ""
            for m in range(zero):
                zeros += "0"
            dict_string = zeros + num
            dict_strings += dict_string
        Dicts[i] = dict_strings
    # 3、通过字典序排序字符串得到结果
    sort = sorted(Dicts.items(), key=lambda x: x[1])
    res = []
    for j in range(len(sort)):
        res.append(sort[j][0])
    return res