import os
from skimage import io,filters
import numpy as np
import csv
from matplotlib import pyplot as plt




#图片矩阵大小
N=28
#灰度阈值
# color=170/255

##读取图片  ok
#file为绝对路径,比如：'F:\\2.png'
#对图片进行二值化，切割，拉伸处理
#返回图片矩阵，矩阵大小为：28*28
def readPicture(file):

    #二值化图片
    img=io.imread(file,as_gray=True)
    #otsu算法自动计算阈值
    color=filters.threshold_otsu(img)
    for i in range(0, img.shape[0]):
        for j in range(0,img.shape[1]):
            img[i][j]=0 if img[i][j] > color else 1

    #切割图片
    img,size=cutImg(img)
    #无可切割点（无像素）则返回-1
    if size==-1:
        return -1
    #拉伸图片
    img=ratioImg(img)
    # plt.imshow(img, cmap='Greys', interpolation='None')
    # plt.show()
    return  img

##输出目录下全部图片矩阵至'data.csv'， Ok
#dir为绝对路径，如"F:\\abc"，classify为True则以文件名对图片分类
# 大小为N*(28*28+1),
# 第一列为每行的类别，为1则代表该图片数字值为1，若classify为false则第一列为-1
def appendCsvFileByDirectry(dir,classify):
    files =[]#文件列表
    Pictures =[]#返回结果
    filelist= os.listdir(dir)
    for file in filelist:
        if os.path.isfile(dir+'\\'+file) and (file.endswith('jpg') or file.endswith('png')) :
            files.append(file)
    long=len(files)
    #处理每行,按名字分类
    for file in files:
        pic = np.zeros(N * N + 1)
        pic[1:28 * 28 + 1] = readPicture(dir + "\\" + file).reshape(N * N)
        pic[0:1] = int(file.split('.')[0]) if classify else -1
        pic = pic.flatten()
        Pictures = pic if (Pictures == [])   else  np.r_[Pictures, pic]
    Pictures=Pictures.astype(int).reshape(len(files), N * N + 1)
    csvfile=open('data.csv','a',newline='')
    csv.writer(csvfile,delimiter=',').writerows(Pictures)
    csvfile.close()

##输出指定文件图片矩阵至'data.csv'，OK
#filename为绝对路径，如"F:\\7.png"，classify为True则以文件名对图片分类
# 大小为N*(28*28+1),
# 第一列为每行的类别，为1则代表该图片数字值为1，若classify为false则第一列为-1
def appendCsvFileByFileName(filename,classify):
    if os.path.isfile(filename) and (filename.endswith('jpg') or filename.endswith('png')):
        Picture = []  # 返回结果
        pic = np.zeros(N * N + 1)
        pic[1:28 * 28 + 1] = readPicture(filename).reshape(N * N)
        pic[0:1] = int(filename.split('.')[-2].split('\\')[-1]) if classify else -1
        pic = pic.flatten()
        Picture = pic if (Picture == [])   else  np.r_[Picture, pic]
        csvfile = open('data.csv', 'a', newline='')
        csv.writer(csvfile, delimiter=',').writerow(Picture)
        csvfile.close()
#切割图片函数 0k
def cutImg(img):
    #存放图片边界
    size={'top':-1,'right':-1,'bottom':-1,'left':-1,'flag':-1}
    for i in range(0, img.shape[0]):
        for j in range(0,img.shape[1]):
            if img[i][j]==1:
                size['flag']=1
                #最小上边界
                if size['top']==-1 :
                    size['top']=i
                #最小左边界
                if size['left']==-1 or j<size['left']:
                    size['left']=j
                #最大右边界
                if j>size['right']:
                    size['right']=j
                #最大下边界
                if i>size['bottom']:
                    size['bottom']=i
    if size['flag']!= -1:
        return img[size['top']:size['bottom']+1,size['left']:size['right']+1],size
    return -1,-1

 #等比例拉伸至 N*N  即28*28
#首先需要将图片补全为正方形图片，之后再采样，防止数字比例失调 ok
def ratioImg(img):
    # 图片最大的长或宽
    height=len(img)
    width=len(img[0])
    # 存储补全后的方形图片
    squareImg=[]
    #分类补全，将图片处理为正方形，使数子居中
    #若高>宽
    if height > width:
        squareImg = np.zeros(height*height).reshape(height,height)#方形图片
        for i in range(0,height):
            for j in range(0,width):
                squareImg[i][j+int(np.floor((height-width)/2))]=img[i][j]
    #若高<宽
    if width>=height:
        squareImg = np.zeros(width * width).reshape(width, width)  # 方形图片
        for i in range(0, height):
            for j in range(0, width):
                squareImg[i++ int(np.floor((width - height) / 2))][j] = img[i][j]

    # #开始压缩
    #  压缩比例，采样间隔
    ratio = len(squareImg)/N

    ##初始化一个N*N数组,存放最终压缩的图片
    Img=np.ones(N**2).reshape(N,N)
    for i in range(0,N):
        for j in range(0,N):
            Img[i][j]=squareImg[int(np.floor(i*ratio))][int(np.floor(j*ratio))]#每隔N一端距离取值给压缩后的点
    return Img








