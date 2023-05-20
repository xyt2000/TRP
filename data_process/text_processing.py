# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/2 11:55
# software: PyCharm

"""
文件说明：
"""
import re
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
    """
           报告的文字预处理 供参考
       for q in range(1,21):
           print(str(q) + "start")
           file_path = "../data/reports/"+str(q)+"/app"+str(q)+".csv"
           reports = pd.read_csv(file_path, encoding="utf-8")
           all_text = list(reports['text'])

           # 分词 + 去除停止词
           texts = segment_filter(all_text)
           texts = merge(texts)
           texts = synonymsy(texts)
           use_texts = []
           for text in texts:
               for word in text.split(" "):
                   if bool(re.search(r'\d', word)):
                       text = text.replace(word+" ", '')
               use_texts.append(text)
           # print(use_texts)
           path = "..\output\\" + str(num) + "\\" + "_text.txt"
           f = open(path, "w", encoding="utf-8")
           for i in range(len(use_texts)):
               f.write(use_texts[i] + "\n", )
           f.close()
           """
    # 报告图片中文字的预处理
    for num in range(1,21):
        path = "../output"
        image_text_path = path + "/" + str(num) + "/" + "text.txt" # 图中提取的文字
        #image_text_path = path + "/" + str(num) + "/" + "text.txt" # 报告提取的文字
        f = open(image_text_path,"r",encoding="utf-8")
        all_text = []
        for line in f.readlines():
            all_text.append(line.split("&")[1])
        texts = segment_filter(all_text)
        texts = merge(texts)
        texts = synonymsy(texts)
        use_texts = []
        for text in texts:
            for word in text.split(" "):
                if bool(re.search(r'\d', word)):
                    text = text.replace(word+" ", '')
            use_texts.append(text)
        # print(use_texts)
        path = "..\\output" + str(num) + "\\" + "use_text.txt"
        f = open(path, "w", encoding="utf-8")
        for i in range(len(use_texts)):
            f.write(use_texts[i] + "\n", )
        f.close()
