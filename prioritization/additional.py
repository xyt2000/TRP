# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/7 18:57
# software: PyCharm

"""
文件说明：
"""
import time
import numpy as np


def additional1(matrix):
    """
    实现GA
    :param matrix: 覆盖矩阵
    :return:测试排序
    """
    test_num = len(matrix)
    line_num = len(matrix[0])
    test_line_dict = {}
    for i in range(test_num):
        test_line_dict[i] = []
    # 遍历矩阵，生成字典key是测试用例id value是元素的字典
    for j in range(test_num):
        temp_list = np.where(matrix[j] == 1)
        test_line_dict[j] = temp_list[0].tolist()
    test_sort = []
    coverage_element = []
    for i in range(line_num):
        coverage_element.append(0)
    coverage_element = np.array(coverage_element)
    while len(test_line_dict) != 0:
        # 获取覆盖做最多行的test
        max_len = -1
        del_index = 0
        for test, lines in test_line_dict.items():
            if len(lines) > max_len:
                del_index = test
                max_len = len(lines)
        if max_len == 0:
            # 程序元素没被覆盖完 但是已有测试覆盖不到新的元素了 所以剩余所有测试都加上
            if is_full_coverage(coverage_element) == 0:
                for test, lines in test_line_dict.items():
                    test_sort.append(test)
                return test_sort
            # 程序元素覆盖完了 重新置为0 继续循环
            else:
                for i in range(line_num):
                    coverage_element[i] = 0
            # 没排序的测试再次生成字典
            for j in range(test_num):
                if id_in_dict(j, test_line_dict):
                    temp_list = np.where(matrix[j] == 1)
                    test_line_dict[j] = temp_list[0].tolist()
            for test, lines in test_line_dict.items():
                if len(lines) > max_len:
                    del_index = test
                    max_len = len(lines)

        test_lines = test_line_dict[del_index]
        for i in test_lines:
            coverage_element[i] = 1
        test_sort.append(del_index)
        test_line_dict.pop(del_index)
        for test, lines in test_line_dict.items():
            # 将其test的value与test字典里的其他value做差
            test_line_dict[test] = set(lines).difference(set(test_lines))
    return test_sort


def is_full_coverage(coverage_element):
    """
    查看是否全被覆盖
    :param coverage_element:
    :return:全被覆盖返回1 否则返回0
    """
    list = np.where(coverage_element==0)
    if len(list) > 0:
        return 0
    else:
        return 1


def id_in_dict(num, dict):
    """
    查看测试用例num 是否在剩余的dict内
    :param num:
    :param dict:
    :return:
    """
    for test, lines in dict.items():
        if num == int(test):
            return 1
    return 0

def additional(matrix):
    dataset = np.array(matrix)
    addtional = additional1(dataset)
    return addtional

if __name__ == '__main__':
    txt_path = '../data/matrix/commons-io.txt'  # txt文本路径
    data_lists = open(txt_path).readlines()  # 读出的是str类型
    dataset = []
    # 对每一行作循环
    for line in data_lists:
        line = line.strip('\n')  # 去掉开头和结尾的换行符
        sub = []
        for i in line:
            sub.append(int(i))
        dataset.append(sub)  # 把这一行的结果作为元素加入列表dataset
    print('程序元素数量：' + str(len(dataset[0])))
    print('测试用例数量：' + str(len(dataset)))
    t1 =  time.perf_counter()
    dataset = np.array(dataset)
    t2 = time.perf_counter()
    print('np时间' + str(t2 - t1))
    start = time.perf_counter()
    addtional = additional1(dataset)
    end = time.perf_counter()
    print('排序时间' + str(end - start))
    print(addtional)