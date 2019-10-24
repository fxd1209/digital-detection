import os
import sys
import time
from PIL import Image
#常量池
MENU_FILE_ITME_OPEN=2  #open image
MENU_FILE_ITME_OPENS=3  #open images
MENU_FILE_ITME_EXIT=4  #open images

MENU_SKIN_ITME_ONE=5
MENU_SKIN_ITME_TWO=6
MENU_SKIN_ITME_THREE=7
MENU_SKIN_ITME_FOUR=8
MENU_SKIN_ITME_FIVE=9
MENU_SKIN_ITME_SIX=10
MENU_SKIN_ITME_SEVEN=11




BTN_READ_FILE=10
BTN_OCR_IMG=11
BTN_EXPORT_EXCEL=12
BTN_BITMAP_SHOW=13
BTN_OCR_TRAIN=14
BTN_IMG_PRO=15  #处理图片

class URL:
    @staticmethod
    def getRootPath():
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find("digital-detection\\") + len("digital-detection\\")]  # 获取myProject，也就是项目的根路径
        return rootPath

    @staticmethod
    def getResPath(relPath):
        dataPath = os.path.abspath(URL.getRootPath() + relPath )  # 获取tran.csv文件的路径
        return dataPath

    #根据路径获取文件（含有后缀）
    @staticmethod
    def getFileNameByUrl(url):
        return os.path.basename(url)

    #根据路径获取没有后缀的文件名
    @staticmethod
    def getFileNameByUrlNoSuffix(url):
        file=os.path.basename(url)  #去掉各种路径，只剩下 name.type  a.txt
        file = os.path.splitext(url)
        filename,type = file
        return filename

    #根据路径获取文件类型
    @staticmethod
    def getFileTypeByUrl(url):
        file = os.path.splitext(url)
        filename, type = file
        return type
    #根据路径获取文件所在路径(文件上级路径)
    @staticmethod
    def getFileDir(url):
        return os.path.dirname(url)

    #获取文件大小 结果精确两位数，单位MB
    @staticmethod
    def getFileSize(url):
        f = os.path.getsize(url)
        f = f / float(1024 * 1024)
        return round(f, 2)

    #获取文件创建时间
    @staticmethod
    def getFileCreateTime(url):
        t = os.path.getctime(url) #时间戳
        return URL.timestamp2datatime(t)

    """
    获取文件修改时间
    """
    @staticmethod
    def getFileModifyTime(url):
        t = os.path.getmtime(url)
        return URL.timestamp2datatime(t)

    #获取图片尺寸
    @staticmethod
    def getImageSize(url):
        img = Image.open(url)
        return img.size

    #获取图片类型
    @staticmethod
    def getImageType(url):
        img = Image.open(url)
        return img.format

    """
    时间戳格式化 1479264792
    2016-11-16 10:53:12
    """
    @staticmethod
    def timestamp2datatime(timestamp):
        convert = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', convert)