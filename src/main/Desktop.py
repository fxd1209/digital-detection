"""
用法写这:不在乎格式
wx.Frame --不带参数的默认构造函数，是窗体
wx.Panel --放入wxFrame对象中的Component,继承至wxWindow
wx.StaticText --该类提供了控制持有，比如只读文本，它不会产生任何事件
TextCtl --他控制在wx其中可以显示文本和编辑
RadioButton & RadioBox --每个按钮，wx.RadioButton类的一个对象携带旁边有一个圆形按钮文本
标签。wx.RadioBox 提供一个边框和标签组
wx.CheckBox --一个复选框
ComboBox $ Choice Class --wx.ComboBox对象提供选择的项目列表，可以配置一个下来
拉列表或永久性的显示。wx.Choice类，其目的也是一个下拉列表中，这是永久只读

wx.Gauge --该类对象表示垂直或水平条，其中以图形方式显示递增量。
wx.Slider --提供了滚动条相同的功能。滑动器提供了一个方便的方式来处理由滑块具体wx.EVT_SLIDER
时间绑定拖动句柄
wx.MenuBar --略低于顶层窗口的标题栏中的横条保留，以显示一系列菜单。
wx.Toolbar --如果wx.Toobal 对象的样式参数设置为 wx.TB_DOCKABLE,它成为可停靠。浮动工具栏还可以用wxPython中的AUIToolBar类构造器
wx.Dialog --对话框类对象，通常作为父框架顶部上的弹出窗口。
wx.SplitterWindow --布局管理器，它拥有两个子窗口，大小可以通过拖动他们之间的边界动态变化。分离控制器给出了可拖动来调整控制件的句柄
HTMLWindow --wxHTML库中包含用于解析和显示HTML。wxHtmlWindow是一个通用的HTML浏览器
ListBox $ ListCtrl --一个wx.ListBox控件呈现字符串垂直滚动列表。默认情况下，在列表中的单个产品选择。ListCtrl
空间是一个高度增强列表显示和选择工具。多个列表可以显示在报表视图，列表视图和图标视图。


listBox学习链接：https://www.xuebuyuan.com/3265192.html



wxPython事件:
函数或方法响应于点击按钮，调用事件选择相应的处理函数，用户的操作被执行。应用程序的运行时期间发生的某个事件数据被存储为来自wx.Event衍生的子类的对象。
例如，要调用一个按钮的点击事件的程序上的 OnClick()方法
self.b1.Bind(EVT_BUTTON, OnClick)

bind()方法是通过从wx.EvtHandler类的所有显示对象继承。EVT_BUTTON这里是绑定器，其中关联按钮单击事件的 OnClick()方法。
在wxPython中事件是两种类型的。基本事件和命令事件。大多数 wxWidgets生成命令事件。

基本事件
一个基本的事件停留在它起源的窗口。比如移动窗口的 OnMove 事件
self.Bind(wx.EVT_MOVE, self.OnMove)

命令事件。
命令事件可以传播到一个或多个窗口，类层次结构来源于窗口上方。比如点击按钮的 OnButtonClicked)事件
self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)




wxPython布局
wxPython的布局又包含绝对布局和相对布局两种方式。绝对布局需要定义每一个控件的位置坐标，方法单一繁琐，很难实际应用。所以，主要的布局方式都是采用相对布局。wxPython提供了一系列的布局管理器，被称为Sizer，它们都继承至wx.sizer基类。
BoxSizer
sizer允许控件排放在按行或列的方式。BoxSizer布局是由它的定位参数(wxVERTICAL或wxHORIZONTAL)确定。

GridSizer
顾名思义，一个GridSizer对象呈现二维网格。控件被添加在网格槽以左到右和由上到下方顺序。

FlexiGridSizer
这种sizer 也有一个二维网格。它提供灵活性布局中的控制单元。

GridBagSizer
GridBagSizer是一种多功能sizer。它比FlexiGridSizer提供了更多的增强功能。子构件可被添加到网格中的指定单元格。

StaticBoxSizer
StaticBoxSizer把一个盒子sizer放到静态框。它提供了围绕框边界以及顶部标签。

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



class MainWin(wx.Frame):
    def __init__(self,*args,**kw):
        super(MainWin,self).__init__(style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX,*args,**kw)

        self.fileNamePath={}     #名字-路径键值对  同一路径下不可能有重复名字，故以名字作为key
        #top，left, right1Title, right1, right2Title, right2, bottomTitle, bottom
        self.skinList=[
                       [(255,63,30),(245,247,251),(255,63,30),(240,255,255),(255,63,30),(240,255,255),(255,63,30),(255,63,30)],   # skin1
                       [(196,147,239),(245,247,251),(196,147,239),(245,246,248),(196,147,239),(245,246,248),(196,147,239),(196,147,239)],   # skin2
                       [(234,187,19),(245,247,251),(234,187,19),(245,246,248),(234,187,19),(245,246,248),(234,187,19),(234,187,19)],   # skin3
                       [(244,206,205),(245,247,251),(244,206,205),(245,246,248),(244,206,205),(245,246,248),(244,206,205),(244,206,205)]    # skin4
                       ]


        # 创建菜单栏(MenuBar),在菜单栏里面添加菜单(Menu),在菜单里面加菜单项（menuItem）
        self.menuBar = wx.MenuBar()  # 菜单栏
        self.menu_file = wx.Menu()  # 菜单栏中一文件菜单
        self.menu_skin = wx.Menu()  # 菜单栏中一换肤菜单
        self.initMenuBar()

        self.sizer = wx.GridBagSizer(0, 0)  # 列间隔，行间隔都为0

        """
        #panel top Start
        """
        self.panelTop = wx.Panel(self)
        self.panelTop.SetMinSize((1120, 30))
        self.panelTop.SetBackgroundColour((230,230,250))

        # 在Panel上添加Button
        self.btnReadFile = wx.Button(self.panelTop, id=CST.BTN_READ_FILE, label=u'读取', pos=(400, 0), size=(70, 30))
        self.btnReadFile.SetDefault()
        self.btnReadFile.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/import.gif")))
        self.btnReadFile.Bind(wx.EVT_LEFT_DOWN,self.OnOpenFiles)

        # 在Panel上添加Button
        self.btnOcr = wx.Button(self.panelTop, id=CST.BTN_OCR_IMG,label=u"识别", pos=(470, 0), size=(70, 30))
        self.btnOcr.SetDefault()
        self.btnOcr.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/identify.gif")))
        self.btnOcr.Bind(wx.EVT_LEFT_DOWN, self.OnOpenFile)


        # 在Panel上添加Button
        self.btnExport = wx.Button(self.panelTop, id=CST.BTN_EXPORT_EXCEL, label=u'导出Excel', pos=(540, 0), size=(70, 30))
        self.btnExport.SetDefault()
        self.btnExport.SetBitmap(bitmap=wx.Bitmap(URL.getResPath("images/logo/excel.gif")))
        self.btnExport.Bind(wx.EVT_LEFT_DOWN, self.OnOpenFile)


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
        #self.ocrresult(self.nameListBox, self.fileInfo)

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

        self.PanelW, self.PanelH = self.panelLeft.GetSize()  # 展示图片区域的宽高，以留着展示图片用
        self.ImgW, self.ImgH = (0,0)
        self.ImgX,self.ImgY=0,0
        self.ImgBit=""
        self.setShowImage(self.panelLeft,URL.getResPath("images/logo/ocr_bg.jpg"))


    def initMenuBar(self):
        # 文件菜单的菜单项
        # menuBar,parentMenu,itemId,itemName,itemBgUrl,EVENT_MENU,fun
        self.createAndBindMenuItem(self.menuBar, self.menu_file, CST.MENU_FILE_ITME_OPEN, "open image", "", wx.EVT_MENU,
                                   self.OnOpenFile)
        self.createAndBindMenuItem(self.menuBar, self.menu_file, CST.MENU_FILE_ITME_OPENS, "open images", "",
                                   wx.EVT_MENU,
                                   self.OnOpenFiles)
        # 换肤菜单的菜单项
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_ONE, "性感红", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_TWO, "基佬紫", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_THREE, "金色稻田", "", wx.EVT_MENU,
                                       self.OnChangeSkin)
        self.createAndBindSkinMenuItem(self.menuBar, self.menu_skin, CST.MENU_SKIN_ITME_FOUR, "粉红女郎", "", wx.EVT_MENU,
                                       self.OnChangeSkin)

        self.menuBar.Append(self.menu_file, '&文件')
        self.menuBar.Append(self.menu_skin, '&换肤')

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





def main():
    ex = wx.App()
    mainWin=MainWin(None)
    mainWin.Show(True)
    ex.MainLoop()
if __name__ == '__main__':
    main()
# app = wx.App()
# window = wx.Frame(None,title="数字识别", size=(1120, 560),style=wx.DEFAULT_FRAME_STYLE,name="frame")
# panel  = wx.Panel(window)
# label  = wx.StaticText(panel, label="Hello World", pos=(100, 100))
# window.Show(True)
# app.MainLoop()
