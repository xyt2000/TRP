# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/1/9 16:54
# software: PyCharm

"""
文件说明：
"""
for num in range(1,21):
    print(num)
    word_path = "../output//" + str(num) + "/" +"edit" + ".txt"
    matrix = []
    f = open(word_path,"r")
    for line in f.readlines():
        line = line.replace("\n", "")
        line = line[1:-1]
        line = line.split(", ")
        line = list(map(int, line))
        matrix.append(line)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 1/matrix[i][j]
    f.close()
    path = "../output//" + str(num) + "/" +"edit_sim" + ".txt"
    f = open(path,"w")
    for line in matrix:
        f.write(str(line)+"\n")
    f.close()