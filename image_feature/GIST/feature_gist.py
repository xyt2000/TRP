import cv2
import sys
import numpy as np
import pandas as pd

sys.path.append("./GIST/")

from utils_gist import *

def get_distance_cos(vec1, vec2):
    dist = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return dist

cur_path = "..\\..\\data"
if __name__ == "__main__":
    for num in range(20, 21):
        print(num)
        file_path = "\\reports\\"+ str(num) + "\\" + "app" + str(num)+".csv"
        path = cur_path + file_path
        reports = pd.read_csv(path)
        number = list(reports['index'])
        images = list(reports['image'])
        # download screenshots of all reports and return the local image path
        length = len(number)
        matrix = [[0 for i in range(length)]for j in range(length)]
        gist_matrix = []
        gist_helper = GistUtils()
        for i in range(length):
            index1 = number[i]
            tmp1 = images[i].split('.')
            path1 = os.path.join(cur_path, "reports", str(num), "images", str(index1) + '.' + tmp1[len(tmp1) - 1])
            try:
                np_img = cv2.imread(path1, -1)
                np_gist = gist_helper.get_gist_vec(np_img, mode="gray")
                gist_matrix.append(np_gist[0])
            except:
                gist_matrix.append(np.zeros(256))
        path = "..\\..\\output\\" + str(num) + "\\" + "gist.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(gist_matrix[i].tolist()) + "\n")
        f.close()
        for i in range(length):
            matrix[i][i] = 1
            for j in range(i+1,length):
                try:
                    matrix[i][j] = get_distance_cos(gist_matrix[i], gist_matrix[j])
                    matrix[j][i] = matrix[i][j]
                except:
                    matrix[i][j] = -1
                    print(str(i)+"," + str(j))
            print(matrix[i])

        path = "E:\TRP\output\\" + str(num)+ "\\" + "gist_res.txt"
        f = open(path, "w")
        for i in range(length):
            f.write(str(matrix[i])+"\n")
        f.close()




