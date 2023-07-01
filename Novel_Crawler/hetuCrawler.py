import driver
from selenium.webdriver.common.by import By
from format import format, s2tw
import helpers


def crawelHome(homeLink):
    soup = helpers.getSoup(homeLink, helpers.Encoding.utf8)
    infoDiv = soup.select_one('div.book_info.finish')
    banner = 'https:' + infoDiv.select_one('img')['src']

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
    chrome = driver.get_selenium(href)
    h2s = chrome.find_elements(By.CSS_SELECTOR, '#content h2')
    
    h2Texts = []
    for h2 in h2s:
        h2Texts.append(s2tw(h2.text))
    title = ' '.join(h2Texts)
    contents = chrome.find_elements(By.CSS_SELECTOR, '#content div')
    contentTexts = []
    for div in contents:
        contentTexts.append(div.get_attribute('innerText'))
    content = s2tw('\n\n'.join(contentTexts))
    newContent = format(title + '\n\r\n' + content)
    chrome.quit()
    return newContent

if __name__ == '__main__':
    a = crawelArticle('https://hetushu.com/book/5636/4205265.html')
    # homeLink = 'https://hetushu.com/book/91/index.html'
    # soup, banner, title, author, state, desc = crawelHome(homeLink)
    # hrefs = getArticleList(soup, '')
    # for h in hrefs:
    #     a = crawelArticle(h)
    #     print(a)
    print('a')