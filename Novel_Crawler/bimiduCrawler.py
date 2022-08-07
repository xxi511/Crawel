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
    banner = soup.select_one('img')['src']
    title = s2tw(soup.select_one('div.info h2').get_text())
    info_ps = soup.select('div.info p.info-xg span')
    author = ''
    state = '(連載中)'
    for p in info_ps:
        text = p.get_text()
        if '作者：' in text:
            author = s2tw(text.split('：')[1].strip())

    descText = s2tw(soup.select_one('div.detail-body-body p.text-indent').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    ulEle = soup.select('div.newzjlist ul.dirlist')[1]
    path = soup.select_one('meta[property="og:url"]')['content']
    shouldStart = False
    hrefs = []
    for atag in ulEle.select('li a'):
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
        hrefs.append(path+href)
    return hrefs


def crawelArticle(href):
    soup = getSoup(href)
    title = s2tw(soup.select_one('div.play-title h1').get_text())
    contentEle = soup.select_one('div.txt_tcontent')
    contents = contentEle.decode_contents().split('<br/>')
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    link = "https://www.bimidu.com/3/3141/"
    soup, banner, title, author, state, desc = crawelHome(link)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')