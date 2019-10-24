#coding=utf-8
'''
Created on 2017-12-6

'''

from src.main.util import ImgProcess
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import fetch_mldata
from src.main.util.CST import URL
import numpy as np
import pickle
import gzip
import cv2


url = URL.getResPath("images/test/numbers.jpg")
img = cv2.imread(url, cv2.IMREAD_UNCHANGED)
img, imgbinary, rectList = ImgProcess.imgProcess(img)


# 加载数据
# mnist = fetch_mldata("MNIST original")
url=URL.getResPath("data/train_data.gz")
with gzip.open(url) as fp:
    training_data,valid_data,test_data = pickle.load(fp,encoding="bytes")
x_training_data,y_training_data = training_data
x_valid_data,y_valid_data = valid_data
x_test_data,y_test_data = test_data
classes = np.unique(y_test_data)

# 将验证集和训练集合并
x_training_data_final = np.vstack((x_training_data,x_valid_data))
y_training_data_final = np.append(y_training_data,y_valid_data)



# 设置神经网络模型参数
# mlp = MLPClassifier(solver='lbfgs', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
# 使用solver='lbfgs',准确率为79%，比较适合小(少于几千)数据集来说，且使用的是全训练集训练，比较消耗内存
# mlp = MLPClassifier(solver='adam', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
# 使用solver='adam'，准确率只有67%
mlp = MLPClassifier(solver='sgd', activation='relu',alpha=1e-4,hidden_layer_sizes=(56,56), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
# 使用solver='sgd'，准确率为98%，且每次训练都会分batch，消耗更小的内存

# 训练模型
print("训练start")
mlp.fit(x_training_data_final, y_training_data_final)
print("训练完成")
#srcimg,processimg,rectList,model
resultImg,processimg,resultList=ImgProcess.imgSklearnPredicted(img,imgbinary,rectList,mlp)
cv2.imshow("re", resultImg)
cv2.imshow("pro",processimg)
cv2.imwrite("res.jpg",resultImg)
print(resultList)
cv2.waitKey()
#mlp.predict()
# 查看模型结果
print(mlp.score(x_test_data,y_test_data))  #0.971
print(mlp.n_layers_) #4
print(mlp.n_iter_)   #10  迭代次数
print(mlp.loss_)     #0.03失误
print(mlp.out_activation_)
# Iteration 1, loss = 0.31452262
# Iteration 2, loss = 0.13094946
# Iteration 3, loss = 0.09715855
# Iteration 4, loss = 0.08033498
# Iteration 5, loss = 0.06761733
# Iteration 6, loss = 0.06085069
# Iteration 7, loss = 0.05485305
# Iteration 8, loss = 0.04950742
# Iteration 9, loss = 0.04468061
# Iteration 10, loss = 0.04156696
# D:\Python27\lib\site-packages\sklearn\neural_network\multilayer_perceptron.py:563: ConvergenceWarning: Stochastic Optimizer: Maximum iterations reached and the optimization hasn't converged yet.
#   % (), ConvergenceWarning)
# 0.9726
# 4
# 10
# 0.0415669639552
# softmax
