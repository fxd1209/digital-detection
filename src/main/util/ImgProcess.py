#图片处理函数
import cv2
import numpy as np
from src.main.util import ann as A
def imgProcess(srcImg):
    img = srcImg
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imggray = cv2.GaussianBlur(imggray, (7, 7), 0)

    # 训练集数据为 白色背景黑色字，所以此处需要将其二值化为一样的
    ret, imgbinary = cv2.threshold(imggray, 127, 255, cv2.THRESH_BINARY_INV)
    #腐蚀
    #imgbinary = cv2.erode(imgbinary, np.ones((2, 2), np.uint8), iterations=2)
    # 分开图像中的各个数字，并找出轮廓
    contours, hier = cv2.findContours(imgbinary.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 通过轮廓来迭代，并且放弃完全包含在其他矩形中的矩形，只添加不包含在其他矩形中和不超过图像宽度的好的矩形
    rectList = []
    for c in contours:
        r = x, y, w, h = cv2.boundingRect(c)
        a = cv2.contourArea(c) #获取矩形的面积
        b = (img.shape[0] - 3) * (img.shape[1] - 3) #获取图片的大概面积,矩形识别有可能边图片边框识别进去，如果面积差不多，就不要这个边框
        is_inside = False
        for q in rectList:
            if isRectInside(r, q):
                is_inside = True
                break
        if not is_inside:
            if not a == b:
                rectList.append(r)
    return img,imgbinary,rectList



def imgPredicted(srcimg,processimg,rectList,model):
    resultList=[]
    resultImg=srcimg.copy()
    for r in rectList:
        x, y, w, h = digitRect(r)
        cv2.rectangle(resultImg, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
        roi = processimg[int(y):int(y + h), int(x):int(x + w)]
        try:
            digit_value = int(A.predict(model,roi.copy())[0])
            resultList.append(digit_value)
        except:
            continue
        cv2.putText(resultImg, "%d" % digit_value, (int(x), int(y - 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    return srcimg,resultImg,resultList


def imgSklearnPredicted(srcimg,processimg,rectList,model):
    resultList=[]
    resultImg=srcimg.copy()
    for r in rectList:
        x, y, w, h = digitRect(r)
        cv2.rectangle(resultImg, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
        roi = processimg[int(y):int(y + h), int(x):int(x + w)]
        try:
            digit_value = int(A.predictSklearn(model,roi.copy())[0])
            resultList.append(digit_value)
        except:
            continue
        cv2.putText(resultImg, "%d" % digit_value, (int(x), int(y - 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    return (resultImg,processimg,resultList)






#一个矩形是否完全包含在另一个矩形中
def isRectInside(r1, r2):
  x1,y1,w1,h1 = r1
  x2,y2,w2,h2 = r2
  if ((x1 > x2) and (y1 > y2) and (x1+w1 < x2+w2) and (y1+h1 < y2 + h2)) or ((x1<x2) and (y1<y2) and (x1+w1 > x2+w2) and (y1+h1 > y2+ h2)):
    return True
  else:
    return False


#获取数字周围的矩形，并将其转化为正方形，在数字上对其中心化，
# 有5个空点来保证数字在正方形中
def digitRect(rect):
  x, y, w, h = rect
  padding = 10
  Xo = x + w/2
  Yo = y + h/2
  if (h > w):
    w = h
    x = Xo - (w/2)
  else:
    h = w
    y = Yo - (h/2)
  return (x-padding, y-padding, w+padding, h+padding)