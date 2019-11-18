import requests
import re
import base64
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    infoDiv = soup.select_one('div.book_info.finish')
    banner = 'https://hetushu.com' + infoDiv.select_one('img')['src']

    title = s2tw(infoDiv.select_one('h2').get_text())
    author = s2tw(infoDiv.select_one('div').get_text())[3:]
    state = '(連載中)'

    descP = soup.select('div.intro p')
    descTexts = []
    for p in descP:
        descTexts.append(format(s2tw(p.get_text())))
    desc = '\n'.join(descTexts)
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in rootSoup.select('#dir a'):
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
        hrefs.append('https://hetushu.com' + href)
    return hrefs


def crawelArticle(href):
    soup = getSoup(href)
    h2s = soup.select('#content h2')
    h2Texts = []
    for h2 in h2s:
        h2Texts.append(s2tw(h2.get_text()))
    title = ' '.join(h2Texts)
    contentTexts = rearrange(soup)
    content = '\n\r'.join(contentTexts)
    content = s2tw(content)
    newContent = format(title + '\n\r\n' + content)
    return newContent

def rearrange(soup):
    # soup = getSoup('href')
    b64Data = soup.find_all('meta')[4]['content']
    b64Decode = base64.b64decode(b64Data).decode('utf8')
    indexRefs = re.split(r'[A-Z]+%', b64Decode)
    indexRefs = list(map(int,indexRefs))
    contentDiv = soup.select_one('#content')
    star = 0
    children = list(contentDiv.children)
    for i, ele in enumerate(children):
        if ele.name == 'h2':
            star = i + 1
        elif ele.name == 'div' and (not ele.has_attr('class') or ele['class'] is not 'chapter'):
            break

    real = [None] * len(indexRefs)
    j = 0
    for i, ele in enumerate(indexRefs):
        if indexRefs[i] < 5:
            real[indexRefs[i]] = children[i + star].decode_contents()
            j += 1
        else:
            real[indexRefs[i] - j] = children[i + star].decode_contents()

    return real


if __name__ == '__main__':
    homeLink = 'https://hetushu.com/book/91/index.html'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')