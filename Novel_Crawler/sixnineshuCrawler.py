#coding=utf-8
from format import format, s2tw
import helpers
from urllib.parse import urlparse

def format_homeLink(link: str) -> str:
    parsed = urlparse(link)
    host = '{}://{}'.format(parsed.scheme, parsed.hostname)
    path = parsed.path[1:-1]
    if ''.endswith('.htm'):
        return '{}/{}'.format(host, path)
    else:
        return '{}/{}.htm'.format(host, path)

def format_chapter_link(link: str) -> str:
    if 'txt' in link:
        parsed = urlparse(link)
        host = '{}://{}'.format(parsed.scheme, parsed.hostname)
        paths = parsed.path.split('/')
        path = paths[-1].split('.')[0]
        return '{}/{}/'.format(host, path)
    else:
        return link

def crawelHome(homeLink):
    link = format_homeLink(homeLink)
    soup = helpers.getSoup(link, helpers.Encoding.gbk)
    banner = soup.select_one('div.bookimg2 img')['src']
    title = s2tw(soup.select_one('div.booknav2 h1 a').get_text())
    author = s2tw(soup.select_one('div.booknav2 p a').get_text())
    state = '(連載中)'
    desc = ''

    chapter_link = soup.select_one('div.addbtn a.btn')['href']
    chapter_soup = helpers.getSoup(chapter_link, helpers.Encoding.gbk)
    return chapter_soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    tags = soup.select('#catalog ul li a')
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
    soup = helpers.getSoup(href, helpers.Encoding.gbk)
    title = s2tw(soup.select_one('div.txtnav h1.hide720').get_text())
    txtnav = soup.select_one('div.txtnav')
    removed = ['h1.hide720', 'div.txtinfo', '#txtright', '#bottom-ad']
    for selector in removed:
        [element.decompose() for element in txtnav.select(selector)]
    content = s2tw(txtnav.get_text())
    if title in content:
        return format(content)
    else:
        newContent = format(title + '\n\r\n' + content)
        return newContent


if __name__ == '__main__':
    homeLink = 'https://www.69xinshu.com/book/45165/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')