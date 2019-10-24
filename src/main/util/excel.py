from collections import OrderedDict

from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data


def read_xls_file():
    xls_data = get_data(r"write_test.xlsx")
    print("Get data type:", type(xls_data))
    for sheet_n in xls_data.keys():
        print(sheet_n, ":", xls_data[sheet_n])


# 写excel数据，xls格式
def save_xls_file(url,list):
    #list = []： 原图，处理后的图，数字矩形区域，图片名，全路径，结果图路径，过程图路径，结果List
    OD = OrderedDict()
    # sheet表的数据
    sheet_1 = []
    row_1_data = [u"图片名称", u"图片路径", u"结果集"]  # 每一行的数据
    sheet_1.append(row_1_data)
    for data in list:
        imgnmae=data[3]
        imgpath=data[4]
        imgres=data[7]
        new_num_list=[str(x) for x in imgres]
        row_2_data = [imgnmae,imgpath, ",".join(new_num_list)]
        sheet_1.append(row_2_data)
    # 添加sheet表
    OD.update({u"这是结果表": sheet_1})
    # 保存成xls文件
    save_data(url, OD)

# if __name__ == '__main__':
#     # read_xls_file()
#     save_xls_file("url",[])