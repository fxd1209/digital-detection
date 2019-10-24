"""
7、多线程
在上面介绍中，我们都是在主线程操作，实际应用中，多线程是必要的：

不用多线程可能会导致图形界面卡死
多线程可以使程序以更高效率运行
多线程可以让程序做更多的事
简单用法：

import threading
def ThreadBatchUpLoad(self,arg):
    print("thread run")

def Onclick(self,event):
    t1 = threading.Thread(target=self.ThreadBatchUpLoad, args=(event,))
    t1.start()
"""


import wx
import os
from PIL import Image
from src.main.util import CST
from src.main.util.CST import URL
from src.main.util import sklnn as S
from sklearn.externals import joblib
from src.main.util import ImgProcess
from src.main.util import excel
import threading
import time
import cv2
import numpy as np




class MainWin(wx.Frame):
    def __init__(self,*args,**kw):
        super(MainWin,self).__init__(style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX,*args,**kw)

        self.fileNamePath={}     #名字-路径键值对  同一路径下不可能有重复名字，故以名字作为key
        self.srcImgDstImgArea=[]
        self.finishedResList=[] #原图，处理后的图，数字矩形区域，图片名，全路径，结果图路径，过程图路径，结果List
        #top，left, right1Title, right1, right2Title, right2, bottomTitle, bottom
        self.skinList=[
                       [(196, 147, 239), (230, 230, 250), (196, 147, 239), (245, 246, 248), (196, 147, 239), (245, 246, 248),(196, 147, 239), (196, 147, 239)],# skin1
                       [(255,0,0),(250,128,114),(255,0,0),(245,246,248),(255,0,0),(245,246,248),(255,0,0),(255,0,0)],   # skin2
                       [(255,215,0), 	(255,248,220), (255,215,0),(245,246,248),(255,215,0),(245,246,248),(255,255,255),(255,215,0)],   # skin3
                       [(255,182,193), (244,206,205),(255,182,193),(245,246,248),(255,182,193),(245,246,248),(255,182,193),(255,182,193)] ,   # skin4
                       [(92,34,35),(245,247,251),(92,34,35),(245,246,248),(92,34,35),(245,246,248),(92,34,35),(92,34,35)],
                       [(236,118,150),(245,247,251),(236,118,150),(245,246,248),(236,118,150),(245,246,248),(236,118,150),(236,118,150)],
                       [(77,64,48),(245,247,251),(77,64,48),(245,246,248),(77,64,48),(245,246,248),(77,64,48),(77,64,48)]

                       ]


        # 创建菜单栏(MenuBar),在菜单栏里面添加菜单(Menu),在菜单里面加菜单项（menuItem）
        self.menuBar = wx.MenuBar()  # 菜单栏
        self.menu_file = wx.Menu()  # 菜单栏中一文件菜单
        self.menu_skin = wx.Menu()  # 菜单栏中一换肤菜单
        self.menu_help=wx.Menu()
        self.initMenuBar()

        self.sizer = wx.GridBagSizer(0, 0)  # 列间隔，行间隔都为0

        """
        #panel top Start
        """
        self.panelTop = wx.Panel(self)
        self.panelTop.SetMinSize((1120, 30))

        # 在Panel上添加Button
        self.btnReadFile = wx.Button(self.panelTop, id=CST.BTN_READ_FILE, label=u'读取', pos=(330, 0), size=(70, 30))
        self.btnReadFile.SetDefault()
        self.btnReadFile.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/import.gif")))
        self.btnReadFile.Bind(wx.EVT_LEFT_DOWN,self.OnOpenFiles)
        # 在Panel上添加Button
        self.btnOcrTrain = wx.Button(self.panelTop, id=CST.BTN_OCR_TRAIN, label=u"训练", pos=(400, 0), size=(70, 30))
        self.btnOcrTrain.SetDefault()
        self.btnOcrTrain.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/import.gif")))
        self.btnOcrTrain.Bind(wx.EVT_LEFT_DOWN, self.OnTrainClick)
        # 在Panel上添加Button
        self.btnOcr = wx.Button(self.panelTop, id=CST.BTN_IMG_PRO,label=u"处理", pos=(470, 0), size=(70, 30))
        self.btnOcr.SetDefault()
        self.btnOcr.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/identify.gif")))
        self.btnOcr.Bind(wx.EVT_LEFT_DOWN, self.OnProceeClick)

        # 在Panel上添加Button
        self.btnOcr = wx.Button(self.panelTop, id=CST.BTN_OCR_IMG, label=u"识别", pos=(540, 0), size=(70, 30))
        self.btnOcr.SetDefault()
        self.btnOcr.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/identify.gif")))
        self.btnOcr.Bind(wx.EVT_LEFT_DOWN, self.OnOrcClick)

        # 在Panel上添加Button
        self.btnExport = wx.Button(self.panelTop, id=CST.BTN_EXPORT_EXCEL, label=u'导出', pos=(610, 0), size=(70, 30))
        self.btnExport.SetDefault()
        self.btnExport.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/excel.gif")))
        self.btnExport.Bind(wx.EVT_LEFT_DOWN, self.OnExportExcel)


        """
         #panel left Start
        """
        self.panelLeft = wx.Panel(self)
        self.panelLeft.SetMinSize((900,356))


        """
        #panel right Start
        """
        self.panelRight1 = wx.Panel(self)
        self.panelRight1.SetMinSize((220, 178))
        wx.StaticText(self.panelRight1,-1,pos=(0,0),size=(220,20),label="文件列表")
        self.nameListBox = wx.ListBox(self.panelRight1, -1,pos=(0,20),size=(220,158),choices=list(self.fileNamePath.keys()), style=wx.LB_SINGLE,name=u"测试")  # wx.LB_SINGLE只能选择单个
        # 添加事件处理
        self.Bind(wx.EVT_LISTBOX, self.onClickNameListBox,self.nameListBox)


        self.panelRight2 = wx.Panel(self)
        self.panelRight2.SetMinSize((220, 178))
        wx.StaticText(self.panelRight2, -1, pos=(0, 0), size=(220, 158),label="文件信息")
        # parent=None, id=None, label=None, pos=None, size=None, style=0, name=None
        self.fileInfo=wx.StaticText(self.panelRight2,-1,pos=(0,20),size=(220,158))
        self.setFileInfoText(self.nameListBox,self.fileInfo)
        #self.fileInfo.SetLabel("文件信息")

        """
        #panel bottom Start
        """
        self.panelBottom = wx.Panel(self)
        self.panelBottom.SetMinSize((1120, 170))
        wx.StaticText(self.panelBottom, -1, pos=(0, 0), size=(1120, 20), label="识别结果")
        # parent=None, id=None, label=None, pos=None, size=None, style=0, name=None
        self.ocrresult = wx.StaticText(self.panelBottom, -1, pos=(0, 20), size=(1120, 150))


        # 在第0行第0列，添加一个控件，占1行和10列的空间，wx.EXPAND表示控件扩展至填满整个“格子”的空间
        self.sizer.Add(self.panelTop,pos=(0, 0),span=(1, 10),flag=wx.EXPAND | wx.ALL,border=0)
        self.sizer.Add(self.panelLeft, pos=(1, 0), span=(2, 7), flag=wx.EXPAND | wx.ALL, border=1)
        self.sizer.Add(self.panelRight1, pos=(1, 7), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=1)
        self.sizer.Add(self.panelRight2, pos=(2, 7), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=1)
        self.sizer.Add(self.panelBottom, pos=(3, 0), span=(1, 10), flag=wx.EXPAND | wx.ALL, border=1)

        self.SetSizerAndFit(self.sizer)
        self.SetMenuBar(self.menuBar)
        self.SetSize((1120, 560))
        self.SetTitle('数字识别')
        self.Centre()

        self.setSkin(self.skinList,0) #设置默认皮肤为第一个

        self.PanelW, self.PanelH = self.panelLeft.GetSize()  # 展示图片区域的宽高，以留着展示图片用
        self.ImgW, self.ImgH = (0,0)
        self.ImgX,self.ImgY=0,0
        self.ImgBit=""
        self.setShowImage(self.panelLeft,URL.getResPath("images/logo/ocr_bg.jpg"))
        self.train_processing_value=1  #训练进度条初始值
        self.img_proccessing_value=1   #处理图片进度条初始值
        self.img_ocr_value=1            #识别图片进度条初始值


    def initMenuBar(self):
        # 文件菜单的菜单项
        # menuBar,parentMenu,itemId,itemName,itemBgUrl,EVENT_MENU,fun
        self.createAndBindMenuItem(self.menuBar, self.menu_file, CST.MENU_FILE_ITME_OPEN, "打开图片", "", wx.EVT_MENU,
                                   self.OnOpenFile)
        self.createAndBindMenuItem(self.menuBar, self.menu_file, CST.MENU_FILE_ITME_OPENS, "打开图片们", "",
                                   wx.EVT_MENU,
                                   self.OnOpenFiles)
        self.createAndBindMenuItem(self.menuBar, self.menu_file, CST.MENU_FILE_ITME_EXIT, "退出", "",
                                   wx.EVT_MENU,
                                   self.OnExitClick)
        # 换肤菜单的菜单项
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_ONE, "基佬紫", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_TWO, "性感红", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_THREE, "金色稻田", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_FOUR, "粉红女郎", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_FIVE, "暗玉紫", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_SIX, "淡绛红", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_SEVEN, "淡松烟", "", wx.EVT_MENU,
                                       self.OnChangeSkin)

        self.createAndBindMenuItem(self.menuBar, self.menu_help,-1, "使用", "",
                                   wx.EVT_MENU,
                                   self.OnHelpChlick)

        self.menuBar.Append(self.menu_file, '&文件')
        self.menuBar.Append(self.menu_skin, '&换肤')
        self.menuBar.Append(self.menu_help, '&帮助')

    #点击文件列表里面文件 响应事件函数
    def onClickNameListBox(self, event):
        listbox = event.GetEventObject()
        self.setShowImageOnListBoxChange(listbox)
        self.setFileInfoText(self.nameListBox, self.fileInfo)



    def setShowImage(self,parent,url):
        parent.DestroyChildren() #抹掉原先显示的图片
        imgW,imgH=self.ImgW,self.ImgH
        image=Image.open(url)

        self.ImgW, self.ImgH = image.size
        if self.ImgH>self.PanelH:  #按照比例进行缩小
            ratio=self.ImgH/self.ImgW #原比例
            self.ImgH=self.PanelH-4  #使得高一定小于展示panel
            self.ImgW=self.ImgH/ratio

        #图片位置居中
        self.ImgX = self.PanelW / 2 - self.ImgW / 2
        self.ImgY = self.PanelH / 2 - self.ImgH / 2

        #重置图片大小
        if URL.getFileTypeByUrl(url)==".jpg" or URL.getFileTypeByUrl(url)==".jpeg":
            image = wx.Image(url,wx.BITMAP_TYPE_JPEG)
        elif URL.getFileTypeByUrl(url)==".png":
            image = wx.Image(url, wx.BITMAP_TYPE_PNG)
        image = image.Rescale(self.ImgW, self.ImgH)
        self.ImgBit = image.ConvertToBitmap()
        # 通过计算获得图片的存放位置
        self.bitmapButton = wx.BitmapButton(parent, -1,self.ImgBit, pos=(self.ImgX, self.ImgY),size=(self.ImgW,self.ImgH))





    #设置文件列表   n 设置选中第几项
    def setNameListBox(self,n=0):
        # 清空文件列表
        self.nameListBox.Clear()
        for name in list(self.fileNamePath.keys()):
            self.nameListBox.Append(name)
        # 如果ListBox中有值，设置选中
        if self.nameListBox.GetCount() >= 1:
            self.nameListBox.SetSelection(n)

    def setFileInfoText(self,listBox,staticText):
        if listBox.GetCount()>=1:
            selectionString = listBox.GetStringSelection()
            url = self.fileNamePath.get(selectionString)
            filename = URL.getFileNameByUrl(url)
            filetype = URL.getFileTypeByUrl(url)
            filesize = URL.getFileSize(url)  # 文件大小 mb
            filecreatetime = URL.getFileCreateTime(url)
            filemodifytime = URL.getFileModifyTime(url)
            imagesize = URL.getImageSize(url)  # 图片分辨率

            strz = "名称:\t" + filename + "\n" \
                   + "类型:\t" + filetype + "\n" \
                   + "大小:\t" + str(filesize) + "MB\n" \
                   + "尺寸:\t" + str(imagesize[0])+"*"+str(imagesize[1])+"\n" \
                   + "创建时间:"+filecreatetime+"\n" \
                   + "修改时间:"+filemodifytime
            staticText.SetLabel(strz)

    def setShowImageOnListBoxChange(self,listBox):
        # 根据选中的名字获取图片展示
        selectionString = listBox.GetStringSelection()
        self.setShowImage(self.panelLeft, self.fileNamePath.get(selectionString))

    def setResultText(self):
        # self.finishedResList存储顺序：原图，处理后的图，数字矩形区域，图片名，全路径，结果图路径，过程图路径，结果List
        for res in self.finishedResList:
            strc=self.ocrresult.GetLabel()
            imgname=res[3]
            imgfullpath=res[4]
            imgresList=res[7]
            num_list_new = [str(x) for x in imgresList]
            print(imgresList)
            strz=strc+"\n"+"图片名:"+imgname+"\t"+"路径:imgfullpath"+imgfullpath+"\t"+"结果集:"+",".join(num_list_new)
            self.ocrresult.SetLabel(strz)

    def showResultImg(self):
        print(len(self.finishedResList))
        if len(self.finishedResList)>0:
            for res in self.finishedResList:
                strc = self.ocrresult.GetLabel()
                imgname = res[3]
                imgfullpath = res[4]
                resfullpath = res[5]
                profullpath = res[6]
                resimg = cv2.imread(resfullpath)
                proimg = cv2.imread(profullpath)
                cv2.namedWindow(imgname, 0)
                cv2.resizeWindow(imgname, 1120, 560)
                cv2.imshow(imgname, np.hstack([resimg, proimg]))
            cv2.waitKey()



    def OnOpenFile(self,e):
        wildcardImg="Image(*.jpg)|*.jpg|Image(*.jpeg)|*.jpeg|Image(*.png)|*.png|All files(*.*)|*.*"
        dialog = wx.FileDialog(None,message= '选择图片', defaultDir=os.getcwd(), defaultFile='', wildcard=wildcardImg)
        if dialog.ShowModal() == wx.ID_OK:
            self.fileNamePath.clear()
            fullpath=dialog.GetPath()
            filename=URL.getFileNameByUrl(fullpath)
            # 文件绝对路径作key,文件名加后缀作value加入字典
            self.fileNamePath[filename]=fullpath
            #选择文件后，清空文件展示列表，将新添加的展示到列表
            self.setNameListBox()
            self.setShowImageOnListBoxChange(self.nameListBox)
            self.setFileInfoText(self.nameListBox, self.fileInfo)
            dialog.Destroy()



    def OnOpenFiles(self,e):
        # 这个过滤的格式是 描述 | 类型
        wildcardImg="Image(*.jpg)|*.jpg|Image(*.jpeg)|*.jpeg|Image(*.png)|*.png|All files(*.*)|*.*"
        """
        FileDialog(parent, message=FileSelectorPromptStr, defaultDir=EmptyString, defaultFile=EmptyString,
                   wildcard=FileSelectorDefaultWildcardStr, style=FD_DEFAULT_STYLE, pos=DefaultPosition,
                   size=DefaultSize, name=FileDialogNameStr)
                   wx.FD_MULTIPLE：允许选择多个文件
        """
        dialog = wx.FileDialog(None,message= '选择图片', defaultDir=os.getcwd(), defaultFile='', wildcard=wildcardImg, style=wx.FD_OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.fileNamePath.clear()
            absolute_paths = dialog.GetPaths()
            for path in absolute_paths:
                self.fileNamePath[URL.getFileNameByUrl(path)] = path  # 文件名作key,文件路径作value加入字典

            # 选择文件后，清空文件展示列表，将新添加的展示到列表
            self.setNameListBox()
            self.setShowImageOnListBoxChange(self.nameListBox)
            self.setFileInfoText(self.nameListBox, self.fileInfo)
            dialog.Destroy()


    def OnExitClick(self,event):
        dlg = wx.MessageDialog(None, u"确定退出吗？想好了？", u"询问", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()
        dlg.Destroy()

    def OnHelpChlick(self,event):
        dlg = wx.MessageDialog(None, u"没有帮助！问人！", u"询问", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            pass
        dlg.Destroy()
    #menuBar,parentMenu,itemId,itemName,itemBgUrl,EVENT_MENU,fun
    def createAndBindMenuItem(self,menuBar,parentMenu,itemId,itemName,itemBgUrl,EVENT_MENU,fun):
        menuItem=wx.MenuItem(parentMenu,itemId,itemName)
        #设置背景
        #menuItem.SetBitmap(wx.Bitmap(itemBgUrl))
        parentMenu.Append(menuItem)
        self.Bind(EVENT_MENU,fun,id=itemId)

    # menuBar,parentMenu,itemId,itemName,itemBgUrl,EVENT_MENU,fun
    def createAndBindSkinMenuItem(self, menuBar, parentMenu, itemId, itemName, itemBgUrl, EVENT_MENU, fun):
        menuItem = wx.MenuItem(parentMenu, itemId, itemName,kind = wx.ITEM_RADIO)
        # 设置背景
        # menuItem.SetBitmap(wx.Bitmap(itemBgUrl))
        parentMenu.Append(menuItem)
        self.Bind(EVENT_MENU, fun,id=itemId)


    #设置皮肤 skinList-皮肤颜色列表  n-第几个皮肤
    def setSkin(self,skinList,n):
        self.panelTop.SetBackgroundColour(self.skinList[n][0])
        self.panelLeft.SetBackgroundColour(self.skinList[n][1])
        self.panelRight1.SetBackgroundColour(self.skinList[n][2])   #Right1的title  设置RightPanel的背景，然后用ListBox的颜色来覆盖
        self.nameListBox.SetBackgroundColour(self.skinList[n][3])
        self.panelRight2.SetBackgroundColour(self.skinList[n][4])   #Right2的title
        self.fileInfo.SetBackgroundColour(self.skinList[n][5])
        self.panelBottom.SetBackgroundColour(self.skinList[n][6])    #bottom的title
        self.ocrresult.SetBackgroundColour(self.skinList[n][7])
        self.panelTop.Refresh()
        self.panelLeft.Refresh()
        self.panelRight1.Refresh()
        self.nameListBox.Refresh()
        self.panelRight2.Refresh()
        self.fileInfo.Refresh()
        self.panelBottom.Refresh()
        self.ocrresult.Refresh()

    def OnChangeSkin(self,event):
        id=event.GetId()
        if   id==CST.MENU_SKIN_ITME_ONE:
            self.setSkin(self.skinList,0)
        elif id==CST.MENU_SKIN_ITME_TWO:
            self.setSkin(self.skinList, 1)
        elif id==CST.MENU_SKIN_ITME_THREE:
            self.setSkin(self.skinList, 2)
        elif id==CST.MENU_SKIN_ITME_FOUR:
            self.setSkin(self.skinList, 3)
        elif id==CST.MENU_SKIN_ITME_FIVE:
            self.setSkin(self.skinList, 4)
        elif id==CST.MENU_SKIN_ITME_SIX:
            self.setSkin(self.skinList, 5)
        elif id==CST.MENU_SKIN_ITME_SEVEN:
            self.setSkin(self.skinList, 6)

    def OnExportExcel(self,event):
        url=URL.getRootPath()+"data/excel_res.xlsx"
        if len(self.finishedResList)>0:
            excel.save_xls_file(url,self.finishedResList)
            dlg = wx.MessageDialog(None, u"保存成功", u"结果", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            dlg.Destroy()
        else:
            dlg1 = wx.MessageDialog(None, u"请先识别", u"警告", wx.YES_NO | wx.ICON_QUESTION)
            if dlg1.ShowModal() == wx.ID_YES:
                pass
            dlg1.Destroy()



    def OnTrainClick(self,event):
        dlg = wx.MessageDialog(None, u"即将开多线程训练?", u"询问", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            # parent = None, id = None, range = 100, pos = None, size = None, style = None, validator = None, name = None
            self.gauge1 = wx.Gauge(self.panelLeft, -1, range=100, pos=(0,350), size=(900, 10))
            self.gauge1.SetValue(self.train_processing_value)
            # 将wx空闲的事件绑定到进度条上
            self.Bind(wx.EVT_IDLE, self.train_processing_bar)
            t1 = threading.Thread(target=self.threadTrain, args=(event,))
            t1.start()
        dlg.Destroy()


    def threadTrain(self, arg):
        model = S.create_mlp(solver='sgd', activation='relu', alpha=1e-4, hidden_layer_sizes=(56, 56), random_state=1,
                             max_iter=10, verbose=10, learning_rate_init=.1)
        x_training_data, y_training_data, x_test_data, y_test_data = S.decompreData("")
        model = S.train(x_training_data, y_training_data, model)
        self.train_processing_value=100
        joblib.dump(model, "skmpl.m")  # 保存模型


    #处理图片
    def OnProceeClick(self,event):
        if (len(self.fileNamePath) > 0):
            self.gaugeImgPro = wx.Gauge(self.panelLeft, -1, range=100, pos=(0, 350), size=(900, 10))
            self.gaugeImgPro.SetValue(self.img_proccessing_value)
            # 将wx空闲的事件绑定到进度条上
            self.Bind(wx.EVT_IDLE, self.img_processing_bar)
            t2 = threading.Thread(target=self.threadProcessImg, args=(event,))
            t2.start()
        else:
            dlg = wx.MessageDialog(None, u"请选择图片!", u"警告", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
               pass
            dlg.Destroy()

    def threadProcessImg(self, arg):
        if(len(self.fileNamePath)>0):
            for name in self.fileNamePath:
                url=self.fileNamePath.get(name)
                img = cv2.imread(url, cv2.IMREAD_UNCHANGED)
                img, imgbinary, rectList = ImgProcess.imgProcess(img)
                self.srcImgDstImgArea.append([img,imgbinary,rectList,name,url])  #将处理好的信息放进一个数组
            self.img_proccessing_value=100


    def train_processing_bar(self, event):
        if self.train_processing_value < 99 and self.train_processing_value!=0:
            self.train_processing_value += 1
            time.sleep(0.3)
            self.gauge1.SetValue(self.train_processing_value)
        if self.train_processing_value==100:
            self.train_processing_value=0
            self.gauge1.SetValue(self.train_processing_value)
            dlg = wx.MessageDialog(None, u"训练完成！", u"训练", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            self.gauge1.Destroy()
            dlg.Destroy()


    def img_processing_bar(self, event):
        if self.img_proccessing_value < 99 and self.img_proccessing_value!=0:
            self.img_proccessing_value += 1
            time.sleep(0.3)
            self.gaugeImgPro.SetValue(self.img_proccessing_value)
        if self.img_proccessing_value==100:
            self.img_proccessing_value=0
            self.gaugeImgPro.SetValue(self.img_proccessing_value)
            dlg = wx.MessageDialog(None, u"处理完成！", u"处理", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            self.gaugeImgPro.Destroy()
            dlg.Destroy()

    def OnOrcClick(self,event):
        if (len(self.srcImgDstImgArea) > 0):
            self.gaugeImgOcr = wx.Gauge(self.panelLeft, -1, range=100, pos=(0, 350), size=(900, 10))
            self.gaugeImgOcr.SetValue(self.img_ocr_value)
            # 将wx空闲的事件绑定到进度条上
            self.Bind(wx.EVT_IDLE, self.img_ocr_bar)
            t3 = threading.Thread(target=self.threadOcrImg, args=(event,))
            t3.start()
        else:
            dlg = wx.MessageDialog(None, u"无处理图片!", u"警告", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
               pass
            dlg.Destroy()


    def threadOcrImg(self, arg):
        # 加载模型
        model = joblib.load("skmpl.m")
        rootUrl=URL.getRootPath()

        for src_dst_rectlit in self.srcImgDstImgArea:
            srcimg = src_dst_rectlit[0]       #原图
            imgbinary = src_dst_rectlit[1] #处理后的图
            rectList = src_dst_rectlit[2]  #数字位置矩形List
            srcimgname=src_dst_rectlit[3]
            srcimgfullpath=src_dst_rectlit[4]
            resultImg, processimg, resultList = ImgProcess.imgSklearnPredicted(srcimg, imgbinary, rectList, model)
            urlres=rootUrl+"images/result/res_"+srcimgname #结果图
            urlpro=rootUrl+"images/result/pro_"+srcimgname #图片处理图
            cv2.imwrite(urlres,resultImg)
            cv2.imwrite(urlpro, processimg)
            # 原图，处理后的图，数字矩形区域，图片名，全路径，结果图路径，过程图路径，结果List
            self.finishedResList.append([srcimg,imgbinary,rectList,srcimgname,srcimgfullpath,urlres,urlpro,resultList])
        self.img_ocr_value = 100 #标记已经完成
        self.setResultText()


    def img_ocr_bar(self, event):
        if self.img_ocr_value < 99 and self.img_ocr_value!=0:
            self.img_ocr_value += 1
            time.sleep(0.3)
            self.gaugeImgOcr.SetValue(self.img_ocr_value)
        elif self.img_ocr_value == 100:
            self.img_ocr_value = 0
            self.gaugeImgOcr.SetValue(self.img_ocr_value)
            dlg = wx.MessageDialog(None, u"识别完成！", u"处理", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            self.gaugeImgOcr.Destroy()
            dlg.Destroy()
            self.showResultImg()





# app = wx.App()
# window = wx.Frame(None,title="数字识别", size=(1120, 560),style=wx.DEFAULT_FRAME_STYLE,name="frame")
# panel  = wx.Panel(window)
# label  = wx.StaticText(panel, label="Hello World", pos=(100, 100))
# window.Show(True)
# app.MainLoop()
