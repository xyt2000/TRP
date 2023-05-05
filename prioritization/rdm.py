# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/4/21 17:19
# software: PyCharm

"""
文件说明：
"""
import csv
import random


def get_apfd(report_file, sequence):
    result = [[row[0] for row in csv.reader(open(report_file, 'r', encoding='UTF-8'))],
              [row[2]for row in csv.reader(open(report_file, 'r', encoding='UTF-8'))]]
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

items = [276, 134, 29, 9, 13, 26, 152, 41, 75, 26, 5, 10, 17, 131, 88, 51, 4, 294, 12, 24]
for i in range(20):
    apfds = []
    app_path = "../data/reports/" + str(i+1) + "/" + "app" + str(i+1) + ".csv"
    for m in range(1000):
        res = [j for j in range(items[i])]
        random.shuffle(res)
        apfds.append(get_apfd(app_path,res))
    apfds.sort()
    apfds = apfds[:10]
    apfds = sum(apfds)
    print(apfds/10)