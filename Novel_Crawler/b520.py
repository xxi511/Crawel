#coding=utf-8
from format import format, s2tw
import helpers

def crawelHome(homeLink):
    soup = helpers.getSoup(homeLink, helpers.Encoding.gbk)
    banner = soup.select_one('#fmimg img')['src'] 
    title = s2tw(soup.select_one('#info h1').get_text())
    author = s2tw(soup.select_one('#info p').get_text())[7:]
    state = '(連載中)'
    descText = s2tw(soup.select_one('#intro p').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    tags = soup.select('#list dd a')
    for atag in tags:
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
    title = s2tw(soup.select_one('div.bookname h1').get_text())
    content = s2tw(soup.select_one('#content').get_text())
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'http://www.b520.cc/0_111/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, 'http://www.b520.cc/0_111/75039.html')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')