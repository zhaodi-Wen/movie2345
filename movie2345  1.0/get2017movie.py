#!/usr/bin/evn python
#-*-coding: utf-8 -*-
'''
Created on 2017年8月20日

@author: WZD06
'''
from bs4 import BeautifulSoup
import sys
import urllib2
from mylog import MyLog as mylog
import codecs 
import sys
from saveExcel import save2017Movie

reload(sys)
sys.setdefaultencoding("utf-8")

class MovieItem(object):
    """docstring for MovieItem"""
    name = None
    point = None
    staring = None


class GetMovie(object):
    """docstring for GetMovie"""
    def __init__(self):
        self.urlBase = 'http://dianying.2345.com/list/----2017--.html'
        self.log = mylog()
        self.pages = self.getPages()
        self.urls = []
        self.items = []
        self.getUrls(self.pages)
        self.items = self.spider(self.urls)
        self.log.info(u'开始下载数据')
        self.piplines(self.items)
        self.log.info(u'数据下载成功')
        self.log.info(u'数据开始保存在表格')
        save2017Movie(self.items)
        self.log.info(u'数据已经保存完毕')

    

    def getPages(self):
        self.log.info(u'开始获取页数')
        htmlConten = self.getResponseContent(self.urlBase)
        soup = BeautifulSoup(htmlConten,'html.parser')
        tag = soup.find('div',attrs={'class':"v_page"})
        subtags = tag.find_all('a')
        pages = subtags[-2].get_text()
        self.log.info(u'获取页数成功')

        return int(pages)

    def getResponseContent(self,url):
        try:
            response = urllib2.urlopen(url)
        except :
            self.log.error(u'python返回URL :%s失败'%url)
        else:
            self.log.info(u'python 返回 URL ：%s成功'%url)
            return response.read()

    def getUrls(self,pages):
        for page in xrange(1,pages+1):
            url = 'http://dianying.2345.com/list/----2017---'+str(page)+'.html'
            self.urls.append(url)
            self.log.info(u'添加URL:%s到URLS成功'% url)
        return self.urls

    def spider(self,urls):
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent,'lxml')
            anchorTag = soup.find('ul',attrs={'class':"v_picTxt pic180_240 clearfix"})
            tags = anchorTag.find_all('li')
            for tag in tags:
                item = MovieItem()
                try:
                    item.name = tag.find('span',attrs={'class':"sTit"}).get_text()
                    item.point = tag.find('span',attrs={'class':"pRightBottom"}).get_text().replace(u'分','')
                    item.staring = tag.find('span',attrs={'class':"sDes"}).get_text().replace(u'主演：','')
                except :
                    pass
                self.items.append(item)
                self.log.info(u'获取电影名为<<%s>>成功'%item.name)
        return self.items

    def piplines(self,items):
        filename = u'2017热门电影.txt'.encode('GBK')
        with open(filename,'w') as fp:
            fp.write('电影名称     电影评分     电影主演  \r')
            for item in items:
                fp.write('%s             %s           %s    \r\n'%(item.name,item.point,item.staring))
                self.log.info(u'获取电影名字为%s的数据保存成功'%item.name)

if __name__ == '__main__':
    GM = GetMovie()
    


        
        
        
