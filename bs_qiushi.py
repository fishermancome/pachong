#!/bin/env python
#!encoding:utf-8
import urllib2
from bs4 import BeautifulSoup

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories = []
        self.enable = False
   
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/text/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            html = response.read()
            return html
 
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "connected failed",e.reason
                return None
 

    def getPageItems(self,pageIndex):
        html = self.getPage(pageIndex)
        if not html:
            print "load failed"
            return None
        pageStories = []
        soup = BeautifulSoup(html,'lxml')
        for item in soup.find_all('div',class_="content"):
            pageStories.append(item.get_text())
        return pageStories
 

    def loadPage(self):

        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print story
    
    def start(self):
        print "reading qiushibaike enter Q to exit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)
 
 
spider = QSBK()
spider.start()
