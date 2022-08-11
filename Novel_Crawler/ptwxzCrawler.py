import driver
import requests
from bs4 import BeautifulSoup
from format import format, s2tw



def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers, verify=False)
    resp.encoding = 'gbk'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def checkHomeLink(homeLink):
    # https://www.ptwxz.com/bookinfo/6/6326.html
    # https://www.ptwxz.com/html/6/6326/
    if 'bookinfo' in homeLink:
        return homeLink
    else:
        split = homeLink.split('/')
        return "https://www.ptwxz.com/bookinfo/{}/{}.html".format(split[-3], split[-2])

def crawelHome(homeLink):
    link = checkHomeLink(homeLink)
    soup = getSoup(link)
    bannerSelector = '#content table[width="96%"] tr td table img[width="100"]'
    banner = soup.select_one(bannerSelector)['src']

    authorSelector = '#content table[width="96%"] tr td td[width="25%"]'
    authorDiv = soup.select(authorSelector)[1]
    title = s2tw(soup.select_one('h1').get_text()).strip(' \r\n')
    author = s2tw(authorDiv.text.split('：')[1])
    state = '(連載中)'

    descDiv = soup.select_one('div[style="float:left;width:460px;"]')
    [span.decompose() for span in descDiv.select('span')]
    [link.decompose() for link in descDiv.select('a')]
    [br.decompose() for br in descDiv.select('br')]
    desc = format(s2tw(descDiv.text))
    return soup, banner, title, author, state, desc


def getArticleList(rootSoup, startChapterName):
    selector = 'table[width="100%"][border="0"][cellpadding="3"] td[width="20%"] a'
    href = rootSoup.select_one(selector)['href']
    link = href if href.startswith('http') else "https://www.ptwxz.com" + href
    soup = getSoup(link)
    shouldStart = False
    hrefs = []
    allLinks = soup.select('div.centent ul li a:not([rel])')
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
        hrefs.append(link + href)
    return hrefs


def crawelArticle(href):
    chrome = driver.get_selenium(href)
    chrome.execute_script("return document.querySelector('div.toplink').remove()")
    chrome.execute_script("return document.querySelector('div.share').remove()")
    contentDiv = chrome.find_element_by_css_selector("#content")
    content = contentDiv.text
    chrome.quit()

    content = s2tw(content)
    newContent = format(content)
    return newContent

if __name__ == '__main__':
    homeLink = 'https://www.ptwxz.com/bookinfo/9/9207.html'
    # https://tw.hjwzw.com/Book/33924
    # https://tw.hjwzw.com/Book/Chapter/33924
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')