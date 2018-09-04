# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 19:11
# @Author  : HoPGoldy

import requests
from lxml import etree
import re


class Chinasspp():
    _session = None

    _baseUrl = 'http://www.chinasspp.com/brand/brands.html'
    _ladiesPageUrl = 'http://www.chinasspp.com/brand/%E5%A5%B3%E8%A3%85%E5%93%81%E7%89%8C/'
    _MainPageSourceReg = '(?<=/span><h1>品牌大全</h1></div>)[\s\S]*(?=p id="l_page" class="pagination">)'
    _ladiesMainPageSourceReg = '(?<=/span><h1>女装品牌大全</h1></div>)[\s\S]*(?=p id="l_page" class="pagination">)'
    _ItemsUrlReg = 'http://www.chinasspp.com/brand/[\S]*/'
    _itemNameReg = '(?<=h2><strong>)[\S\u4e00-\u9fa5]*(?= 品牌简介)'
    _itemNameXpath = '//*[@id="container"]/div[4]/h2/strong/text()'
    _itemIntroduceXpath = '//*[@id="container"]/div[4]/div/p/text()'
    _itemIntroduceSpareXpath = '//*[@id="container"]/div[3]/div/p/text()'
    _brandLogoXpath = '//*[@id="container"]/div[2]/div[1]/p[1]/img/@src'

    def __init__(self):
        session = requests.session()
        session.keep_alive = False

        self._session = session

    def searchBrand(self, brandName):
        response = self._session.get(f'http://www.chinasspp.com/brand/bsearch.aspx?key={brandName}&cid=&s_btn=%CB%D1+%CB%F7')
        mainSource = self._getDataByRegular(response.text, self._MainPageSourceReg)
        if mainSource is None or len(mainSource) == 0:
            return None

        brandUrls = self._getDataByRegular(mainSource[0], self._ItemsUrlReg)

        if brandUrls is None or len(brandUrls) == 0:
            return None

        result = []
        for url in brandUrls:
            info = self.getItemInfo(url)
            if '查询失败' not in info['name']:
                result.append(info)

        return result

    def getPageItems(self, pageNum=1):
        response = self._session.get(f'http://www.chinasspp.com/brand/brands-{pageNum}.html')
        # print(response.text)
        mainSource = self._getDataByRegular(response.text, self._MainPageSourceReg)
        result = self._getDataByRegular(mainSource[0], self._ItemsUrlReg)

        return result

    def getLadiesPageItems(self, pageNum=1):
        response = self._session.get(f'http://www.chinasspp.com/brand/%E5%A5%B3%E8%A3%85%E5%93%81%E7%89%8C/{pageNum}/')
        # print(response.text)
        mainSource = self._getDataByRegular(response.text, self._ladiesMainPageSourceReg)
        result = self._getDataByRegular(mainSource[0], self._ItemsUrlReg)

        return result

    def getItemInfo(self, url):
        try:
            response = self._session.get(url)
            # print(response.text)
            name = self._getDataByXpath(response.text, self._itemNameXpath)[0]
            name = name.replace(' 品牌简介', '')
            name = name.replace(' 品牌动态', '')
            introduceTemp = self._getDataByXpath(response.text, self._itemIntroduceXpath)
            logo = self._getDataByXpath(response.text, self._brandLogoXpath)
            if len(logo) != 0:
                logo = logo[0]
            else:
                logo = ''

            introduce = ''
            if len(introduceTemp) == 0:
                for sentence in self._getDataByXpath(response.text, self._itemIntroduceSpareXpath):
                    introduce += sentence
            else:
                for sentence in introduceTemp:
                    introduce += sentence

            return {
                'name': name.replace(' 品牌介绍', ''),
                'introduce': introduce,
                'logo': logo
            }
        except requests.exceptions.ConnectionError:
            return {
                'name': '查询失败',
                'introduce': '查询失败',
                'logo': '查询失败'
            }

    def _getDataByRegular(self, pageSource, RegularString):
        result = re.findall(RegularString, pageSource)
        dedupResult = list(set(result))
        dedupResult.sort(key=result.index)
        return dedupResult

    def _getDataByXpath(self, pageSource, xpath):
        e = etree.HTML(pageSource)
        return e.xpath(xpath)