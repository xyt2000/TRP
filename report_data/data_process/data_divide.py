# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2022/12/6 23:08
# software: PyCharm

"""
文件说明：
"""
import os
import re

import jieba
import pandas as pd


import jieba.posseg

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

def cut(x_raw_list):
    segment_list = []
    for x_raw in x_raw_list:
        res = []
        if len(x_raw) > 0:
            for raw in x_raw:
                temp  = raw.split(" ")
                for word in temp:
                    res.append(word)
        else:
            res = res
        segment_list.append(res)
    return segment_list


def merge(text_list):
    res = []
    for text in text_list:
        sub = ""
        for sentence in text:
            sub += sentence
        res.append(sub)
    return res

if __name__ == "__main__":
    for q in range(1,21):
        print(str(q) + "start")
        file_path = "../data/reports/"+str(q)+"/app"+str(q)+".csv"
        reports = pd.read_csv(file_path, encoding="utf-8")
        all_text = list(reports['text'])
        procedures = list(reports['procedure'])
        descriptions = list(reports['description'])

        # 分词 + 去除停止词
        all_text_list = segment_filter(all_text)
        procedures_list = segment_filter(procedures)
        descriptions_list = segment_filter(descriptions)


        descriptions_list = merge(descriptions_list)
        descriptions_list = synonymsy(descriptions_list)
        # 替换近义词
        # res_list = synonymsy(x_raw_list)
        # print(res_list)

        problem_widgets = []

        problem_widgets_descriptions = []
        for procedures, descriptions in zip(procedures_list, descriptions_list):
            problem_widget = ''
            last_procedure = ''

            if len(procedures) >= 1:
                last_procedure = procedures[len(procedures) - 1]
                last_procedure_seged = jieba.posseg.cut(last_procedure.strip())
                first_v = False
                for x in last_procedure_seged:
                    if first_v:
                        if x.flag != 'x' and x.flag != 'm':# 如果在动词后面，且不是数量词或者非语素字
                            problem_widget += x.word
                    else:
                        if x.flag == 'v':# 记录当前是动词
                            first_v = True

                problem_widget = word_segment2token(problem_widget).strip()
                problem_widgets_description = problem_widget+descriptions
                problem_widgets_descriptions.append(problem_widgets_description)
            else:
                problem_widgets_descriptions.append(descriptions)

        # all_text_words = cut(all_text_list)
        procedures_words = cut(procedures_list)
        all_text_words_list = []
        for i in range(len(procedures_words)):
            sub = procedures_list[i].copy()
            sub.append(descriptions_list[i])
            all_text_words_list.append(sub)

        all_text_words_list_write = merge(all_text_words_list)
        all_procedures_list_write = merge(procedures_list)

        f = open("../data/reports/"+str(q)+"/"+str(q)+"_text_words.txt","w")
        for line in all_text_words_list_write:
            strs = line +"\n"
            f.write(strs)
        f.close()
        f = open("../data/reports/" + str(q) + "/" + str(q) + "_procedures_words.txt","w")
        for line in all_procedures_list_write:
            strs = line + "\n"
            f.write(strs)
        f.close()

        f = open("../data/reports/" + str(q) + "/" + str(q) + "_descriptions_words.txt","w")
        for line in descriptions_list:
            strs = line + "\n"
            f.write(strs)
        f.close()

        f = open("../data/reports/" + str(q) + "/" + str(q) + "_problem_widgets_descriptions.txt","w")
        for line in problem_widgets_descriptions:
            strs = line + "\n"
            f.write(strs)
        f.close()
        print(str(q) + "end")

