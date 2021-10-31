import urllib
import re
import xlwt
import os
from bs4 import BeautifulSoup
from urllib import request
from fake_useragent import UserAgent
import time
import random
from urllib.request import ProxyHandler
from urllib.request import build_opener
#IP来源于网络
proxies_list = [
    'https://144.255.49.40:9999',
    'https://60.13.42.15:9999',
    'https://163.204.246.105:9999'
]

def generate():
    baseUrl = 'https://movie.douban.com/top250?start='
    # 爬取目标url
    datalist = getData(baseUrl)
    # 保存数据
    saveData(datalist)


savepath = '豆瓣电影Top'
col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "影片评分", "影片评价人数", "影片概况", "影片内容")
# 创建影片超链接正则表达式
findLink = re.compile(r'<a href="(.*?)">')
# 创建图片正则表达式
findImgSrc = re.compile(r'<img .* src="(.*?)"', re.S)  # re.S的作用是让换行符包含在字符串中
# 创建影片名正则表达式
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 创建评分正则表达式
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 创建评价人数正则表达式
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 创建概况正则表达式
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 创建影片相关内容正则表达式
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseUrl):
    datalist = []
    for i in range(10):
        url = baseUrl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页
        # 逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')  # 也可以使用lxml代替html.parser作为解析器
        # 通过条件筛选我们需要的列表
        for item in soup.find_all('div', class_="item"):
            data = []  # 保存一部电影的所有信息
            item = str(item)  # 将列表转换为字符串

            # 获取影片超链接
            link = re.findall(findLink, item)[0]  # re库通过正则表达式来查找指定的字符串
            data.append(link)  # 添加超链接

            #  获取图片链接
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片链接

            # 获取文章标题
            titles = re.findall(findTitle, item)  # 片名可能只有中文名，没有外国名
            if len(titles) == 2:  # 如果有中文和外国名需要分别添加
                ctitle = titles[0]
                data.append(ctitle)  # 添加中文名
                otitle = titles[1].replace("/", " ")  # 去掉标题中的/字符
                data.append(otitle.split())  # 添加英文名,并将空格去掉
            else:
                data.append(titles[0])
                data.append(" ")  # 留空

            # 获取影片评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加影片评分

            # 获取评价人数
            judge = re.findall(findJudge, item)[0]
            data.append(judge)  # 添加评论人数

            # 获取概况
            inq = re.findall(findInq, item)
            data.append(inq)  # 添加概况

            # 获取影片内容
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\\s+)?/>(\\s+)', " ", bd)  # 使用空格替换掉<br', '>'
            bd = re.sub('/', " ", bd)  # 使用空格替换掉/
            data.append(bd.split())  # 去掉前后的空格（\xa0代表空白符&nbsp 使用strip()无法去掉）
            datalist.append(data)  # 将一页的电影信息添加进去

    return datalist


# 获取网页链接
def askURL(url):
    '''ua = UserAgent()
    head = {
        "User-Agent":ua.random
    }
    req = urllib.request.Request(url, headers=head)'''
    #更换IP
    use_ip = random.choice(proxies_list)
    proxy = {'http':use_ip}
    opener = build_opener(proxy)
    html = ""
    try:
        response = opener.open(url)
        html = response.read().decode('utf-8')  # read()获取响应体的内容，内容是bytes字节流，需要转换成字符串

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 保存数据
def saveData(datalist):
    #创建table picture 文件夹
    py_path = os.getcwd()
    table_path = py_path + '\\table'
    picture_path = py_path + '\\picture'
    os.mkdir(table_path)
    os.mkdir(picture_path)
    # 创建workBook对象
    dict = {}
    for i in range(250):
        book = xlwt.Workbook(encoding="utf-8")
        #top number
        num = i + 1
        # 创建工作表
        sheet = book.add_sheet(savepath + str(num), cell_overwrite_ok=True)  # cell_overwrite_ok=True, 可以覆盖原单元格中数据
        # 写入数据表头
        for j in range(0, 8):
            sheet.write(0, j, col[j])
        #写入数据内容
        data = datalist[i]
        for k in range(0, 8):
            sheet.write(1, k, data[k])
            #保存图片
            if(k == 1):
                ua = UserAgent()
                #对付图片防盗链
                head = {
                    "User-Agent": ua.random,
                    'Referer':'https://movie.douban.com/top250'
                }
                req = urllib.request.Request(data[1], headers=head)
                picture = request.urlopen(req).read()
                time.sleep(1)
                savingPic_path = picture_path + '\\' + savepath + str(num) + '.jpg'
                with open(savingPic_path,'wb') as f:
                    f.write(picture)
            if(k == 2):
                dict[str(num)] = data[2]
            #中文名检索

        # 保存表单
        book.save(table_path + '\\' + savepath+str(num)+'.xls')
        print("第%d条saved" % (i + 1))
    print("generate finished")
    return dict


