#!/usr/bin/python
#coding:utf-8

import re
import urllib2
import json
import base64
from bs4 import BeautifulSoup
import MySQLdb


def OpenPage(url):
    Myheaders = {}
    req = urllib2.Request(url,headers=Myheaders)
    f = urllib2.urlopen(req)
    data = f.read()
    return data

def Test1():
    print OpenPage("http://jy.51uns.com:8022/Pro_StudentEmploy/StudentJobFair/Zhaoping.aspx?WorkType=0")

def Test2():
    print OpenPage("http://jy.51uns.com:8022/Frame/Data/jdp.ashx?rnd=1528794488557&fn=GetZhaopinList&StartDate=2000-01-01&SearchKey=&InfoType=-1&CompanyAttr=&CompanyType=&Area=&City=&CompanyProvice=&Post=&Zhuanye=&XLkey=&Age=&start=0&limit=15&DateType=999&InfoState=1&WorkType=0&CompanyKey=")
#解析主页内容，获取招聘信息的url
def ParseMainPage(page):
    #json.dumps() 转化数据成json格式
    #json.loads() 转化json格式成python数据类型
    data = json.loads(page)
    #解析后的Data是一个大的字典,rows是招聘信息数据的key
    #rows里面保存了一个包含多个招聘信息的list
    #list里面的每个元素都是一条招聘信息，保存为字典类型
    rows = data["rows"]
    prefix = "http://jy.51uns.com:8022/Frame/Data/jdp.ashx?rnd=1533005391497&fn=GetOneZhaopin&StartDate=2000-01-01&JobId="
    IdList = []
    for item in rows:
        IdList.append(prefix + item['Id'])
    #return [prefix + item["Id"] for item in rows]
    return IdList

def Test3():
    page = OpenPage("http://jy.51uns.com:8022/Frame/Data/jdp.ashx?rnd=1533001139862&fn=GetZhaopinList&StartDate=2000-01-01&SearchKey=&InfoType=-1&CompanyAttr=&CompanyType=&Area=&City=&CompanyProvice=&Post=&Zhuanye=&XLkey=&Age=&start=0&limit=15&DateType=999&InfoState=1&WorkType=0&CompanyKey=")

    print ParseMainPage(page)

#解析招聘信息详情页
def ParseDetailPage(page):
    data = json.loads(page)
    if not data["Succeed"]:
        print "error"
        return
    data = data["Data"]
    detail = data["EmployContent"]
    soup = BeautifulSoup(detail,"html.parser")
    #查找全部的p标签
    GetP = soup.find_all("p")
    #get_text()
    content = [item.get_text() for item in GetP]
    content = "\n".join(content)

    return data["Id"],data["CompanyTitle"],data["WorkPositon"],content


def Test4():
    page = OpenPage("http://jy.51uns.com:8022/Frame/Data/jdp.ashx?rnd=1533005501840&fn=GetOneZhaopin&JobId=b360f9f177e34d94ba1363615aabda5f&StartDate=2000-01-01")
    jobid,title,position,content = ParseDetailPage(page)
    print jobid
    print title
    print position
    print content
#把数据写到文件里面
def WriteDataToFile(data):
    f = open("output.txt","a+")

    f.write(data.encode("utf-8"))
    f.close()

#TestPy database
#create table 'CrawlerSchool'(
#    'id' text,
#    'company' text,
#    'workposition' text,
#     "content" text,
#) ENGINE = InnoDB DEFAULT CHARSET = utf8

def WriteDataToMySQL(data):
    db = MySQLdb.connect(host="localhost",user="root",passwd="nihao.",db="test",charset="utf8")
    cursor = db.cursor()
    #base64 base64编码保障咱们能够把中文+特殊符号的内容存进数据库
    content = data[3]
    #进行base64编码,解决content里包含特殊符号的问题
    content = base64.b64encode(content)
    #构建sql语句
    sql = "insert into CrawlerSchool values('%s','%s','%s','%s')" % (data[0],data[1],data[2],data[3])
    print "sql=" + sql
    try:
        #执行sql语句
        cursor.execute(sql)
        db.commit()
    except Exception,e:
        #插入失败时，为了保证数据库操作的原子性，需要进行回滚
        db.rollback()
        print e
    #数据库链接关闭
    db.close()

def TestInsert():
    test_data = ('10086', '比特科技', '班主任', '颜值担当')
    WriteDataToMySQL(test_data)

#mysql -u root -p < table.sql
if __name__ == "__main__":
    #url = "http://jy.51uns.com:8022/Frame/Data/jdp.ashx?rnd=1533001139862&fn=GetZhaopinList&StartDate=2000-01-01&SearchKey=&InfoType=-1&CompanyAttr=&CompanyType=&Area=&City=&CompanyProvice=&Post=&Zhuanye=&XLkey=&Age=&start=0&limit=15&DateType=999&InfoState=1&WorkType=0&CompanyKey="
    ##根据主页ajax获取数据的url，获取服务器端相应的招聘信
    #mainPage = OpenPage(url)
    ##分析服务器端响应，得到招聘信息详情页的数据获取url
    #urlList = ParseMainPage(mainPage)
    #for item in urlList:
    #    print "crawler url=" + item
    #    #获取招聘信息详情
    #    detailPage = OpenPage(item)
    #    #解析数据
    #    data = ParseDetailPage(detailPage)
    #    #id,公司名,招聘岗位,招聘详情
    #    WriteDataToFile("\n".join(data))
    #print "crawler done"
    TestInsert()




