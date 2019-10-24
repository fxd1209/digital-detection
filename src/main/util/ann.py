import cv2
import pickle
import numpy as np
import gzip
from src.main.util.CST import URL

#让数组输出不用省略号代替
#np.set_printoptions(threshold=np.inf)

def loadData(url):
  #mnist = gzip.open(url, 'rb')
  trainRar = gzip.open(URL.getResPath("data/train_data.gz"), 'rb')
  #train_data是一个元组 第一个元组是一个二维数组，其中每一行为一张图片的一为存储，第二个元组为对应的结果值
  train_data, class_data, test_data = pickle.load(trainRar,encoding='bytes')
  # list=[]
  # for i in range(15):
  #   list.append(train_data[0][i].reshape(28, 28))
  # cv2.imshow(u"训练集部分图片预览", np.hstack(list))
  # cv2.waitKey()
  trainRar.close()
  return (train_data, class_data, test_data)

def decompreData():
  #加载数据集
  train_data, validation_data, test_data = loadData("")
  tr_inputs = []
  tr_results = []
  # 将训练数据集独立出输入值和结果值
  for x in train_data[0]:
    tr_inputs.append(np.reshape(x,(784,1)))
  for x in train_data[1]:
    #向量化结果，因为所有操作是向量操作，如果这个数字是5，就讲数组第5个标记为1.0
    tr_results.append(vectorizedResult(x))
  # 打包为元组的列表,即将 图片和结果一一映射(图片数组向量,结果向量)
  tr_data = zip(tr_inputs, tr_results)

  val_inputs = []
  for x in validation_data[0]:
    val_inputs.append(np.reshape(x, (784, 1)))
  val_data = zip(val_inputs, validation_data[1])

  test_inputs = []
  for x in test_data[0]:
    test_inputs.append(np.reshape(x, (784, 1)))
  te_data = zip(test_inputs, test_data[1])

  return (tr_data, val_data, te_data)


#向量化结果集
def vectorizedResult(j):
  array = np.zeros((10, 1))  #0填充10行一列的二维数组
  array[j] = 1.0
  return array

def create_ann(hidden = 20):
  ann = cv2.ml.ANN_MLP_create()
  #设置拓扑结构
  ann.setLayerSizes(np.array([784, hidden, 10]))
  ann.setTrainMethod(cv2.ml.ANN_MLP_RPROP)  #使用bp反向传播的方式
  ann.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM) #设置激活函数为sigmodid
  """
  设置迭代终止条件
  type是类型，COUNT-达到醉倒迭代次数时终止。EPS为当迭代终止条件达到阈值时终止,COUNT+EPS将最大迭代次数和阈值都作为终止条件
  maxCount是迭代的最大次数，
  epsilon是特定的阈值
  """
  ann.setTermCriteria((cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1))
  return ann

#ann,样本数量,迭代次数
def train(ann, samples = 10000, times = 1):
  tr_d, val_d, test_d =decompreData()
  for x in range(times):
    counter = 0
    tr_d, val_d, test_d = decompreData()
    for img in tr_d:
      if (counter > samples):
        print("内层")
        break
      if (counter % 500 == 0):
        print("迭代次数 %d: 已完成 %d/%d" % (x+1, counter, samples))
      counter += 1
      data, digit = img #压缩的时候，是把图片矩阵和结果映射打包为元组的
      # print(digit)
      # cv2.imshow("tet",data.reshape(28,28))
      # cv2.waitKey()
      #ravel()合并数组 如[[1,2,3],[4,5,6]],合并为[1,2,3,4,5,6]
      #train data, ROW_SAMPLE, labelsMat
      ann.train(np.array([data.ravel()], dtype=np.float32), cv2.ml.ROW_SAMPLE, np.array([digit.ravel()], dtype=np.float32))
    print("迭代次数 %d 完成" % int(x+1))
  return ann,test_d
  
def test(ann, test_data):
  temp=list(test_data)
  sample = np.array(temp[0][0].ravel(), dtype=np.float32).reshape(28, 28)
  # cv2.imshow("sample", sample)
  # cv2.waitKey()
  print(ann.predict(np.array([temp[0][0].ravel()], dtype=np.float32)))

def predict(ann, sample):
  data = sample.copy()
  rows, cols = data.shape
  if (rows != 28 or cols != 28) and rows * cols > 0:
    data = cv2.resize(data, (28, 28), interpolation = cv2.INTER_LINEAR)
  return ann.predict(np.array([data.ravel()], dtype=np.float32))


def predictSklearn(clf, sample):
  data = sample.copy()
  rows, cols = data.shape
  if (rows != 28 or cols != 28) and rows * cols > 0:
    data = cv2.resize(data, (28, 28), interpolation = cv2.INTER_LINEAR)
  return clf.predict(np.array([data.ravel()], dtype=np.float32))

"""
ann, test_data = train(create_ANN())
test(ann, test_data)
"""

