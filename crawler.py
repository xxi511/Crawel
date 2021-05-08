# coding: utf-8
import requests.packages.urllib3
from zwduCrawler import crawelHome as zwCrawelHome, getArticleList as zwGetArticleList, crawelArticle as zwCrawelArticle
from sfCrawler import crawelHome as sfCrawelHome, getArticleList as sfGetArticleList, crawelArticle as sfCrawelArticle
from hjCrawler import crawelHome as hjCrawelHome, getArticleList as hjGetArticleList, crawelArticle as hjCrawelArticle
from wenkuCrawler import crawelHome as wenCrawelHome, getArticleList as wenGetArticleList, crawelArticle as wenCrawelArticle
from hetuCrawler import crawelHome as hetuCrawelHome, getArticleList as hetuGetArticleList, crawelArticle as hetuCrawelArticle
from zssqCrawler import crawelHome as zssqCrawelHome, getArticleList as zssqGetArticleList, crawelArticle as zssqCrawelArticle
from czbookCrawler import crawelHome as caCrawelHome, getArticleList as czGetArticleList, crawelArticle as czCrawelArticle
from quanbenCrawler import crawelHome as quanCrawelHome, getArticleList as quanGetArticleList, crawelArticle as quanCrawelArticle
from dingdianCrawler import crawelHome as dingCrawelHome, getArticleList as dingGetArticleList, crawelArticle as dingCrawelArticle
from uuCrawler import  crawelHome as uuCrawelHome, getArticleList as uuGetArticleList, crawelArticle as uuCrawelArticle
from wutuxsCrawler import  crawelHome as wutuxCrawelHome, getArticleList as wutuxGetArticleList, crawelArticle as wutuxCrawelArticle
from book8Crawler import  crawelHome as b8CrawelHome, getArticleList as b8GetArticleList, crawelArticle as b8CrawelArticle
from bimiduCrawler import crawelHome as bimCrawelHome, getArticleList as bimGetArticleList, crawelArticle as bimCrawelArticle

requests.packages.urllib3.disable_warnings()

class Crawler:
    def __init__(self):
        self.support = ['sf', 'zwdu', 'hj', 'wenku', 'hetu', 'zssq', 'czbook', 'quanben',
                        'dingdian', 'uu', 'wutuxs', '8book', 'bimidu']
        self.site = ''

    def crawelHome(self, homeLink):
        if 'book.sfacg.com' in homeLink:
            self.site = 'sf'
            return sfCrawelHome(homeLink)
        elif 'zwdu.com' in homeLink or '81book.com' in homeLink or '81zw.com' in homeLink:
            self.site = 'zwdu'
            return zwCrawelHome(homeLink)
        elif 'hjwzw.com' in homeLink:
            self.site = 'hj'
            return hjCrawelHome(homeLink)
        elif 'wenku8.net' in homeLink:
            self.site = 'wenku'
            return wenCrawelHome(homeLink)
        elif 'hetushu.com' in homeLink or 'hetubook.com' in homeLink:
            self.site = 'hetu'
            return hetuCrawelHome(homeLink)
        elif 'zssq.cc' in homeLink:
            self.site = 'zssq'
            return zssqCrawelHome(homeLink)
        elif 'czbooks.net' in homeLink:
            self.site = 'czbook'
            return caCrawelHome(homeLink)
        elif 'quanben.io' in homeLink:
            self.site = 'quanben'
            return quanCrawelHome(homeLink)
        elif 'dingdianorg.com' in homeLink:
            self.site = 'dingdian'
            return dingCrawelHome(homeLink)
        elif 'uukanshu' in homeLink:
            self.site = 'uu'
            return uuCrawelHome(homeLink)
        elif 'wutuxs.com' in homeLink:
            self.site = 'wutuxs'
            return wutuxCrawelHome(homeLink)
        elif '8book.com' in homeLink:
            self.site = '8book'
            return b8CrawelHome(homeLink)
        elif 'bimidu.com' in homeLink:
            self.site = 'bimidu'
            return  bimCrawelHome(homeLink)
        else:
            raise ValueError('Unsupport source website')

    def getArticleList(self, rootSoup, startChapterName):
        if self.site == 'sf':
            return sfGetArticleList(rootSoup, startChapterName)
        elif self.site == 'zwdu':
            return  zwGetArticleList(rootSoup, startChapterName)
        elif self.site == 'hj':
            return hjGetArticleList(rootSoup, startChapterName)
        elif self.site == 'wenku':
            return wenGetArticleList(rootSoup, startChapterName)
        elif self.site == 'hetu':
            return hetuGetArticleList(rootSoup, startChapterName)
        elif self.site == 'zssq':
            return zssqGetArticleList(rootSoup, startChapterName)
        elif self.site == 'czbook':
            return czGetArticleList(rootSoup, startChapterName)
        elif self.site == 'quanben':
            return quanGetArticleList(rootSoup, startChapterName)
        elif self.site == 'dingdian':
            return dingGetArticleList(rootSoup, startChapterName)
        elif self.site == 'uu':
            return uuGetArticleList(rootSoup, startChapterName)
        elif self.site == 'wutuxs':
            return wutuxGetArticleList(rootSoup, startChapterName)
        elif self.site == '8book':
            return b8GetArticleList(rootSoup, startChapterName)
        elif self.site == 'bimidu':
            return bimGetArticleList(rootSoup, startChapterName)

    def crawelArticle(self, href):
        if self.site == 'sf':
            return sfCrawelArticle(href)
        elif self.site == 'zwdu':
            return zwCrawelArticle(href)
        elif self.site == 'hj':
            return hjCrawelArticle(href)
        elif self.site == 'wenku':
            return wenCrawelArticle(href)
        elif self.site == 'hetu':
            return hetuCrawelArticle(href)
        elif self.site == 'zssq':
            return zssqCrawelArticle(href)
        elif self.site == 'czbook':
            return czCrawelArticle(href)
        elif self.site == 'quanben':
            return quanCrawelArticle(href)
        elif self.site == 'dingdian':
            return dingCrawelArticle(href)
        elif self.site == 'uu':
            return uuCrawelArticle(href)
        elif self.site == 'wutuxs':
            return wutuxCrawelArticle(href)
        elif self.site == '8book':
            return b8CrawelArticle(href)
        elif self.site == 'bimidu':
            return bimCrawelArticle(href)
