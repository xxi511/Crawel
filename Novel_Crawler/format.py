# coding: utf-8
import os
import re
from opencc import OpenCC

cc = OpenCC('s2tw')
wordDic = []
regexArr = []


def s2tw(content):
    # s2tw Simplified Chinese to Traditional Chinese (Taiwan standard)
    line = cc.convert(content)
    return line


def format(content):
    newContent = replacement(content)
    result = trimSpace(newContent)

    return trimSpace(result)


def trimSpace(content):
    newContent = content.strip()
    newContent = re.sub(r'\t', '', newContent)
    newContent = re.sub(r'\u3000', '', newContent)
    newContent = re.sub(r'\r', '', newContent)
    splits = newContent.split('\n')
    newSplits = []
    for idx, sen in enumerate(splits):
        _sen = sen.strip()
        if _sen == '':
            continue
        if (len(newSplits) != 0):
            _sen = '　　' + sen.strip()
        newSplits.append(_sen)

    newContent = "\n\r\n".join(newSplits)
    return newContent


def replacement(content):
    newContent = content
    arr = loadData()
    patterns = loadRegexData()
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

def get_parent_folder() -> str:
    parent_dir = os.getcwd()
    if parent_dir.endswith('Novel_Crawler'):
        parent_dir = os.path.dirname(parent_dir)
    return parent_dir

def loadData():
    if len(wordDic) > 0:
        return wordDic

    parent_dir = get_parent_folder()
    path = os.path.join(parent_dir, 'data.txt')
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            old, new = line[:-1].split('#####')
            d = {'olds': old, 'news': new}
            wordDic.append(d)
    return wordDic

def loadRegexData():
    if len(regexArr) > 0:
        return regexArr

    parent_dir = get_parent_folder()
    path = os.path.join(parent_dir, 'regex.txt')
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            txt = line.replace('\n', '')
            txt = txt.replace('/', '\/')
            regexArr.append(txt)
    return regexArr