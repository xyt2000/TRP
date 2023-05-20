# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/26 0:46
# software: PyCharm

"""
文件说明：
"""
# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/25 22:20
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
            nn.Linear(768,256),
            nn.Tanh(),
            nn.Linear(256, 128),
            nn. Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
        #Linear和Tanh配套，几对代表深度是多少
        )
        self.encoder2 = nn.Sequential(
            nn.Linear(100, 64),
            nn.Tanh(),
        )
        self.encoder3 = nn.Sequential(
            nn.Linear(1423, 512),
            nn.Tanh(),
            nn.Linear(512, 128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            # Linear和Tanh配套，几对代表深度是多少
        )
        self.encoder4 = nn.Sequential(
            nn.Linear(1145, 512),
            nn.Tanh(),
            nn.Linear(512, 128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            # Linear和Tanh配套，几对代表深度是多少
        )
        self.encoder5 = nn.Sequential(
            nn.Linear(256, 128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            # Linear和Tanh配套，几对代表深度是多少
        )
        self.encoder6 = nn.Sequential(
            nn.Linear(144, 64),
            nn.Tanh(),
            # Linear和Tanh配套，几对代表深度是多少
        )
        self.encoder7 = nn.Sequential(
            nn.Linear(4500, 1024),
            nn.Tanh(),
            nn.Linear(1024, 512),
            nn.Tanh(),
            nn.Linear(512, 64),
            nn.Tanh(),
        )
        self.decoder1 = nn.Sequential(
        nn.Linear(448,128),
        nn.Tanh(),
        nn.Linear(128, 256),
        nn. Tanh(),
        nn.Linear(256, 768),
        nn.Tanh(),
        nn.Sigmoid()
        )
        self.decoder2 = nn.Sequential(
        nn.Linear(448,100),
        nn.Tanh(),
        nn.Sigmoid()
        )
        self.decoder3 = nn.Sequential(
        nn.Linear(448,128),
        nn.Tanh(),
        nn.Linear(128, 512),
        nn. Tanh(),
        nn.Linear(512, 1423),
        nn.Tanh(),
        nn.Sigmoid()
        )
        self.decoder4 = nn.Sequential(
        nn.Linear(448,128),
        nn.Tanh(),
        nn.Linear(128, 512),
        nn. Tanh(),
        nn.Linear(512, 1145),
        nn.Tanh(),
        nn.Sigmoid()
        )
        self.decoder5 = nn.Sequential(
            nn.Linear(448, 128),
            nn.Tanh(),
            nn.Linear(128, 256),
            nn.Tanh(),
            nn.Sigmoid()
        )
        self.decoder6 = nn.Sequential(
            nn.Linear(448, 144),
            nn.Tanh(),
            nn.Sigmoid()
        )
        self.decoder7 = nn.Sequential(
        nn.Linear(448,512),
        nn.Tanh(),
        nn.Linear(512, 1024),
        nn. Tanh(),
        nn.Linear(1024, 4500),
        nn.Tanh(),
        nn.Sigmoid()
        )
    def forward(self, x1, x2, x3, x4, x5, x6, x7):
            encoded1 = self.encoder1(x1)
            encoded2 = self.encoder2(x2)
            encoded3 = self.encoder3(x3)
            encoded4 = self.encoder4(x4)
            encoded5 = self.encoder5(x5)
            encoded6 = self.encoder6(x6)
            encoded7 = self.encoder7(x7)
            encoded = torch.cat((encoded1, encoded2,encoded3, encoded4,encoded5, encoded6,encoded7),dim=1)
            decoded1 = self.decoder1(encoded)
            decoded2 = self.decoder2(encoded)
            decoded3 = self.decoder3(encoded)
            decoded4 = self.decoder4(encoded)
            decoded5 = self.decoder5(encoded)
            decoded6 = self.decoder6(encoded)
            decoded7 = self.decoder7(encoded)
            return encoded, decoded1, decoded2,decoded3, decoded4,decoded5, decoded6,decoded7
autoencoder = AutoEncoder()
optimizer = torch.optim.Adam(autoencoder.parameters(), lr=LR)
loss_func = nn.MSELoss()
test10 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD",  "spm"]
    # all_list = [test1,test2,test3,test4,test5,test6,test7,test8,test9,test10]
all_list = test10
x1,x2,x3,x4,x5,x6,x7= None,None,None,None,None,None,None
y1,y2,y3,y4,y5,y6,y7= None,None,None,None,None,None,None
for num in range(1, 21):
    x1 = torch.Tensor(np.array(read_path("min-max", "bert_vector", num)))
    x2 = torch.Tensor(np.array(read_path("min-max", "word2vec_vector", num)))
    x3 = torch.Tensor(np.array(read_path("min-max", "ocr_tfidf_vector_fill", num)))
    x4 = torch.Tensor(np.array(read_path("min-max", "tfidf_vector_fill", num)))
    x5 = torch.Tensor(np.array(read_path("min-max", "gist", num)))
    x6 = torch.Tensor(np.array(read_path("min-max", "CEDD", num)))
    x7 = torch.Tensor(np.array(read_path("min-max", "spm", num)))
    y1 = x1
    y2 = x2
    y3 = x3
    y4 = x4
    y5 = x5
    y6 = x6
    y7 = x7
    encoded = 0
    for epoch in range(2000):
        encoded, decoded1, decoded2,decoded3, decoded4,decoded5, decoded6,decoded7 = autoencoder(x1, x2, x3, x4, x5, x6, x7)
        loss = loss_func(decoded1, y1) + loss_func(decoded2, y2) + loss_func(decoded3, y3)
        loss_func(decoded4, y4) + loss_func(decoded5, y5)+loss_func(decoded6, y6) + loss_func(decoded7, y7)
        optimizer.zero_grad()
        # 固定步骤
        loss.backward()
        # 固定步骤
        optimizer.step()
        print(loss)
    matrix = encoded.tolist()
    write_path("fillzeroAE", "ae_7", num, matrix)