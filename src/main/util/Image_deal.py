import cv2
import numpy as np

from src.main.util.CST import URL


def readPicture(file):
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯模糊
    blur_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
    # 二值化
    test, binary_img = cv2.threshold(blur_img, 127, 255, cv2.THRESH_BINARY)
    # 做形态学的改变
    kernel = np.ones((7, 7), np.uint8)
    erosion = cv2.erode(binary_img, kernel, iterations=1)
    cv2.bitwise_not(erosion, binary_img)  # 取反
    # 轮廓检测，绘制矩形图
    contours, hierar = cv2.findContours(binary_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rectList = []
    for rect in contours:
        r = x, y, w, h = cv2.boundingRect(rect)
        Flag = False
        for q in rectList:
            if isReactInside(r, q):
                Flag = True
                break
        if not Flag:
            rectList.append(r)
        x0 = x + 2 / w
        y0 = y + 2 / h
        if h > w:
            w = h
            x = x0 - 2 / w
        else:
            h = w
            y = y0 + 2 / h
        cv2.rectangle(binary_img, (x, y), (x + w, y + h), (255, 0, 0))

    cv2.imshow("test", binary_img)
    cv2.waitKey()


# 判断矩阵是否为内部矩阵
def isReactInside(r1, r2):
    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2

    if x1 < x2 and y1 < y2 and w1 > w2 and h1 > h2:
        return True
    else:
        return False


# 矩形转化为正方形
# def rect_trans(rect):
#     x,y,w,h = rect
#     x0 = x+ 2/w
#     y0 = y + 2/h
#     if h>w:
#         w = h
#         x1 = x0- 2/w
#         y1 = y
#     else:
#         h = w
#         y1 = y0 + 2/h
readPicture(URL.getResPath('images/logo/numbers.png'))
