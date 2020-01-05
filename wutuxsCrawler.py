#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link)
    resp.encoding = "gbk"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = soup.select_one('div.info div.pic img')['src']
    title = s2tw(soup.select_one('div.book div.btitle h1').get_text())
    author = s2tw(soup.select_one('div.book div.btitle i').get_text().split('：')[1])
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.js p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('dd #at td a'):
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
    link = 'https://www.wutuxs.com' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('div.bdsub dl dd h1').get_text())
    contentEle = soup.select_one('#contents')
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://www.wutuxs.com/html/5/5597/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')