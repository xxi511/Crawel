#coding=utf-8
import driver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from format import format, s2tw


def getSoup(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.get(link, headers=headers, verify=False)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def crawelHome(homeLink):
    soup = getSoup(homeLink)
    banner = 'https:' + soup.select_one('dl.jieshao a img')['src']
    title = s2tw(soup.select_one('dd.jieshao_content h1').get_text())[:-4]
    author = s2tw(soup.select_one('dd.jieshao_content h2 a').get_text())
    state = '(連載中)'
    descText = s2tw(soup.select_one('dd.jieshao_content h3').get_text())
    desc = format(descText)
    return soup, banner, title, author, state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    tags = soup.select('#chapterList li a')
    for atag in reversed(tags):
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
    link = 'https://tw.uukanshu.com/' + href
    chrome = driver.get_selenium(link)
    # title = s2tw(soup.select_one('div.h1title h1').get_text())
    title = s2tw(chrome.find_element(By.CSS_SELECTOR, 'div.h1title h1').text)
    contentElements = chrome.find_elements(By.CSS_SELECTOR, '#contentbox p')
    contents = [element.text for element in contentElements]
    if '最新網址' in contents[0]:
        contents.pop(0)
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent

if __name__ == '__main__':
    # href = 'b/69861/217812.html'
    # a = crawelArticle(href)

    homeLink = 'https://tw.uukanshu.com/b/69861/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')