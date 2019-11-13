from zwduCrawler import crawelHome as zwCrawelHome, getArticleList as zwGetArticleList, crawelArticle as zwCrawelArticle
from sfCrawler import crawelHome as sfCrawelHome, getArticleList as sfGetArticleList, crawelArticle as sfCrawelArticle
from hjCrawler import crawelHome as hjCrawelHome, getArticleList as hjGetArticleList, crawelArticle as hjCrawelArticle

class Crawler:
    def __init__(self):
        self.support = ['sf', 'zwdu', 'hj']
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
        else:
            raise ValueError('Unsupport source website')

    def getArticleList(self, rootSoup, startChapterName):
        if self.site == 'sf':
            return sfGetArticleList(rootSoup, startChapterName)
        elif self.site == 'zwdu':
            return  zwGetArticleList(rootSoup, startChapterName)
        elif self.site == 'hj':
            return hjGetArticleList(rootSoup, startChapterName)

    def crawelArticle(self, href):
        if self.site == 'sf':
            return sfCrawelArticle(href)
        elif self.site == 'zwdu':
            return zwCrawelArticle(href)
        elif self.site == 'hj':
            return hjCrawelArticle(href)
