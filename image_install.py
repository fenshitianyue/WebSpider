#!/usr/bin/python
# coding:utf-8

import urllib2

# 定义一个全局列表用于保存url pool
url_list = []

def init_url_pool():
    f = open('main_url', 'r')
# 将本地文件中的url依次添加到url_list中并去掉每个url末尾的换行符
    for line in f.readlines():
        url_list.append(line.strip())
# 上面的两行代码也可以用列表推导语法(如下一行代码)
# url_list = [line.strip() for line in f.readlines()]
    f.close()

def test_url_pool():
    fp = open('test_url', 'w+')
    for line in url_list:
        fp.write(line + '\n')
    fp.close()

def test_update_for_url():
    # test code
    # print 'ready open url' + ' : ' + 'i.imgur.com/5HUw3J0.jpg?1'
    # res_1 = urllib2.urlopen('http://i.imgur.com/5HUw3J0.jpg?1')
    # print 'uropen ok'
    for i in len(url_list):
        print 'ready open url' + ' : ' + url_list[i]
        try:
            res = urllib2.urlopen(url_list[i])
        except BaseException:
            print 'Crawl failure'
            continue
        else:
            filename = 'image_' + i + '.jpg'
            f = open(filename, 'w+')
            f.write(res.read())
            f.close()

if __name__ == '__main__':
    init_url_pool()
    test_update_for_url()
