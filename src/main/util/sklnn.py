import cv2
import pickle
import numpy as np
import gzip
from src.main.util.CST import URL
from sklearn.neural_network import MLPClassifier


# 让数组输出不用省略号代替
# np.set_printoptions(threshold=np.inf)

def loadData(url):
    # mnist = gzip.open(url, 'rb')
    trainRar = gzip.open(URL.getResPath("data/train_data.gz"), 'rb')
    # train_data是一个元组 第一个元组是一个二维数组，其中每一行为一张图片的一为存储，第二个元组为对应的结果值
    train_data, class_data, test_data = pickle.load(trainRar, encoding='bytes')
    trainRar.close()
    return (train_data, class_data, test_data)


def decompreData(url):
    # 加载数据集
    train_data, validation_data, test_data = loadData(url)
    x_training_data, y_training_data = train_data
    x_valid_data, y_valid_data = validation_data
    x_test_data, y_test_data = test_data
    classes = np.unique(y_test_data)
    # 将验证集和训练集合并
    x_training_data_final = np.vstack((x_training_data, x_valid_data))
    y_training_data_final = np.append(y_training_data, y_valid_data)

    return (x_training_data_final,y_training_data_final, x_test_data,y_test_data)





def create_mlp(hidden_layer_sizes=(100,), activation="relu",
                 solver='adam', alpha=0.0001,
                 batch_size='auto', learning_rate="constant",
                 learning_rate_init=0.001, power_t=0.5, max_iter=200,
                 shuffle=True, random_state=None, tol=1e-4,
                 verbose=False, warm_start=False, momentum=0.9,
                 nesterovs_momentum=True, early_stopping=False,
                 validation_fraction=0.1, beta_1=0.9, beta_2=0.999,
                 epsilon=1e-8, n_iter_no_change=10):
    # 设置神经网络模型参数
    # mlp = MLPClassifier(solver='lbfgs', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
    # 使用solver='lbfgs',准确率为79%，比较适合小(少于几千)数据集来说，且使用的是全训练集训练，比较消耗内存
    # mlp = MLPClassifier(solver='adam', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
    # 使用solver='adam'，准确率只有67%
    mlp = MLPClassifier( hidden_layer_sizes, activation,
                 solver, alpha,
                 batch_size, learning_rate,
                 learning_rate_init, power_t, max_iter,
                 shuffle, random_state, tol,
                 verbose, warm_start, momentum,
                 nesterovs_momentum, early_stopping,
                 validation_fraction, beta_1, beta_2,
                 epsilon, n_iter_no_change)
    # 使用solver='sgd'，准确率为98%，且每次训练都会分batch，消耗更小的内存
    return mlp


def train(x_training_data,y_training_data,mlp):
    mlp=mlp.fit(x_training_data, y_training_data)
    return mlp


def test(x_test_data, y_test_data,mlp):
    print(mlp.score(x_test_data, y_test_data))
    print(mlp.n_layers_)
    print(mlp.n_iter_)
    print(mlp.loss_)
    print(mlp.out_activation_)



def predictSklearn(clf, sample):
    data = sample.copy()
    rows, cols = data.shape
    if (rows != 28 or cols != 28) and rows * cols > 0:
        data = cv2.resize(data, (28, 28), interpolation=cv2.INTER_LINEAR)
    return clf.predict(np.array([data.ravel()], dtype=np.float32))


"""
ann, test_data = train(create_ANN())
test(ann, test_data)
"""

