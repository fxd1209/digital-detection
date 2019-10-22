import numpy as np
from matplotlib import pyplot as plt

data_file = open('data.csv', 'r')
data_list = data_file.readlines()
data_file.close()
all_values = data_list[3].split(',')
print(all_values[0])
#每行转换为二维数组
image_array = np.array(all_values[1:]).astype(np.int).reshape((28, 28))
plt.imshow(image_array, cmap='Greys', interpolation='None')
plt.show()
