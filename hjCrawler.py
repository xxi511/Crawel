import requests
import re
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def checkHomeLink(homeLink):
    if 'Chapter' in homeLink:
        return 'https://tw.hjwzw.com/Book/' + homeLink[-5:]
    else:
        return homeLink

def crawelHome(homeLink):
    link = checkHomeLink(homeLink)
    soup = getSoup(link)
    coverSelector = 'table[style="margin: 0 auto; width: 1000px; position: relative;"] td[style="width: 740px; background-color: White;"] table'
    coverTable = soup.select_one(coverSelector)
    banner = 'https://tw.hjwzw.com' + coverTable.select_one('div img')['src']

    authorSelector = 'td div[style="height: 300px; overflow: hidden;"]'
    authorDiv = coverTable.select_one(authorSelector)
    title = s2tw(soup.select_one('h1').get_text()).strip(' \r\n')
    author = s2tw(authorDiv.select_one('a').get_text())
    state = '(連載中)'

    descP = authorDiv.select('p')
    descText = ''
    for paragraph in descP:
        text = paragraph.next
        if '內容簡介' in text:
            descText = s2tw(text[6:])
            break
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    selector = 'table[style="margin: 0 auto; width: 1000px; position: relative;"] td[style="width: 740px; background-color: White;"] div[style="width: 100%"] a'
    link = 'https://tw.hjwzw.com' + rootSoup.select_one(selector)['href']
    soup = getSoup(link)
    shouldStart = False
    hrefs = []
    allLinks = soup.select('#tbchapterlist td a')
    for atag in allLinks:
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
    link = 'https://tw.hjwzw.com' + href
    soup = getSoup(link)
    selector = 'div[style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;"]'
    contentDiv = soup.select_one(selector)
    bookName = contentDiv.find('a').get_text()
    content = contentDiv.get_text()
    content = re.sub(bookName, '', content)
    content = s2tw(content)
    newContent = format(content)
    return newContent

if __name__ == '__main__':
    homeLink = 'https://tw.hjwzw.com/Book/33924'
    # https://tw.hjwzw.com/Book/33924
    # https://tw.hjwzw.com/Book/Chapter/33924
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')