import requests
from bs4 import BeautifulSoup
from format import format


def getSoup(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = soup.select_one('div.thumbnail img')['src']
    title = soup.select_one('div.info span.title').get_text()
    authorText = soup.select_one('div.info span.author').get_text()
    author = authorText.split(':')[1].strip()
    stateText = soup.select_one(
        'div.novel-detail div.state table').get_text()
    state = '(連載中)'
    descText = soup.select_one('div.novel-detail div.description').get_text()
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in rootSoup.select('ul.nav.chapter-list li a'):
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
        hrefs.append(atag['href'])
    return hrefs


def crawelArticle(href):
    link = 'https:' + href
    soup = getSoup(link)
    title = soup.select_one('div.name').get_text()
    content = soup.select_one('div.content').get_text()
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://czbooks.net/n/cpn92df'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')