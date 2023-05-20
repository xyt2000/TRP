import os

import numpy as np
import pandas as pd
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image

# 获取vgg19原始模型, 输出图像维度是1000. 可以通过提供本地参数文件的路径, 并使用load_state_dict加载
vgg_model_1000 = models.vgg19(pretrained=True)

# 下面三行代码功能是:得到修改后的vgg19模型.
# 具体实现是: 去掉vgg19原始模型的第三部分classifier的最后一个全连接层,
# 用新的分类器替换原始vgg19的分类器，使输出维度是4096.
vgg_model_4096 = models.vgg19(pretrained=True)
new_classifier = torch.nn.Sequential(*list(vgg_model_4096.children())[-1][:6])
vgg_model_4096.classifier = new_classifier

# 获取和处理图像


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist

cur_path = "..\\data"
if __name__ == "__main__":
    for num in range(1, 21):
        print(num)
        file_path = "\\reports\\"+ str(num) + "\\" + "app" + str(num)+".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        # download screenshots of all reports and return the local image path
        length = len(number)
        matrix = [[0 for i in range(length)]for j in range(length)]
        vgg_matrix = []
        for i in range(length):
            index1 = number[i]
            tmp1 = images[i].split('.')
            path1 = os.path.join(cur_path, "reports", str(num), "images", str(index1) + '.' + tmp1[len(tmp1) - 1])
            try:
                image_dir = path1
                im = Image.open(image_dir).convert("RGB")
                trans = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                im = trans(im)
                im.unsqueeze_(dim=0)

                # 使用vgg19得到图像特征.
                # 原始vgg19模型
                image_feature_1000 = vgg_model_4096(im).data[0]
                print('dim of vgg_model_1000: ', image_feature_1000.shape)
                vgg_matrix.append(np.array(image_feature_1000.tolist()))
            except:
                vgg_matrix.append(np.zeros(4096))
        path = "..\\output\\" + str(num) + "\\" + "vgg19.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(vgg_matrix[i].tolist()) + "\n")
        f.close()
        for i in range(length):
            matrix[i][i] = 1
            for j in range(i+1,length):
                try:
                    matrix[i][j] = get_distance_cos(vgg_matrix[i], vgg_matrix[j])
                    matrix[j][i] = matrix[i][j]
                except:
                    matrix[i][j] = -1
                    print(str(i)+"," + str(j))
            print(matrix[i])

        path = "..\\output\\" + str(num)+ "\\" + "vgg19_res.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(matrix[i])+"\n")
        f.close()