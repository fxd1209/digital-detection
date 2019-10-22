import os
import sys
#常量池
MENU_FILE_ITME_OPEN=2





BTN_READ_FILE=10
BTN_OCR_IMG=11
BTN_EXPORT_EXCEL=12
BTN_BITMAP_SHOW=13

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

    @staticmethod
    def getFileNameByUrl(url):
        file = os.path.splitext(url)
        filename, type = file
        return filename

    @staticmethod
    def getFileTypeByUrl(url):
        file = os.path.splitext(url)
        filename, type = file
        return type