# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/27 0:07
# software: PyCharm

"""
文件说明：
"""
from typing import re

import jieba


class TextProcessingService:
    def __init__(self):
        self.stopWordsPath = "../data/stop_words.txt"
        self.synonymsyList = "../data/cilin.txt"
    @staticmethod
    def splitWords(list):
        x_raw_list = []
        sentences_list = []
        for sample in list:
            sentences = re.split(' |。', sample)
            sentences = [item for item in filter(lambda x: x != '', sentences)]
            sentences_list.append(sentences)
            x_raw = []
            for sentence in sentences:
                tmp = jieba.cut(sentence)  # 使用jieba分词
                x_raw.append(tmp.strip())
            x_raw_list.append(x_raw)
        return x_raw_list
    @staticmethod
    def removeStopWords(self,list):
        stopwords = [line.strip() for line in open(self.stopWordsPath, 'r', encoding='utf-8').readlines()]
        x_raw_list = []
        for sample in list:
            outstr_list = list()
            for word in sample:
                if word not in stopwords:
                    outstr_list.append(word)
            x_raw_list.append(' '.join(outstr_list))
        return x_raw_list
    @staticmethod
    def synonymsyReplace(self,x_raw_list):
        res_list = []
        combine_dict = {}
        for line in open(self.synonymsyList, "r", encoding='utf-8'):
            seperate_word = line[9:].strip().split(" ")
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[seperate_word[i]] = seperate_word[0]
        for str in x_raw_list:
            if len(str) != 0:
                final_sentence = []
                for word in str.split(' '):
                    if word in combine_dict:
                        final_sentence.append(combine_dict[word])
                    else:
                        final_sentence.append(word)
                res_list.append(' '.join(final_sentence))
            else:
                res_list.append(' ')
        return res_list



    def load_stopword_list(filepath):
        """
        create stop word list
        filepath : stop word file path

        """
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def word_segment2token(sample):
        result = jieba.cut(sample, cut_all=False)
        outstr_list = list()
        curpath = os.path.dirname(os.path.realpath(__file__))
        stopwords = load_stopword_list(os.path.join(curpath, 'stop_words.txt'))
        for word in result:
            if word not in stopwords:
                outstr_list.append(word)
        str_out = ' '.join(outstr_list)
        return str_out

    def segment_filter(samples):
        x_raw_list = []
        sentences_list = []
        for sample in samples:
            try:
                sentences = re.split(' |。', sample)
                sentences = [item for item in filter(lambda x: x != '', sentences)]
                sentences_list.append(sentences)
                x_raw = []
                for sentence in sentences:
                    tmp = word_segment2token(sentence)  # 使用jieba分词
                    x_raw.append(tmp.strip())
                x_raw_list.append(x_raw)
            except:
                print(sample)
        return x_raw_list

    def synonymsy(x_raw_list):
        res_list = []
        combine_dict = {}
        for line in open("cilin.txt", "r", encoding='utf-8'):
            seperate_word = line[9:].strip().split(" ")
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[seperate_word[i]] = seperate_word[0]
        for str in x_raw_list:
            if len(str) != 0:
                final_sentence = []
                for word in str.split(' '):
                    if word in combine_dict:
                        word = combine_dict[word]
                        final_sentence.append(word)
                    else:
                        final_sentence.append(word)
                res = ' '.join(final_sentence)
                res_list.append(res)
            else:
                res_list.append(' ')
        return res_list
