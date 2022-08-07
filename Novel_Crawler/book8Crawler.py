#coding=utf-8
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.append(current)
import driver

from format import format, s2tw
import helpers
from selenium.webdriver.common.by import By


def crawelHome(homeLink):
    soup = helpers.getSoup(homeLink, helpers.Encoding.utf8)
    banner = 'https://8book.com' + soup.select_one('div.item-bg div.item-cover img')['src']
    title = s2tw(soup.select_one('div.item-bg div.item_content_box li.h2').get_text())
    author = s2tw(soup.select_one('div.item-bg div.item_content_box li span.item-info-author').get_text())
    state = '(連載中)'

    descText = s2tw(soup.select_one('div.item-bg div.item_content_box li.full_text').get_text())
    desc = format(descText)
    return soup, banner, title, author[3:], state, desc


def getArticleList(soup, startChapterName):
    shouldStart = False
    hrefs = []
    atags = soup.select('ul.row a')
    for atag in atags:
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
    link = 'https://8book.com' + href
    contents = []
    title = ""
    index = 1
    while True:
        page_link = '{}_{}'.format(link, index)
        chrome = driver.get_selenium(page_link)
        if title == '':
            title = s2tw(chrome.find_element(By.CSS_SELECTOR, '#subtitle').text)
        
        contentEle = chrome.find_element(By.CSS_SELECTOR, '#text').text.split('\n\n')
        contents = contents + contentEle
        spans = chrome.find_elements(By.CSS_SELECTOR, 'span.next')
        if len(spans) == 0:
            chrome.close()
            break
        next = s2tw(spans[0].text)
        chrome.close()
        if next == '下一篇':
            break
        index += 1
    content = s2tw('\n'.join(contents))
    newContent = format(title + '\n\r\n' + content)
    return newContent


if __name__ == '__main__':
    homeLink = 'https://8book.com/novelbooks/106587/'
    soup, banner, title, author, state, desc = crawelHome(homeLink)
    hrefs = getArticleList(soup, '')
    for h in hrefs:
        a = crawelArticle(h)
        print(a)
    print('a')