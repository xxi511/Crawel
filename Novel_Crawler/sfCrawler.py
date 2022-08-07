import requests
import re
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers, verify=False)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = ''
    bannerImg = soup.select_one('div.summary-pic img')
    if bannerImg:
        banner = bannerImg['src']
    else:
        styleText = soup.select_one('div.d-banner')['style']
        urlText = re.search(r'url\(.*\)', styleText).group(0)
        banner = urlText[4:-1]

    title = s2tw(soup.select_one('div.summary-content h1.title span').get_text())
    author = s2tw(soup.select_one('div.author-name span').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.summary-content p.introduce').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    link = 'https://book.sfacg.com/' + rootSoup.select_one('#BasicOperation a')['href']
    soup = getSoup(link)
    shouldStart = False
    hrefs = []
    for atag in soup.select('div.catalog-list ul.clearfix li a'):
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
        if 'vip' in href:
            break
        hrefs.append(href)
    return hrefs


def crawelArticle(href):
    link = 'https://book.sfacg.com' + href
    soup = getSoup(link)
    title = s2tw(soup.select_one('div.article-hd h1.article-title').get_text())
    contentTexts = []
    contents = soup.select('#ChapterBody p')
    for c in contents:
        contentTexts.append(c.get_text())
    content = '\n\r'.join(contentTexts)
    content = s2tw(content)
    newContent = format(title + '\n\r\n' + content)
    return newContent

if __name__ == '__main__':
    homeLink = 'http://book.sfacg.com/Novel/210249/'
    # https://book.sfacg.com/Novel/57082/MainIndex/
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')