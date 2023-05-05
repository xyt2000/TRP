"""
文件说明：
    核心算法：prioritization
    输入：测试用例dict(key：测试用例id,value：测试用例，以字符串形式表示) 选择编码方式：CodeBERT or unixCoder
    输出：排序后的测试用例 list(item为测试用例id)
ex:
    input:{1:"def add(a, b):\n    return a + b",
           2:"def sub(a, b):\n    return a - b",
           3:"def mul(a, b):\n    return a * b",
           4:"def div(a, b):\n    return a / b"}
    output:[1,2,3,4]
req:
    pytorch: 1.10.2
    transformers: 4.28.1
    numpy: 1.23.5
"""
import sys
from collections import defaultdict
import torch
from transformers import AutoTokenizer, AutoModel
import random
import numpy as np


def CodeBERT(code):
    """
    获取代码的CodeBERT嵌入
    """
    # 需要本地加载的话可以直接到https://huggingface.co/下载 unixCoder同
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    tokens = tokenizer.tokenize(code)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = torch.tensor([input_ids])
    outputs = model(input_ids)
    code_embedding = outputs.last_hidden_state.mean(dim=1)
    return code_embedding.data.numpy()[0]


def unixCoder(code):
    """
    获取代码的unixCoder嵌入
    """
    tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base")
    model = AutoModel.from_pretrained("microsoft/unixcoder-base")
    tokens = tokenizer.tokenize(code)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = torch.tensor([input_ids])
    outputs = model(input_ids)
    code_embedding = outputs.last_hidden_state.mean(dim=1)
    return code_embedding.data.numpy()[0]


def ART(distance_matrix):
    """
    ART排序算法
    """
    num = len(distance_matrix)
    select = []
    suite = [i for i in range(num)]
    first = random.randint(0, len(distance_matrix) - 1)
    select.append(first)
    suite.remove(first)
    while len(suite) != 0:
        candidate = defaultdict(int)
        for r1 in suite:
            temp = sys.maxsize
            for r2 in select:
                if distance_matrix[r1][r2] < temp:
                    temp = distance_matrix[r1][r2]
                    candidate[r1] = temp
        sort = sorted(candidate.items(), key=lambda x: x[1], reverse=True)
        select_case = int(sort[0][0])
        select.append(select_case)
        suite.remove(select_case)
    return select


def eucliDist(vec1, vec2):
    return np.sqrt(np.sum(np.square(vec1 - vec2)))


def prioritization(testcases, mode):
    num = len(testcases)
    distance_matrix = [[0 for _ in range(num)] for _ in range(num)]
    vec_matrix = []
    if mode == "CodeBERT":
        for key, value in testcases.items():
            vec = CodeBERT(value)
            vec_matrix.append(vec)
    else:
        for key, value in testcases.items():
            vec = unixCoder(value)
            vec_matrix.append(vec)
    vec_matrix = np.array(vec_matrix)
    for i in range(num):
        distance_matrix[i][i] = 0
        for j in range(i + 1, num):
            distance_matrix[i][j] = eucliDist(vec_matrix[i], vec_matrix[j])
            distance_matrix[j][i] = distance_matrix[i][j]
    select = ART(distance_matrix)
    keys = []
    for key in testcases.keys():
        keys.append(key)
    res = []
    for vec in select:
        res.append(keys[vec])
    return res


print(prioritization({1: "def add(a, b):\n    return a + b",
                      2: "def sub(a, b):\n    return a - b",
                      3: "def mul(a, b):\n    return a * b",
                      4: "def div(a, b):\n    return a / b"},
                     "unixCoder",
                     ))
