import src.main.util.Image as im
from matplotlib import pyplot as plt

from threading import Thread, Lock
img=im.readPicture('F:\\abc\\9.png')
#
plt.imshow(img, cmap='Greys', interpolation='None')
plt.show()
# im.appendCsvFileByDirectry("F:\\abc",True)
# im.appendCsvFileByFileName("F:\\7.png",False)