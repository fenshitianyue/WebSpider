#!/usr/bin/python
#coding:utf-8

#这是一个没有破解反爬虫机制的爬虫项目

#使用Python 标准库获取指定 url 的响应
#根据url获取网页内容

import re
import urllib2
from bs4 import BeautifulSoup

def OpenPage(url):
    Myheaders = {}

    request = urllib2.Request(url, headers=Myheaders)

    f = urllib2.urlopen(request)

    data = f.read()
    #python 内置的编码解码方法：decode解码  encode 编码
    #decode的第二个参数是解码失败后的处理方式，三个选项分别为：忽略，替换为？，
    #ignore / replace / xml***
    return data.decode("GBK", errors = "ignore").encode("utf-8")


#从小说主页获取各个章节的URL
def ParseMainPage(page):
    # BeautifulSoup方法，解析服务器端响应内容并格式化
    soup = BeautifulSoup(page, "html.parser")
    #soup.find_all():查找全部符合的内容
    #构造正则表达式的对象：Pattern对象
    ListCharts = soup.find_all(href=re.compile("read"))

    #采用循环的方式生成列表，保存解析出来的url
    #UrlList = []
    #for item in ListCharts:
    #    url = "http://www.shengxu"+item["href"]
    #    UrlList.append(url)

    #采用列表生成式的方法生成列表,保存解析出来的url
    UrlList = ["http://www.shengxu6.com" + item["href"] for item in ListCharts]

    return UrlList

#根据各个章节的url获取章节名和正文
def ParseDetailPage(page):
    soup = BeautifulSoup(page, "html.parser")
    #get_text()方法：取标签类包含的内容
    title = soup.find_all(class_ = "panel-heading")[0].get_text() #获取章节
    content = soup.find_all(class_="content-body")[0].get_text() #获取正文
    return title,content[:-12] #同时返回标题和正文，切片操作除去正文末尾的JS代码

#把数据写入输出文件
def WriteDataToFile(data):
    #f = open("output.txt", "a+")
    #f.close()
    #上下文管理器(防止忘记关闭文件描述符)
    with open("output.txt", "a+") as f:
        f.write(data)


if __name__ == "__main__":
    #打开小说主页
    Get = raw_input("输入要爬取的小说网址：")
    MainPage = OpenPage(Get)
    #解析主页，获得各个章节url
    GetUrl = ParseMainPage(MainPage)
    for item in GetUrl:
        #打开章节页面
        print "Clone " + item
        #打开每一章节的页面
        page = OpenPage(item)
        #获取章节标题和正文
        title,content = ParseDetailPage(page)
        print "Clone title is " + title
        data = "\n\n\n" + title + "\n\n\n" + content
        #此处因为编码问题:提取到的网站数据编码格式是utf-8，但是变量data
        #是ascii类型，所以需要先转码然后再写入文件
        WriteDataToFile(data.encode("utf-8"))



