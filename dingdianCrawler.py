#coding=utf-8
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.get(link, headers = headers, verify=False)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = 'https://www.dingdian.org' + soup.select_one('#fmimg img')['src']
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
    hrefs = []
    for atag in soup.select('dd a'):
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
    link = 'https://www.dingdianorg.com' + href
    soup = getSoup(link)
    soup.select_one('#TXT div.bottem').decompose()
    fonts = soup.select('#TXT font')
    for font in fonts:
        font.decompose()
    scripts = soup.select('#TXT script')
    for script in scripts:
        script.decompose()
    title = s2tw(soup.select_one('div.zhangjieming h1').get_text())
    contentEle = soup.select_one('#TXT')
    contents = contentEle.decode_contents().split('<br/><br/>')
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