#!/usr/bin/env python

#-*- coding:utf-8 -*-
import cv2
import wx
from src.main.Desktop import MainWin
import time



def main():
    ex = wx.App()
    mainWin=MainWin(None)
    mainWin.Show(True)
    ex.MainLoop()
if __name__ == '__main__':
    main()


    """
    ann
    url = URL.getResPath("images/test/2.png")
    # 56 隐藏层的感知器个数      50000是sample(样本)的个数   5是迭代的次数
    model, test_data = A.train(A.create_ann(100), 50000, 30)
    img = cv2.imread(url, cv2.IMREAD_UNCHANGED)
    img, imgbinary, rectList = ImgProcess.imgProcess(img)
    img, resultImg, resultList = ImgProcess.imgPredicted(img, imgbinary, rectList, model)
    cv2.imshow("re", resultImg)
    cv2.waitKey()

    """


    """
    #sknn调用
        url = URL.getResPath("images/test/2.png")
        model=S.create_mlp(solver='sgd', activation='relu',alpha=1e-4,hidden_layer_sizes=(56,56), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
        x_training_data, y_training_data, x_test_data, y_test_data=S.decompreData("")
        model=S.train(x_training_data,y_training_data,model)
        joblib.dump(model,"skmpl.m")
        model=joblib.load("skmpl.m")
        S.test(x_test_data,y_test_data,model)
    
        img=cv2.imread(url, cv2.IMREAD_UNCHANGED)
        img, imgbinary, rectList=ImgProcess.imgProcess(img)
        resultImg, processimg, resultList=ImgProcess.imgSklearnPredicted(img, imgbinary, rectList, model)
        cv2.imshow("re",resultImg)
        cv2.waitKey()
    """

