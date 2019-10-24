#!/usr/bin/env python

#-*- coding:utf-8 -*-
import cv2
from src.main.util import ImgProcess
from src.main.util import ann as A
from src.main.util.CST import URL
from sklearn.externals import joblib
#from sklearn.neural_network import
import time

def main():

    t1=time.time()
    url=URL.getResPath("images/test/2.png")
                    #56 隐藏层的感知器个数      50000是sample(样本)的个数   5是迭代的次数
    ann, test_data = A.train(A.create_ann(56), 100, 2)
   # joblib.dump(ann,"ann.m")
    #ann=joblib.load("ann.m")
    #A.test(ann,test_data)
    img=cv2.imread(url, cv2.IMREAD_UNCHANGED)
    img, imgbinary, rectList=ImgProcess.imgProcess(img)
    img, resultImg,resultList=ImgProcess.imgPredicted(img, imgbinary, rectList, ann)
    cv2.imshow("re",resultImg)
    print(resultList)
    t2=time.time()
    t3=t2-t1
    print(t3)
    cv2.waitKey()


if __name__ == '__main__':
    main()