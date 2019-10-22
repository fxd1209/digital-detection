import sys,os
path = sys.path[0]
print(path)

p=os.getcwd()
print(p)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("digital-detection\\")+len("digital-detection\\")]  # 获取myProject，也就是项目的根路径
dataPath = os.path.abspath(rootPath + 'data\\train.csv') # 获取tran.csv文件的路径
