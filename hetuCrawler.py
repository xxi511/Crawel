import requests
import re
import base64
from bs4 import BeautifulSoup
from format import format, s2tw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform


def getSoup(link):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(link, headers=headers, verify=False)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
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

def getDriverPath():
    sys = platform.system()
    if 'Linux' in sys:
        return './driver/linux_chromedriver'
    elif 'Darwin' in sys:
        return './driver/mac_chromedriver'
    elif 'Windows' in sys:
        return './driver/win_chromedriver.exe'

def crawelArticle(href):
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(getDriverPath(), chrome_options=options)
    driver.get(href)
    h2s = driver.find_elements_by_css_selector('#content h2')
    h2Texts = []
    for h2 in h2s:
        h2Texts.append(s2tw(h2.text))
    title = ' '.join(h2Texts)
    contents = driver.find_elements_by_css_selector('#content div')
    contentTexts = []
    for div in contents:
        contentTexts.append(div.get_attribute('innerText'))
    content = s2tw('\n\n'.join(contentTexts))
    newContent = format(title + '\n\r\n' + content)
    return newContent

if __name__ == '__main__':
    homeLink = 'https://hetushu.com/book/91/index.html'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')