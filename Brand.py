# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 22:35
# @Author  : HoPGoldy
# 封装了chinasspp和wordToPic以提供了需要的方法

import requests
from Modules.ChinassppControl import Chinasspp
from Modules.WordToPic import transform
from setting import MIN_ADDITION_NUM, MAX_ADDITION_NUM, PIC_FOLDER_PATH

# 提供品牌名 返回一个指定字数区间内的介绍
def getBrandInfo(brandName, min=MIN_ADDITION_NUM, max=MAX_ADDITION_NUM):
    chinasspp = Chinasspp()
    returnBrands = chinasspp.searchBrand(brandName)

    if returnBrands is not None and len(returnBrands) != 0:
        for item in returnBrands:
            introduce = item['introduce']
            logoUrl = item['logo']
            if min > len(introduce) < max:
                return introduce, logoUrl
            elif len(introduce) >= MAX_ADDITION_NUM:
                return cutBrandIntroduce(introduce, min, max), logoUrl

    return None, None


# 将字符串切割为指定大小
def cutBrandIntroduce(str, min, max):
    segs = str.split('。')
    goodIntrodue = ''

    for seg in segs:
        goodIntrodue += seg
        if min < len(goodIntrodue) < max:
            return goodIntrodue

    return ' ' * MIN_ADDITION_NUM


# 下载品牌logo
def logoDownload(logoUrl, name):
    response = requests.get(logoUrl)
    response.raise_for_status()

    suffixTemp = logoUrl.split('.')
    suffix = suffixTemp[len(suffixTemp)-1]
    picPath = f'{PIC_FOLDER_PATH}/{name}.{suffix}'
    with open(picPath, 'wb') as f:
        f.write(response.content)
    return picPath


# 创建品牌logo
def logoCreate(brandName, name):
    picPath = f'{PIC_FOLDER_PATH}/{name}.jpg'
    transform(brandName, save_path=picPath)
    return picPath
