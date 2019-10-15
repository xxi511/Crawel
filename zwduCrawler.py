import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    resp = requests.get(link)
    resp.encoding = "gbk"
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = soup.select_one('#fmimg img')['src']
    title = s2tw(soup.select_one('#info h1').get_text())
    info_ps = soup.select('#info p')
    author = ''
    state = ''
    for p in info_ps:
        text = p.get_text()
        if '作\xa0\xa0\xa0\xa0者' in text:
            author = s2tw(text.split('：')[1].strip())
        elif '状\xa0\xa0\xa0\xa0态：' in text:
            state = '(已完結)' if '已完结' in text else '(連載中)'

    descText = s2tw(soup.select_one('#intro p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('#list dl dd a'):
        if not shouldStart:
            if startChapterName in atag.get_text():
                shouldStart = True
            else:
                continue
        href = atag['href']
        hrefs.append(href)
    return hrefs


def crawelArticle(href):
    link = 'https://www.zwdu.com' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('div.bookname h1').get_text())
    content = s2tw(soup.select_one('#content').get_text())
    newContent = format(title + '\n\r\n' + content)
    return newContent