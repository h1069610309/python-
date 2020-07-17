# encoding:utf-8
# !/usr/bin/env python
# @author:wei
# @file: spider.py
# @time: 2020/07/16
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式
import urllib.request, urllib.error  # 制定url，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行Sqlite 数据库操作

findLink = re.compile(r'<a href="(.*)">')  # 创建正则表达式，表示规则 获取电影链接
findImg = re.compile(r'<img.*src="(.*?)"', re.S)  # 影片图片地址
findTitle = re.compile(r'<span class="title">(.*)</span>')  # 电影名
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 评价人数
findInq = re.compile(r'<span class="inq">(.*)。</span>')  # 找到概况
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 电影描述


# url="https://movie.douban.com/top250?start="
def getData(baseurl):
    # 1爬取网页
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askUrl(url)  # 保存获取的网页
        # 2逐一解析
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.findAll('div', class_="item"):
            # print(item) #测试获取item
            data = []  # 保存一部电影item全部信息
            item = str(item)
            link_item_ = re.findall(findLink, item)[0]
            data.append(link_item_)
            img_item_ = re.findall(findImg, item)[0]
            data.append(img_item_)
            title_item_ = re.findall(findTitle, item)
            if len(title_item_) == 2:
                data.append(title_item_[0])
                data.append(title_item_[1].replace("/", ""))
            else:
                data.append(title_item_[0])
                data.append("")
            rating_item_ = re.findall(findRating, item)[0]
            data.append(rating_item_)
            judge_item_ = re.findall(findJudge, item)
            data.append(judge_item_)
            inq_item_ = re.findall(findInq, item)
            if len(inq_item_) != 0:
                inq_item_ = inq_item_[0].replace("。", "")  # 去掉中文句号
                data.append(inq_item_)
            else:
                data.append("")  # 留空
            bd_item_ = re.findall(findBd, item)[0]
            bd_item_ = re.sub('<br(\s)?/>', " ", bd_item_)  # 去掉br
            bd_item_ = re.sub('/', " ", bd_item_)  # 去掉/
            data.append(bd_item_)
            datalist.append(data)  # 把处理好的一部电影放入datalist
    return datalist


# 访问网页
def askUrl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

    }
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req)
    # print(response.read().decode("utf-8"))
    return html
def saveData(datalist,saveUrl):
    print("save...")
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)#创建Workbook对象
    sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)#创建工作表
    col=("电影链接","图片链接","影片中文名","影片英文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])#列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j]) #保存每行每列的数据
    book.save(saveUrl)

def main():
    url = "https://movie.douban.com/top250?start="
    datalist = getData(url)
    # print(data)
    saveUrl = "豆瓣电影Top250.xls"
    #保存数据
    saveData(datalist,saveUrl)


if __name__ == '__main__':
    main()
    print("爬取完毕...")
