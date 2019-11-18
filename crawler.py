# coding: utf-8
from zwduCrawler import crawelHome as zwCrawelHome, getArticleList as zwGetArticleList, crawelArticle as zwCrawelArticle
from sfCrawler import crawelHome as sfCrawelHome, getArticleList as sfGetArticleList, crawelArticle as sfCrawelArticle
from hjCrawler import crawelHome as hjCrawelHome, getArticleList as hjGetArticleList, crawelArticle as hjCrawelArticle
from wenkuCrawler import crawelHome as wenCrawelHome, getArticleList as wenGetArticleList, crawelArticle as wenCrawelArticle
from hetuCrawler import crawelHome as hetuCrawelHome, getArticleList as hetuGetArticleList, crawelArticle as hetuCrawelArticle

class Crawler:
    def __init__(self):
        self.support = ['sf', 'zwdu', 'hj', 'wenku', 'hetu']
        self.site = ''

    def crawelHome(self, homeLink):
        if 'book.sfacg.com' in homeLink:
            self.site = 'sf'
            return sfCrawelHome(homeLink)
        elif 'zwdu.com' in homeLink:
            self.site = 'zwdu'
            return zwCrawelHome(homeLink)
        elif 'hjwzw.com' in homeLink:
            self.site = 'hj'
            return hjCrawelHome(homeLink)
        elif 'wenku8.net' in homeLink:
            self.site = 'wenku'
            return wenCrawelHome(homeLink)
        elif 'hetushu.com' in homeLink:
            self.site = 'hetu'
            return hetuCrawelHome(homeLink)
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
