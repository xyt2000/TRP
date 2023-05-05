# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/26 12:44
# software: PyCharm

"""
文件说明：
"""
import torch
import os
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import numpy as np
# device = torch.device("cuda:o" if torch.cuda.is_available() else "cpu")
def write_path(path1, path2, num, matrix):
    """
    :param path1: 1
    :param path2: 2
    :param num: app
    :param matrix: data
    :return:
    """
    path = "E:/TRP/early_data//"+path1+"//" + str(num) + "/" + path2 + ".txt"
    f = open(path, "w")
    for line in matrix:
        f.write(str(line) + "\n")
    f.close()

def read_path(path1, path2, num):
    """
    :param path1: 1
    :param path2: 2
    :param num: app
    :param matrix: data
    :return:
    """
    path = "E:\TRP\early_data\\"+path1+"\\" + str(num) + "\\" + path2 + ".txt"
    f1 = open(path, "r")
    reses = []
    for line1 in f1.readlines():
        line1 = line1[1:-2].replace("\n", "")
        reses.append(line1.split(", "))
    matrix = []
    for res in reses:
        matrix.append(list(map(float, res)).copy())
    return matrix
torch.cuda.set_device('cuda:0')
EPOCH = 1000
BATCH_SIZE = 50
#设为多少，最后维度就是多少
LR = 0.0005
# def add(m, n):
"""
result = [0] * 50
#特征融合：encoder相加然后一起decoder
out_path = '/home/renyanhua/hua_project/DAIC/database/AVEC2019/fusion_features/speech/deep1'
data1_path = '/home/renyanhua/hua_project/DAIC/database/AVEC2019/Avec_features/speech/DS_VGG' #特征地址
data2_path = '/home/renyanhua/hua_project/DAIC/database/AVEC2019/Avec_features/speech/DS_densenet'
files1 = os.listdir(data1_path)
files2=os.listdir(data2_path)

files1.sort()
files2.sort()
l =[]
for file1,file2 in zip(files1,files2):
#数据加载
    file_1 = np.load(os.path.join(data1_path, file1))
    file_2 = np.load(os.path.join(data2_path, file2))

train_loader1 = Data.DataLoader(dataset=file_1, batch_size=BATCH_SIZE, drop_last=True, shuffle=True)
train_loader2 = Data.DataLoader(dataset=file_2, batch_size=BATCH_SIZE, drop_last=True, shuffle=True)
"""
class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder1 = nn.Sequential(
            nn.Linear(100, 64),
            nn.Tanh(),
        )
        self.encoder2 = nn.Sequential(
            nn.Linear(4500, 1024),
            nn.Tanh(),
            nn.Linear(1024, 512),
            nn.Tanh(),
            nn.Linear(512, 64),
            nn.Tanh(),
        )
        self.decoder1 = nn.Sequential(
        nn.Linear(128,100),
        nn.Tanh(),
        nn.Sigmoid()
        )
        self.decoder2 = nn.Sequential(
        nn.Linear(128,512),
        nn.Tanh(),
        nn.Linear(512, 1024),
        nn. Tanh(),
        nn.Linear(1024, 4500),
        nn.Tanh(),
        nn.Sigmoid()
        )
    def forward(self, x1, x2):
            encoded1 = self.encoder1(x1)
            encoded2 = self.encoder2(x2)
            encoded = torch.cat((encoded1, encoded2),dim=1)
            decoded1 = self.decoder1(encoded)
            decoded2 = self.decoder2(encoded)
            return encoded, decoded1, decoded2

test10 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD",  "spm"]
    # all_list = [test1,test2,test3,test4,test5,test6,test7,test8,test9,test10]
all_list = test10
x1,x2,x3,x4,x5,x6,x7= None,None,None,None,None,None,None
y1,y2,y3,y4,y5,y6,y7= None,None,None,None,None,None,None
def getAutoencoderFusion(Params):
    encoded = 0
    autoencoder = AutoEncoder()
    optimizer = torch.optim.Adam(autoencoder.parameters(), lr=LR)
    loss_func = nn.MSELoss()
    for num in range(1, 21):
        x1 = torch.Tensor(np.array(read_path("min-max", "bert_vector", num)))
        x2 = torch.Tensor(np.array(read_path("min-max", "spm", num)))
        y1,y2= x1,x2
        for epoch in range(1000):
            encoded, decoded1, decoded2 = autoencoder(x2,x2)
            loss = loss_func(decoded1, y2) + loss_func(decoded2, y2)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        matrix = encoded.tolist()
        write_path("fillzeroAE", "ae_7_word+spm", num, matrix)