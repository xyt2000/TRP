# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/3/25 21:54
# software: PyCharm

"""
文件说明：
"""
for num in range(1, 21):
    path1 = "E:\TRP\\early_data\\min-max\\" + str(num) + "\\" + "tfidf_vector.txt"
    path2 = "E:\TRP\\early_data\\min-max\\" + str(num) + "\\" + "ocr_tfidf_vector.txt"
    f1 = open(path1, "r")
    f2 = open(path2, "r")
    tfidf = []
    ocr = []
    for line1,line2 in list(zip(f1.readlines(),f2.readlines())):
        line1 = line1[1:-2].replace("\n","")
        line2 = line2[1:-2].replace("\n","")
        line1list = line1.split(", ")
        n1 = 1145-len(line1list)
        for i in range(n1):
            line1list.append('0.0')
        line2list = line2.split(", ")
        n2 = 1423 - len(line2list)
        for j in range(n2):
            line2list.append('0.0')
        ocr.append(line2list)
        tfidf.append(line1list)

    tfidf_ = []
    for line in tfidf:
        tfidf_.append(list(map(float, line[:])).copy())
    ocr_ = []
    for line in ocr:
        ocr_.append(list(map(float, line[:])).copy())
    path3 = "E:\TRP\early_data\\min-max\\" + str(num) + "\\" + "ocr_tfidf_vector_fill.txt"
    f3 = open(path3,"w")
    for line in ocr_:
        f3.write(str(line)+"\n")
    f3.close()

    path4 = "E:\TRP\early_data\\min-max\\" + str(num) + "\\" + "tfidf_vector_fill.txt"
    f4 = open(path4, "w")
    for line in tfidf_:
        f4.write(str(line) + "\n")
    f4.close()