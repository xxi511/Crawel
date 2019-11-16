# coding: utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers)
    resp.encoding = 'gbk'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    tableSelector = '#content > div[style="width:99%;margin:auto;"] > table'
    tables = soup.select(tableSelector)
    title = ''
    banner = ''
    author = ''
    desc = ''
    for table in tables:
        trs = table.select('tr')
        if len(trs) == 1:
            banner = table.select_one('img')['src']
            midTd = table.select('tr td')[1]
            descText = s2tw(midTd.select('span')[4].get_text())
            desc = format(descText)
        else:
            title = s2tw(table.select_one('b').get_text())
            author = s2tw(table.select('tr > td[width="20%"]')[1].get_text()[5:])


    state = '(連載中)'
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    link = rootSoup.select_one('fieldset a')['href']
    soup = getSoup(link)
    shouldStart = False
    hrefs = []
    for atag in soup.select('table td a'):
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
        hrefs.append(link[:-9]+href)
    return hrefs


def crawelArticle(href):
    soup = getSoup(href)
    title = s2tw(soup.select_one('div#title').get_text())
    content = soup.select_one('div#content').get_text()
    content = s2tw(content)
    newContent = format(title + '\n\r\n' + content)
    return newContent

if __name__ == '__main__':
    homeLink = 'https://www.wenku8.net/book/2428.htm'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')