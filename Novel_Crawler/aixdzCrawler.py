#coding=utf-8
from format import format, s2tw
import helpers


def crawelHome(homeLink):
    soup = helpers.getSoup(homeLink, helpers.Encoding.utf8)
    banner = soup.select_one('div.d_af img')['src']
    title = s2tw(soup.select_one('div.d_info h1').get_text())
    author = s2tw(soup.select_one('div.d_ac ul li a').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.d_co').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    for atag in soup.select('#i-chapter ul li a'):
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
    link = 'https://www.aixdzs.com' + href
    soup = helpers.getSoup(link, helpers.Encoding.utf8)
    title = s2tw(soup.select_one('div.line h1').get_text())
    contentEles = soup.select('div.content p')
    contents = [p.get_text() for p in contentEles]
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://www.aixdzs.com/novel/%E4%B8%89%E5%AF%B8%E4%BA%BA%E9%97%B4'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')