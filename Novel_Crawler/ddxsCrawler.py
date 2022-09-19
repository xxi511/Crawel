#coding=utf-8
from format import format, s2tw
import helpers
import driver


def crawelHome(homeLink):
    chrome = driver.get_selenium(homeLink)
    banner = 'https://www.ddxs.com' + chrome.find_element_by_css_selector('dd.info div.pic img').get_attribute("src")
    title = s2tw(chrome.find_element_by_css_selector('div.btitle h1').text)
    desc = format(s2tw(chrome.find_element_by_css_selector('div.js div.intro').text))
    author = s2tw(chrome.find_element_by_css_selector('div.btitle i').text)
    state = '(連載中)'
    return chrome, banner, title, author, state, desc


def getArticleList(chrome, startChapterName):
    shouldStart = False
    hrefs = []
    table = chrome.find_elements_by_css_selector('table')[1]
    atags = table.find_elements_by_css_selector('a')
    for atag in atags:
        href = atag.get_attribute("href")
        if not shouldStart:
            if startChapterName in atag.text:
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
    chrome = driver.get_selenium(href)
    title = s2tw(chrome.find_element_by_css_selector('#amain dl dd h1').text)
    content = s2tw(chrome.find_element_by_css_selector('#contents').text)
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://www.ddxs.com/wudiconggangtiexiakaishi/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')