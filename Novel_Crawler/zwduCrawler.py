#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link, verify=False)
    # resp.encoding = "gbk"
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
    link = 'https://www.81book.com' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('div.bookname h1').get_text())
    contentEle = soup.select_one('#content')
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://www.81book.com/book/33263/'
    # https://tw.hjwzw.com/Book/33924
    # https://tw.hjwzw.com/Book/Chapter/33924
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')