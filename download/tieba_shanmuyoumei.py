#! /bin/env python
#! encoding:utf-8
import urllib
import urllib2
from bs4 import  BeautifulSoup
import os,sys

path = os.getcwd()
new_path = os.path.join(path,'shanmuyoumei')
if not os.path.isdir(new_path):
    os.mkdir(new_path)
def load_shanmu():
    url = 'http://tieba.baidu.com/p/2166231880'
    res = urllib2.Request(url)
    req = urllib2.urlopen(res)
    html = req.read()

    soup = BeautifulSoup(html,'lxml')

    shanmu = soup.find_all('img',class_='BDE_Image')

    for link in shanmu:
        item = link.get('src')
        content = urllib2.urlopen(item).read()

        with open('shanmuyoumei'+'/'+item[-9:],'wb') as code:
            code.write(content)


load_shanmu()
