# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/30 20:24
# software: PyCharm

"""
文件说明：
自动编码器测试
"""
import math

import numpy as np

from pipeline.fileUtils import read_path, write_path

np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Model  # 泛型模型
from keras.layers import Dense, Input
import matplotlib.pyplot as plt
"""
# X shape (60,000 28x28), y shape (10,000, )
(x_train, _), (x_test, y_test) = mnist.load_data()

# 数据预处理
x_train = x_train.astype('float32') / 255. - 0.5  # minmax_normalized
x_test = x_test.astype('float32') / 255. - 0.5  # minmax_normalized
x_train = x_train.reshape((x_train.shape[0], -1))
x_test = x_test.reshape((x_test.shape[0], -1))
print(x_train.shape)
print(x_test.shape)
"""
def autoencoder(x_train,k):
    dimension = x_train.shape[1]

    encoding_dim = k
    input = None
    decoded = None
    # this is our input placeholder
    # 100以内
    encoder_output = None
    if dimension <= 100:
        input = Input(shape=(x_train.shape[1],))
        #encoded = Dense(10, activation='relu')(input)
        encoder_output = Dense(encoding_dim, activation='relu')(input)
        decoded = Dense(x_train.shape[1], activation='tanh')(encoder_output)
    elif 100 < dimension < 1000:
        input = Input(shape=(x_train.shape[1],))
        encoded = Dense(100, activation='relu')(input)
        encoder_output = Dense(encoding_dim, activation='relu')(encoded)
        decoded = Dense(100, activation='relu')(encoder_output)
        decoded = Dense(x_train.shape[1], activation='relu')(decoded)
    else:
        input = Input(shape=(x_train.shape[1],))
        encoded = Dense(1000, activation='relu')(input)
        encoded = Dense(100, activation='relu')(encoded)
        encoder_output = Dense(encoding_dim, activation='relu')(encoded)
        decoded = Dense(100, activation='relu')(encoder_output)
        decoded = Dense(1000, activation='relu')(decoded)
        decoded = Dense(x_train.shape[1], activation='relu')(decoded)
    """
     # 编码层
    #encoded = Dense(128, activation='relu')(input_img)
    #encoded = Dense(64, activation='relu')(encoded)
    encoded = Dense(10, activation='relu')(input)
    encoder_output = Dense(encoding_dim)(encoded)
    # 解码层
    decoded = Dense(10, activation='relu')(encoder_output)
    #decoded = Dense(64, activation='relu')(decoded)
    #decoded = Dense(128, activation='relu')(decoded)
    decoded = Dense(16, activation='tanh')(decoded)
    """

    # 构建自编码模型
    autoencoder = Model(inputs=input, outputs=decoded)
    # 构建编码模型
    encoder = Model(inputs=input, outputs=encoder_output)
    # compile autoencoder
    autoencoder.compile(optimizer='adam', loss='mse')
    # training
    autoencoder.fit(x_train, x_train, epochs=3000, batch_size=512, shuffle=True)
    # plotting
    encoded = encoder.predict(x_train)
    return encoded


    """
plt.scatter(encoded_imgs[:, 0], encoded_imgs[:, 1], c=y_test, s=3)
plt.colorbar()
plt.show()
    """
import numpy as np

def pca(X, k):
    X = X - np.mean(X, axis=0)
    X_cov = np.cov(X, rowvar=False)
    eigvalues, eigvectors = np.linalg.eig(X_cov)
    max_eigvalue_index = np.argsort(-eigvalues)[:k]
    W = eigvectors[:, max_eigvalue_index]
    Z = X @ W
    return Z

"""
[768, 100, 1423, 1145, 256, 144, 97, 4500]97*8 = 776 
[768, 100, 290, 483, 256, 144, 97, 4500]97 776
[768, 100, 209, 167, 256, 144, 97, 4500]97 776
[768, 100, 100, 59, 256, 144, 97, 4500]59 472 400
[768, 100, 302, 68, 256, 144, 97, 4500]68 544
[768, 100, 211, 153, 256, 144, 97, 4500]97 776
[768, 100, 478, 514, 256, 144, 97, 4500]97 776
[768, 100, 580, 134, 256, 144, 97, 4500]97 776
[768, 100, 732, 454, 256, 144, 97, 4500]97 776
[768, 100, 303, 159, 256, 144, 97, 4500]97 776
[768, 100, 46, 44, 256, 144, 97, 4500] 368 300
[768, 100, 41, 70, 256, 144, 97, 4500] 328 300
[768, 100, 167, 152, 256, 144, 97, 4500] 776
[768, 100, 916, 489, 256, 144, 97, 4500] 776
[768, 100, 854, 477, 256, 144, 97, 4500] 776
[768, 100, 467, 304, 256, 144, 97, 4500] 776
[768, 100, 45, 32, 256, 144, 97, 4500]236 30
[768, 100, 753, 903, 256, 144, 97, 4500] 776  30
[768, 100, 263, 89, 256, 144, 97, 4500] 712   30
[768, 100, 259, 197, 256, 144, 97, 4500] 776  30
768 300 30
100 30
x 100 30


"""


if __name__ == '__main__':
    test10 = ["bert_vector", "word2vec_vector", "ocr_tfidf_vector", "tfidf_vector", "gist", "CEDD", "color", "spm"]
    # all_list = [test1,test2,test3,test4,test5,test6,test7,test8,test9,test10]
    all_list = test10
    for num in range(1, 21):
        shapes = [100, 100, 100, 59, 68,
                  100, 100, 100, 100, 100,
                  44, 41, 100, 100, 100,
                  100, 32, 100, 89, 100]
        for feature in all_list:
            matrix = read_path("output", feature, num)
            matrix = np.array(matrix)
            #low_features = autoencoder(test_matrix, )
            if matrix.shape[1] != shapes[num-1]:
                matrix = pca(matrix, shapes[num-1])
                matrix = np.real(matrix)
                matrix = matrix.tolist()
                write_path("pca", feature, num, matrix)
                print(feature)
            else:
                matrix = matrix.tolist()
                write_path("pca", feature, num, matrix)
                print(feature)





