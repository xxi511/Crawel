#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link)
    resp.encoding = "Big5"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = 'https://8book.com' + soup.select_one('td[align="center"]>img')['src']
    title = s2tw(soup.select_one('td[height="80"]>font').get_text())
    author = s2tw(soup.select_one('td[height="30"]>font').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('td>p>span').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    atags = soup.select('table.episodelist tr td a')
    for atag in atags:
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
    link = 'https://8book.com' + href
    soup = getSoup(link)

    title = s2tw(soup.select_one('table[width="95%"] td[height="80"]>font').get_text())
    contentEle = soup.select_one('p.content')
    [ad.decompose() for ad in contentEle.select('table')]
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://8book.com/books/novelbook_106587.html'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')