#coding=utf-8
from format import format, s2tw
import helpers
import driver

# this file is for https://ddxs.com/chaojisangshigongchang/

def crawelHome(homeLink):
    chrome = driver.get_selenium(homeLink)
    banner = chrome.find_element_by_css_selector('div.book_box div.fm img').get_attribute("src")
    title = s2tw(chrome.find_element_by_css_selector('div.xx dl dt').text)
    desc = format(s2tw(chrome.find_element_by_css_selector('div.book_box p.intro').text))
    author = s2tw(chrome.find_element_by_css_selector('div.xx dl dd').text)
    state = '(連載中)'
    return chrome, banner, title, author, state, desc


def getArticleList(chrome, startChapterName):
    listURL = chrome.current_url + 'all.html'
    newChrome = driver.get_selenium(listURL)
    shouldStart = False
    hrefs = []
    table = newChrome.find_element_by_css_selector('dl.list-striped')
    atags = table.find_elements_by_css_selector('dd a')
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
    content = s2tw(chrome.find_element_by_css_selector('#nr').text)
    newContent = format(content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://ddxs.com/chaojisangshigongchang/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')