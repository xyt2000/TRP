# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/26 20:31
# software: PyCharm

"""
文件说明：
"""
import sys
from collections import defaultdict

import numpy as np


class PrioritizationAlgorithm:
    @staticmethod
    def ART(sim_matrix):
        prioritization = []
        suite = [i for i in range(len(sim_matrix))]
        max_ = defaultdict(int)
        # 第一个max_min向量
        for i in range(len(sim_matrix)):
            temp = -sys.maxsize
            for j in range(len(sim_matrix)):
                if sim_matrix[i][j] > temp and j != i:# 选择最大相似度
                    temp = sim_matrix[i][j]
                    max_[i] = temp
        sort = sorted(max_.items(), key=lambda x: x[1])# 选择最小相似度
        first = sort[0][0]
        prioritization.append(first)
        suite.remove(first)
        # 迭代选取max_min向量
        while len(suite) != 0:
            candidate = defaultdict(int)
            for r1 in suite:
                temp = -sys.maxsize
                for r2 in prioritization:
                    if sim_matrix[r1][r2] > temp: # 选择最大相似度
                        temp = sim_matrix[r1][r2]
                        candidate[r1] = temp
            sort = sorted(candidate.items(), key=lambda x: x[1]) # 选择最小相似度
            select_case = int(sort[0][0])
            prioritization.append(select_case)
            suite.remove(select_case)
        return prioritization

    @staticmethod
    def additional1(self,matrix):
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
                if self.is_full_coverage(coverage_element) == 0:
                    for test, lines in test_line_dict.items():
                        test_sort.append(test)
                    return test_sort
                # 程序元素覆盖完了 重新置为0 继续循环
                else:
                    for i in range(line_num):
                        coverage_element[i] = 0
                # 没排序的测试再次生成字典
                for j in range(test_num):
                    if self.id_in_dict(j, test_line_dict):
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

    @staticmethod
    def is_full_coverage(coverage_element):
        """
        查看是否全被覆盖
        :param coverage_element:
        :return:全被覆盖返回1 否则返回0
        """
        list = np.where(coverage_element == 0)
        if len(list) > 0:
            return 0
        else:
            return 1

    @staticmethod
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
