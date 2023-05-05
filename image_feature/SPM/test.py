# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/27 11:48
# software: PyCharm

"""
文件说明：
"""
import cv2
import numpy as np
from sklearn.cluster import KMeans

VOC_SIZE = 100
PYRAMID_LEVEL = 1

def extract_DenseSift_descriptors(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    disft_step_size = DSIFT_STEP_SIZE
    keypoints = [cv2.KeyPoint(x, y, disft_step_size)
            for y in range(0, gray.shape[0], disft_step_size)
                for x in range(0, gray.shape[1], disft_step_size)]
    keypoints, descriptors = sift.compute(gray, keypoints)
    return [keypoints, descriptors]

def build_codebook(X, voc_size):
    features = np.vstack((descriptor for descriptor in X))
    kmeans = KMeans(n_clusters=voc_size, n_jobs=-2)
    kmeans.fit(features)
    codebook = kmeans.cluster_centers_.squeeze()
    return codebook

def spm(imgs):
    train_feature = [extract_DenseSift_descriptors(img) for img in imgs]
    train_kp, train_des = zip(*train_feature)
    codebook = build_codebook(train_des, VOC_SIZE)
    imgs = [spatial_pyramid_matching(imgs[i],
                                        train_des[i],
                                        codebook,
                                        level=PYRAMID_LEVEL)
               for i in xrange(len(imgs))]
    matrix = np.asarray(imgs)









if __name__ == '__main__':
    cur_path = "E:\TRP\data"
    for num in range(1, 21):
        try:
            import cPickle
            pkl = "./"+str(num)+".pkl"
            print(num)
            file_path = "\\reports\\"+ str(num) + "\\" + "image_path.txt"
            path = cur_path + file_path
            f = open(path,"r")
            Paths = []
            for line in f.readlines():
                Paths.append(line.replace("\n",""))
            length = len(Paths)
            x_train = []
            for path in Paths:
                img = cv2.imread(path)
                img = cv2.resize(img, (32, 32))
                x_train.append(img)
            VOC_SIZE = 100
            PYRAMID_LEVEL = 1
            DSIFT_STEP_SIZE = 4
            x_train_feature = [extract_DenseSift_descriptors(img) for img in x_train]
            x_train_kp, x_train_des = zip(*x_train_feature)
            codebook = build_codebook(x_train_des, VOC_SIZE)
            x_train = [spatial_pyramid_matching(x_train[i],
                                                x_train_des[i],
                                                codebook,
                                                level=PYRAMID_LEVEL)
                       for i in xrange(len(x_train))]
            x_train = np.asarray(x_train)
            path = "E:\TRP\output\\" + str(num)+ "\\" + "spm_32.txt"
            f = open(path, "w")
            for i in range(length):
                f.write(str(x_train[i].tolist())+"\n")
            f.close()
        except:
            print(str(num)+"error")