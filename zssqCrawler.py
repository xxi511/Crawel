import requests
import re
import base64
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    infoDiv = soup.select_one('.container .bookinfo')
    banner = 'https://zssq.cc' + infoDiv.select_one('.bimg img')['src']

    title = s2tw(infoDiv.select_one('.btitle h1').get_text())
    author = s2tw(infoDiv.select_one('.btitle em a').get_text())
    state = '(連載中)'

    desc = format(s2tw(infoDiv.select_one('.intro').get_text()))[5:]
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    shouldStart = False
    hrefs = []
    innerDiv = rootSoup.select('.container .inner')[-1]
    for atag in innerDiv.select('dd a'):
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
        hrefs.append('https://zssq.cc' + href)
    return hrefs


def crawelArticle(href):
    soup = getSoup(href)
    title = format(s2tw(soup.select_one('#main .inner h1').get_text()))
    content = s2tw(soup.select_one('#main .inner #BookText').get_text())
    newContent = format(title + '\n\r\n' + content)
    return newContent

if __name__ == '__main__':
    homeLink = 'https://zssq.cc/s/55603/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')