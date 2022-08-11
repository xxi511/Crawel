#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
from format import format, s2tw
import helpers


def getSoup(link):
    resp = requests.get(link, verify=False)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def checkHomeLink(homeLink):
    if homeLink.endswith('/list.html'):
        return homeLink
    else:
        return homeLink + 'list.html'


def crawelHome(homeLink):
    _homeLink = checkHomeLink(homeLink)
    soup = helpers.getSoup(_homeLink, helpers.Encoding.utf8)
    banner = soup.select_one('div.list2 img')['src']
    title = s2tw(soup.select_one('div.list2 span[itemprop="name"]').get_text())
    info_ps = soup.select('#info p')
    author = s2tw(soup.select_one('div.list2 span[itemprop="author"]').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.description p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('div.box ul.list3 li a'):
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
    link = 'http://www.quanben.io' + href
    soup = helpers.getSoup(link, helpers.Encoding.utf8)
    # loadMore(soup)
    title = s2tw(soup.select_one('h1.headline').get_text())
    contentTexts = []
    contents = soup.select('#content p')
    for c in contents:
        contentTexts.append(c.get_text())
    content = '\n\r'.join(contentTexts)
    content = s2tw(content)
    newContent = format(title + '\n\r\n' + content)
    return newContent

def loadMore(soup):
    loadStr = soup.select_one("div.more a")['onclick']
    loadPattern = r"'([a-zA-Z0-9]*)'"
    loadMatch = re.findall(loadPattern, loadStr)

    script = soup.find('script', type='text/javascript').text
    pattern = r"myScript.src = [\S].*pinyin="
    match = re.search(pattern, script).group()
    link = "http://www.quanben.io" + match[16:] + loadMatch[0] + "&id=" + loadMatch[1]
    resp = requests.get(link)
    resp.encoding = "utf-8"

if __name__ == '__main__':
    homeLink = 'http://www.quanben.io/n/xiaoyuanquannenggaoshou/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')