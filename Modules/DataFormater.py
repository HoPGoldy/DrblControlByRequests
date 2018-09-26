# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 16:39
# @Author  : HoPGoldy

import win32clipboard as w
import win32con
from setting import CATEGORY
import re
import random

dataSplitReg = r'━━━━第[0-9]+个条目━━━━[\s]+'
urlReg = '[\S]+(?=\r\n)'
brandReg = r'(?<=宝贝名：\r\n)[\S]+'
titleReg = r'(?<=[\s])[\S]+(?=\r\n长亮点)'
longHighLightsReg = r'(?<=长亮点：\r\n)[\S]+\r\n[\S]+\r\n[\S]+'
shortHighLightReg = r'(?<=短亮点：\r\n)[\S]+\r\n[\S]+\r\n[\S]+'
designHighlightReg = r'(?<=设计亮点\r\n)[\S]+(?=\r\n)'
otherAdditionTitleReg = r'(搭配指南|材质解析)'
otherAdditionContentReg = r'(?<=(搭配指南|材质解析)\r\n)[\S]+'


def getClipBoardData():
    w.OpenClipboard()
    text = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()

    return text


def formatDataByReg(text):
    dataTemps = re.split(dataSplitReg, text)
    datas = []
    for i in range(1, len(dataTemps)):
        dataTemp = dataTemps[i]
        brand = getBrand(dataTemp)

        data = {
            'category': CATEGORY,
            'brand': brand,
            'targetPeople': (9, random.randint(47, 51)),
            'url': getUrl(dataTemp),
            'title': f'{brand} {getTitle(dataTemp)}',
            'longHighLight': getLongHighLights(dataTemp),
            'shortHighLight': getShortHighLights(dataTemp),
            'addition': [{
                    'title': getOtherAdditionTitle(dataTemp),
                    'content': getOtherAdditionContent(dataTemp)}
                ]
            }
        datas.append(data)
    return datas


def show(datas):
    print()
    for i in range(0, len(datas)):
        print(f'[检查] ————————————————条目{i + 1}————————————————')
        print(f'[检查] 分类索引 > {datas[i]["category"]}')
        print(f'[检查] 目标人群索引 > {datas[i]["targetPeople"][0]}, {datas[i]["targetPeople"][1]}')
        print(f'[检查] 商品链接 > {datas[i]["url"]}')
        print(f'[检查] 标题 > {datas[i]["title"]}')
        for longHighLight in datas[i]['longHighLight']:
            print(f'[检查] 长亮点 > {longHighLight}')
        for shortHighLight in datas[i]['shortHighLight']:
            print(f'[检查] 短亮点 > {shortHighLight}')
        for addition in datas[i]['addition']:
            if 'brand' in addition:
                print(f'[检查] {addition["title"]}: {addition["brand"]} > {addition["content"]}')
            else:
                print(f'[检查] {addition["title"]} > {addition["content"]}')
        print()


def getUrl(data):
    return re.search(urlReg, data).group(0)


def getBrand(data):
    return re.search(brandReg, data).group(0)


def getTitle(data):
    return re.search(titleReg, data).group(0)


def getLongHighLights(data):
    longHighLightsText = re.search(longHighLightsReg, data).group(0)
    return re.split(r'\r\n', longHighLightsText)


def getShortHighLights(data):
    shortHighLightsText = re.search(shortHighLightReg, data).group(0)
    return re.split(r'\r\n', shortHighLightsText)


def getDesignHighlight(data):
    return re.search(designHighlightReg, data).group(0)


def getOtherAdditionTitle(data):
    return re.search(otherAdditionTitleReg, data).group(0)


def getOtherAdditionContent(data):
    return re.search(otherAdditionContentReg, data).group(0)

