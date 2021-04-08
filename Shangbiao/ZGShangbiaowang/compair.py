from PIL import Image
import math
import operator
from functools import reduce
import os
def compare(pic1,pic2):
    '''
    :param pic1: 图片1路径
    :param pic2: 图片2路径
    :return: 返回对比的结果
    '''
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))

    # print(differ)
    return differ

for i in range(1, 4249):
    if not os.path.exists(r'C:\Users\admin\Downloads\{}.jpg'.format(i)) or not os.path.exists(r'C:\Users\admin\Downloads\{}.jpg'.format(i+1)):
        continue
    # print('正在对比的图片为：%s 和%s'%(i,i+1))
    if not compare(r'C:\Users\admin\Downloads\{}.jpg'.format(i),r'C:\Users\admin\Downloads\{}.jpg'.format(i+1)):
        print(i,i+1)

