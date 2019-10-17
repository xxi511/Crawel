from zwduCrawler import crawelHome as zwCrawelHome, getArticleList as zwGetArticleList, crawelArticle as zwCrawelArticle
from sfCrawler import crawelHome as sfCrawelHome, getArticleList as sfGetArticleList, crawelArticle as sfCrawelArticle

class Crawler:
    def __init__(self):
        self.support = ['sf', 'zwdu']
        self.site = ''

    def crawelHome(self, homeLink):
        if 'book.sfacg.com' in homeLink:
            self.site = 'sf'
            return sfCrawelHome(homeLink)
        elif 'zwdu.com' in homeLink:
            self.site = 'zwdu'
            return zwCrawelHome(homeLink)
        else:
            raise ValueError('Unsupport source website')

    def getArticleList(self, rootSoup, startChapterName):
        if self.site == 'sf':
            return sfGetArticleList(rootSoup, startChapterName)
        elif self.site == 'zwdu':
            return  zwGetArticleList(rootSoup, startChapterName)

    def crawelArticle(self, href):
        if self.site == 'sf':
            return sfCrawelArticle(href)
        elif self.site == 'zwdu':
            return zwCrawelArticle(href)