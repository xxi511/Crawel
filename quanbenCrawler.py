#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def checkHomeLink(homeLink):
    if homeLink.endswith('/list.html'):
        return homeLink
    else:
        return homeLink + 'list.html'


def crawelHome(homeLink):
    _homeLink = checkHomeLink(homeLink)
    soup = getSoup(_homeLink)
    banner = soup.select_one('div.list2 img')['src']
    title = s2tw(soup.select_one('div.list2 span[itemprop="name"]').get_text())
    info_ps = soup.select('#info p')
    author = s2tw(soup.select_one('div.list2 span[itemprop="author"]').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.description p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('div.box ul.list3 li a'):
        href = atag['href']
        if not shouldStart:
            if startChapterName in atag.get_text():
                shouldStart = True
            elif startChapterName in href:
                shouldStart = True
            elif href in startChapterName:
                shouldStart = True
            else:
                continue
        hrefs.append(href)
    return hrefs


def crawelArticle(href):
    link = 'http://www.quanben.io' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('h1.headline').get_text())
    contentTexts = []
    contents = soup.select('#content p')
    for c in contents:
        contentTexts.append(c.get_text())
    content = '\n\r'.join(contentTexts)
    content = s2tw(content)
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'http://www.quanben.io/n/xiaoyuanquannenggaoshou/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')