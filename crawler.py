# coding: utf-8
from turtle import home
import requests.packages.urllib3
from Novel_Crawler.helpers import Support
from Novel_Crawler.book8Crawler import crawelHome as b8CrawelHome, getArticleList as b8GetArticleList, crawelArticle as b8CrawelArticle
from Novel_Crawler.b520 import crawelHome as b520CrawelHome, getArticleList as b520GetArticleList, crawelArticle as b520CrawelArticle
from Novel_Crawler.bimiduCrawler import crawelHome as bimCrawelHome, getArticleList as bimGetArticleList, crawelArticle as bimCrawelArticle
from Novel_Crawler.biquyueCrawler import crawelHome as biquCrawelHome, getArticleList as biquGetArticleList, crawelArticle as biquCrawelArticle
from Novel_Crawler.cnuuCrawler import crawelHome as cnuuCrawelHome, getArticleList as cnuuGetArticleList, crawelArticle as cnuuCrawelArticle
from Novel_Crawler.czbookCrawler import crawelHome as czCrawelHome, getArticleList as czGetArticleList, crawelArticle as czCrawelArticle
from Novel_Crawler.ddxsCrawler import crawelHome as ddCrawelHome, getArticleList as ddGetArticleList, crawelArticle as ddCrawelArticle
from Novel_Crawler.hetuCrawler import crawelHome as hetuCrawelHome, getArticleList as hetuGetArticleList, crawelArticle as hetuCrawelArticle
from Novel_Crawler.hjCrawler import crawelHome as hjCrawelHome, getArticleList as hjGetArticleList, crawelArticle as hjCrawelArticle
from Novel_Crawler.ptwxzCrawler import crawelHome as ptCrawelHome, getArticleList as ptGetArticleList, crawelArticle as ptCrawelArticle
from Novel_Crawler.quanbenCrawler import crawelHome as quanCrawelHome, getArticleList as quanGetArticleList, crawelArticle as quanCrawelArticle
from Novel_Crawler.sfCrawler import crawelHome as sfCrawelHome, getArticleList as sfGetArticleList, crawelArticle as sfCrawelArticle
from Novel_Crawler.sixnineshuCrawler import crawelHome as snCrawelHome, getArticleList as snGetArticleList, crawelArticle as snCrawelArticle
from Novel_Crawler.uuCrawler import  crawelHome as uuCrawelHome, getArticleList as uuGetArticleList, crawelArticle as uuCrawelArticle
from Novel_Crawler.wenkuCrawler import crawelHome as wenCrawelHome, getArticleList as wenGetArticleList, crawelArticle as wenCrawelArticle
from Novel_Crawler.wutuxsCrawler import  crawelHome as wutuxCrawelHome, getArticleList as wutuxGetArticleList, crawelArticle as wutuxCrawelArticle
from Novel_Crawler.zwduCrawler import crawelHome as zwCrawelHome, getArticleList as zwGetArticleList, crawelArticle as zwCrawelArticle

requests.packages.urllib3.disable_warnings()

class Crawler:
    def __init__(self):
        self.site = Support.unknown

    def crawelHome(self, homeLink):
        self.site = Support(homeLink)
        functions = {
            Support.b520: b520CrawelHome,
            Support.bimidu: bimCrawelHome,
            Support.biquyue: biquCrawelHome,
            Support.book8: b8CrawelHome,
            Support.cnuu: cnuuCrawelHome,
            Support.czbook: czCrawelHome,
            Support.ddxs: ddCrawelHome,
            Support.hetu: hetuCrawelHome, 
            Support.hj: hjCrawelHome,
            Support.pt: ptCrawelHome, 
            Support.quanben: quanCrawelHome, 
            Support.sf: sfCrawelHome,
            Support.sixnineshu: snCrawelHome,
            Support.uu: uuCrawelHome, 
            Support.wenku: wenCrawelHome, 
            Support.wutuxs: wutuxCrawelHome, 
            Support.zwdu: zwCrawelHome,
        }
        if self.site == Support.unknown:
            raise ValueError('Unsupport source website')
        print("Get novle information")
        return functions[self.site](homeLink)

    def getArticleList(self, rootSoup, startChapterName):
        functions = {
            Support.b520: b520GetArticleList,
            Support.bimidu: bimGetArticleList,
            Support.biquyue: biquGetArticleList,
            Support.book8: b8GetArticleList,
            Support.cnuu: cnuuGetArticleList,
            Support.czbook: czGetArticleList,
            Support.ddxs: ddGetArticleList,
            Support.hetu: hetuGetArticleList, 
            Support.hj: hjGetArticleList,
            Support.pt: ptGetArticleList, 
            Support.quanben: quanGetArticleList, 
            Support.sf: sfGetArticleList,
            Support.sixnineshu: snGetArticleList,
            Support.uu: uuGetArticleList, 
            Support.wenku: wenGetArticleList, 
            Support.wutuxs: wutuxGetArticleList, 
            Support.zwdu: zwGetArticleList,
        }
        print("Get novel chapter list")
        return functions[self.site](rootSoup, startChapterName)

    def crawelArticle(self, href):
        functions = {
            Support.b520: b520CrawelArticle,
            Support.bimidu: bimCrawelArticle,
            Support.biquyue: biquCrawelArticle,
            Support.book8: b8CrawelArticle,
            Support.cnuu: cnuuCrawelArticle,
            Support.czbook: czCrawelArticle,
            Support.ddxs: ddCrawelArticle,
            Support.hetu: hetuCrawelArticle, 
            Support.hj: hjCrawelArticle,
            Support.pt: ptCrawelArticle, 
            Support.quanben: quanCrawelArticle, 
            Support.sf: sfCrawelArticle,
            Support.sixnineshu: snCrawelArticle,
            Support.uu: uuCrawelArticle, 
            Support.wenku: wenCrawelArticle, 
            Support.wutuxs: wutuxCrawelArticle, 
            Support.zwdu: zwCrawelArticle,
        }
        print("Get novel content: {}".format(href))
        return functions[self.site](href)
