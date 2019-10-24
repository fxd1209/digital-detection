#!/usr/bin/env python

#-*- coding:utf-8 -*-
import cv2
from src.main.util import ImgProcess
from src.main.util import ann as A
from src.main.util.CST import URL
import time
def main():
    t1 = time.time()
    url=URL.getResPath("images/test/numbers.jpg")
    ann, test_data = A.train(A.create_ann(500), 50000, 5)
    #A.test(ann,test_data)
    img=cv2.imread(url, cv2.IMREAD_UNCHANGED)
    img, imgbinary, rectList=ImgProcess.imgProcess(img)
    img, resultImg,resultList=ImgProcess.imgPredicted(img, imgbinary, rectList, ann)
    cv2.imshow("re",resultImg)
    print(resultList)
    t2 = time.time()
    print(t2)
    cv2.waitKey()


if __name__ == '__main__':
    main()