import sys
import xlrd
from PyQt5.QtWidgets import QApplication, QMainWindow
import pic
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import UIdesign
import read
import math
col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "影片评分", "影片评价人数", "影片概况", "影片内容")

def get_key(dict, value):
    return [k for (k, v) in dict.items() if value in v]

def rank_search(ui,bptree):
    input = ui.rank_line.text()
    if not input:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，你还没有输入搜索请求。\n')
        return
    try:
        num = int(input)
        KeyValue = bptree.search(num)
        if num > 250:
            UIdesign.Ui_MainWindow.clear(ui)
            UIdesign.Ui_MainWindow.printf(ui, '抱歉，仅提供Top250电影信息的搜索。\n')
            return
        if not KeyValue:
            UIdesign.Ui_MainWindow.clear(ui)
            UIdesign.Ui_MainWindow.printf(ui, '抱歉，没有符合要求的电影。\n')
        else:
            xls_path = KeyValue.value[0]
            pic_path = KeyValue.value[1]
            info = read.readData(xls_path)
            UIdesign.Ui_MainWindow.clear(ui)
            for i in range(len(info)):
                UIdesign.Ui_MainWindow.printf(ui, col[i] + ':' + info[i] + '\n')
            pixmap = QtGui.QPixmap(pic_path)
            UIdesign.Ui_MainWindow.show_picture(ui, pixmap)

    except:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，请输入整数。\n')
        return


def name_search(ui,bptree,dict):
    input = ui.name_line.text()
    if not input:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，你还没有输入搜索请求。\n')
        return
    list = get_key(dict, input)
    if not list:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，没有符合要求的电影。\n')
    else:
        num = int(list[0])
        xls_path = bptree.search(num).value[0]
        pic_path = bptree.search(num).value[1]
        info = read.readData(xls_path)
        UIdesign.Ui_MainWindow.clear(ui)
        for i in range(len(info)):
            UIdesign.Ui_MainWindow.printf(ui, col[i] + ':' + info[i] + '\n')
        pixmap = QtGui.QPixmap(pic_path)
        UIdesign.Ui_MainWindow.show_picture(ui, pixmap)

def score_search(ui,bptree,dict):
    input = ui.score_line.text()
    if not input:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，你还没有输入搜索请求。\n')
        return
    try:
        judge = float(input)
        list = []
        if judge > 10:
            UIdesign.Ui_MainWindow.clear(ui)
            UIdesign.Ui_MainWindow.printf(ui, '抱歉，请输入10以内(包括10)的评分。\n')
            return
        for i in range(1,251):
            if dict[str(i)][1] >= judge:
                list.append(str(i))
        if not list:
            UIdesign.Ui_MainWindow.clear(ui)
            UIdesign.Ui_MainWindow.printf(ui,'抱歉，没有符合要求的电影。\n')
        else:
            UIdesign.Ui_MainWindow.clear(ui)
            for j in range(len(list)):
                num = int(list[j])
                xls_path = bptree.search(num).value[0]
                info = read.readData(xls_path)
                for i in range(len(info)):
                    UIdesign.Ui_MainWindow.printf(ui, col[i] + ':' + info[i] + '\n')

    except:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，请输入电影评分。\n')
        return

def judge_person_search(ui, bptree, dict):
    input = ui.judge_person_line.text()
    if not input:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，你还没有输入搜索请求。\n')
        return
    try:
        number = int(input)
        list = []
        for i in range(1,251):
            if dict[str(i)][2] >= number:
                list.append(str(i))
        if not list:
            UIdesign.Ui_MainWindow.clear(ui)
            UIdesign.Ui_MainWindow.printf(ui,'抱歉，没有符合要求的电影。\n')
        else:
            UIdesign.Ui_MainWindow.clear(ui)
            for j in range(len(list)):
                num = int(list[j])
                xls_path = bptree.search(num).value[0]
                info = read.readData(xls_path)
                for i in range(len(info)):
                    UIdesign.Ui_MainWindow.printf(ui, col[i] + ':' + info[i] + '\n')

    except:
        UIdesign.Ui_MainWindow.clear(ui)
        UIdesign.Ui_MainWindow.printf(ui, '抱歉，请输入整数。\n')
        return

def showUI(bptree,dict):
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UIdesign.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.rank_search_button.clicked.connect(partial(rank_search,ui,bptree))
    ui.name_search_button.clicked.connect(partial(name_search,ui,bptree,dict))
    ui.score_search_button.clicked.connect(partial(score_search,ui,bptree,dict))
    ui.judge_person_search_button.clicked.connect(partial(judge_person_search, ui, bptree, dict))
    sys.exit(app.exec_())

