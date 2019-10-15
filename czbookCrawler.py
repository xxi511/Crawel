import requests
from bs4 import BeautifulSoup
from format import format


def getSoup(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = soup.select_one('div.thumbnail img')['src']
    title = soup.select_one('div.info span.title').get_text()
    authorText = soup.select_one('div.info span.author').get_text()
    author = authorText.split(':')[1].strip()
    stateText = soup.select_one(
        'div.novel-detail div.state table').get_text()
    state = "(已完結)" if '已完結' in stateText else '(連載中)'
    descText = soup.select_one('div.novel-detail div.description').get_text()
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startFrom):
    for idx, atag in enumerate(soup.select('ul.nav.chapter-list li a')):
        if idx + 1 < startFrom - 1:
            continue
        print(atag)
        href = atag['href']
        crawelArticle(href)


def crawelArticle(href):
    link = 'https:' + href
    soup = getSoup(link)
    title = soup.select_one('div.name').get_text()
    content = soup.select_one('div.content').get_text()
    newContent = format(title + '\n\r\n' + content)
    return newContent
