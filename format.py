# coding: utf-8
import re
from opencc import OpenCC

cc = OpenCC('s2tw')
wordDic = []


def s2tw(content):
    # s2tw Simplified Chinese to Traditional Chinese (Taiwan standard)
    line = cc.convert(content)
    return line


def format(content):
    newContent = trimSpace(content)
    replace = replacement(newContent)
    return trimSpace(replace)


def trimSpace(content):
    newContent = re.sub(r'\xa0', '\r\n', content)
    newContent = re.sub(r'\u3000', '', newContent)
    newContent = re.sub(r'\n', '', newContent)
    splits = newContent.split('\r')
    newSplits = []
    for idx, sen in enumerate(splits):
        _sen = sen.strip()
        if _sen == '':
            continue
        if (idx != 0):
            _sen = '　　' + sen.strip()
        newSplits.append(_sen)

    newContent = "\n\r\n".join(newSplits)
    return newContent


def replacement(content):
    newContent = content
    arr = loadData()
    patterns = ['Ｗ.*Ｗ.*Ｗ.*Ｃ.*Ｏ.*Ｍ.*', '[\?]*八.*一.*中.*文.*[網网]*[\?]*']
    for pattern in patterns:
        newContent = re.sub(pattern, '', newContent)
    for d in arr:
        olds = d['olds']
        news = d['news'] if d['news'] != '!@#$%' else ''
        if '*' in olds:
            olds = re.sub('\*', '\*', olds)
        if '?' in olds:
            olds = re.sub('\?', '\?', olds)
        newContent = re.sub(r'{}'.format(olds), news, newContent)
    return newContent


def loadData():
    if len(wordDic) > 0:
        return wordDic

    with open('data.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            old, new = line[:-1].split('#####')
            d = {'olds': old, 'news': new}
            wordDic.append(d)
    return wordDic
