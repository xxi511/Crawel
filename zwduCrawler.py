#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link, verify=False)
    resp.encoding = "gbk"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = soup.select_one('#fmimg img')['src']
    title = s2tw(soup.select_one('#info h1').get_text())
    info_ps = soup.select('#info p')
    author = ''
    state = '(連載中)'
    for p in info_ps:
        text = p.get_text()
        if '作\xa0\xa0\xa0\xa0者' in text:
            author = s2tw(text.split('：')[1].strip())

    descText = s2tw(soup.select_one('#intro p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('#list dl dd a'):
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
    link = 'https://www.zwdu.com' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('div.bookname h1').get_text())
    contentEle = soup.select_one('#content')
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    href = '/book/40503/17761682.html'
    crawelArticle(href)