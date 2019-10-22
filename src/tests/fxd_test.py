import wx
import time


class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "多模测试热补丁工具", size=(800, 600))
        panel = wx.Panel(self)
        list1 = ["BPN2", "BPL1", "BPC"]
        list2 = ["RRU1", "RRU2", "RRU3"]
        # ListBox类实例
        self.listbox1 = wx.ListBox(panel, -1, (50, 80), (200, 60), list1, wx.LB_SINGLE)  # wx.LB_SINGLE只能选择单个
        self.listbox2 = wx.ListBox(panel, -1, (50, 150), (200, 60), list2, wx.LB_MULTIPLE)  # 多选
        # CheckListBox类实例
        self.listbox3 = wx.CheckListBox(panel, -1, (300, 80), (200, 60), list1)
        # Choice类实例
        self.listbox4 = wx.Choice(panel, -1, (300, 200), (200, 40), list2)
        self.listbox4.Bind(wx.EVT_CHOICE, self.One_Play)
        # 进度条展示
        self.gauge1 = wx.Gauge(panel, -1, 100, (50, 250), (200, 60))
        self.value = 1
        self.gauge1.SetValue(self.value)
        # 将wx空闲的事件绑定到进度条上
        self.Bind(wx.EVT_IDLE, self.Gauge_Test)
        # 滑块
        self.slider = wx.Slider(panel, -1, 10, 10, 100, (300, 350), (200, 60))
        self.slider.Bind(wx.EVT_SCROLL, self.Slider_Test)

    def Gauge_Test(self, event):
        if self.value < 100:
            self.value += 1
            time.sleep(0.3)
            self.gauge1.SetValue(self.value)

    def Slider_Test(self, event):
        value = self.slider.GetValue()
        print
        "now value is:", value

    def One_Play(self, event):
        print
        "本次选择了吗：", self.listbox4.GetStringSelection()

    def Two_Play(self, event):
        print
        "本次选择了吗：", self.listbox2.GetSelections()


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


