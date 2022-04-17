#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.get(link, headers = headers, verify=False)
    resp.encoding = "gbk"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = 'https://www.230book.net/' + soup.select_one('#fmimg img')['src']
    title = s2tw(soup.select_one('#info h1').get_text())
    info_ps = soup.select('#info p')
    author = ''
    state = '(連載中)'
    for p in info_ps:
        text = p.get_text()
        if '者：' in text:
            author = s2tw(text.split('：')[1].strip())

    descText = s2tw(soup.select_one('#intro').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    meta = soup.select_one('meta[property="og:url"]')
    prefix = meta["content"]
    hrefs = []
    for atag in soup.select('#list ul li a'):
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
        hrefs.append(prefix + href)
    return hrefs


def crawelArticle(href):
    soup = getSoup(href)
    title = s2tw(soup.select_one('div.bookname h1').get_text())
    contentEle = soup.select_one('#content')
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://www.dingdian.org/lyd63902/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')