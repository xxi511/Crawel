#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw
import helpers

def crawelHome(homeLink):
    soup = helpers.getSoup(homeLink, helpers.Encoding.utf8)
    banner = soup.select_one('img.thumbnail')['src'] 
    title = s2tw(soup.select_one('h1.booktitle').get_text())
    author = s2tw(soup.select_one('p.booktag a').get_text())
    state = '(連載中)'
    descText = s2tw(soup.select_one('p.bookintro').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    tags = soup.select('#list-chapterAll dd a')
    for atag in reversed(tags):
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
    soup = helpers.getSoup(href, helpers.Encoding.utf8)
    title = s2tw(soup.select_one('h1.pt10').get_text())
    content = s2tw(soup.select_one('p.readcotent').get_text())
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://cn.uukanshu.cc/book/2063/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')