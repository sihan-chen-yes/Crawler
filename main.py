from spider import generate
from BPlus import Bptree,KeyValue
import os
import UI
import xlrd

py_path = os.getcwd()
table_path = py_path + '\\table\\豆瓣电影Top'
picture_path = py_path + '\\picture\\豆瓣电影Top'

#movie_dict = generate()
#爬虫 产生本地 .xls文件库与.jpg文件库 得到字典 rank ,中文名

movie_dict = {}
for i in range(250):
    num = i + 1
    book = xlrd.open_workbook(table_path + str(num) + '.xls')
    sheet = book.sheets()[0]
    info = sheet.row_values(1)
    movie_dict[str(num)] = []
    movie_dict[str(num)].append(info[2])
    movie_dict[str(num)].append(float(info[4]))
    movie_dict[str(num)].append(int(info[5]))

#generate bptree
kv_list = []
for i in range(0, 250):
        key = i + 1
        value = ((table_path+str(key)+'.xls'),(picture_path+str(key)+'.jpg'))
        kv_list.append(KeyValue(key, value))
content_bptree = Bptree(20, 20)
for kv in kv_list:
    content_bptree.insert(kv)

#启动UI界面
UI.showUI(bptree=content_bptree,dict=movie_dict)
