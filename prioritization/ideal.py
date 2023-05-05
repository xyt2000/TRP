# author:xuyutao
# contact: 1026310947@qq.com
# datetime:2023/2/28 20:28
# software: PyCharm

"""
文件说明：
"""
def sums(num):
    return num*(num-1)/2

nums = [276,134,29,9,13,26,152,41,75,26,5,10,17,131,88,51,4,294,12,24]
Categories = [20, 9, 6, 8, 3, 4, 8, 4, 7, 5, 3, 2, 9, 8, 15, 8, 2, 12, 3, 5]
for i in range(20):
    ideal_apfd = 1 + 1 / (2 * nums[i]) - sums(Categories[i]) / (nums[i]*Categories[i])
    print(ideal_apfd)
