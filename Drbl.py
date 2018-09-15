# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 10:13
# @Author  : HoPGoldy

import requests
from lxml import etree
import json
import re
import time


class DrblControl():
    baseUrl = 'https://drbl.daorc.com/'
    loginUrl = 'https://drbl.daorc.com/user_jsonLogin.action'
    addItemUrl = 'https://drbl.daorc.com/data_saveData.action'#http://httpbin.org/post'
    getRecommendUrl = 'https://drbl.daorc.com/main_welcome2.action?set=11'
    seachItemUrl = 'https://drbl.daorc.com/commoditylibrary_itemcCheck.action'
    checkItemUrl = 'https://drbl.daorc.com/commoditylibrary_getCommodityDetailByUrl.action'
    importWordUrl = 'https://drbl.daorc.com/$%7BcontextPath%7D/wordimport_importWord.action'
    importImgUrl = 'https://drbl.daorc.com/picturelibrary_uploadBatch.action?itemId='
    getBrandListUrl = 'https://drbl.daorc.com/data_queryDataListToJSON.action'
    getBrandUrl = 'https://drbl.daorc.com/brands_getBrands.action'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
    checkItemFiledicid = '1504322571727'
    _session = None
    _loginToken = None

    def __init__(self):
        session = requests.session()
        response = session.get(self.baseUrl)
        loginToken = self._getDataByRegular(response.text, '(?<="token":")[\w]*(?="})')[0]
        # print(f'token的值为：{loginToken}')

        self._session = session
        self._loginToken = loginToken

    # 登陆
    def login(self, userName, password):
        fromData = {
            'loginName': userName,
            'password': password,
            'checkyzm': '0',
            'struts.token.name': 'token',
            'token': self._loginToken}

        response = self._session.post(self.loginUrl, data=fromData)
        returnJson = json.loads(response.text)
        # print('登陆返回的json为：' + str(returnJson))
        if returnJson['status'] == '1':
            return True
        else:
            return False

    # 新建好货
    def addItem(self, itemData=None):
        # 获取宝贝id
        itemInfo = self.getItemInfo(itemData['url'])
        if itemInfo == None:
            return None

        # 获取页面上的id信息
        response = self._session.get('https://drbl.daorc.com/data_addData.action?fileTypeId=101&tableFlag=WJ&isopen=0')
        temp_f_dataId = self._getDataByXpath(response.text, '//*[@id="temp_f_dataId"]/@value')[0]
        temp_f_curruserid = self._getDataByXpath(response.text, '//*[@id="temp_f_curruserid"]/@value')[0]

        # 构造详情页数据
        detailData = [{
            "coverUrl": itemInfo['img'],
            "title": itemData['title'],
            "itemId": itemInfo['id'],
            "supplement": []
        }]
        detailData = json.dumps(detailData)

        # 构造亮点数据
        longHighLight = ''
        shortHighLight = ''
        for i in range(len(itemData['longHighLight'])):
            longHighLight += itemData['longHighLight'][i]
            if i < (len(itemData['longHighLight']) - 1):
                longHighLight += '@,@'
        for i in range(len(itemData['shortHighLight'])):
            shortHighLight += itemData['shortHighLight'][i]
            if i < (len(itemData['shortHighLight']) - 1):
                shortHighLight += '@,@'

        # 构造补充数据
        additionData = []
        for addition in itemData['addition']:
            temp = {
                "title": addition['title'],
                "describe": addition['content'],
                "url": "/static/image/select.jpg",
                "type": "2",
                "w": 380,
                "h": 380
            }
            if 'brand' in addition:
                temp.update({'bname': addition['brand']})
                logoUrl = self.importImg(addition['logoPath'])
                temp['url'] = logoUrl
            additionData.append(temp)

        additionData = json.dumps(additionData)

        # 构造表单数据
        fromData = {
            'fileTypeId': 101,
            'tableFlag': 'WJ',
            't_fileTypeId': None,
            't_tableFlag': None,
            'ajId': None,
            'id': None,
            'temp_f_dataId': temp_f_dataId,
            'temp_f_rowIds': None,
            'temp_f_updateFileTypeId': None,
            'temp_f_iszujuan': None,
            'temp_f_jnIds': None,
            'temp_f_isopen': 0,
            'temp_f_curruserid': temp_f_curruserid,
            'temp_f_newAutostatus': None,
            'CHANNELID': 101,
            'BADGE': 0,
            'RWID': None,
            'ITEMID': itemInfo['id'],
            'CLASSIFYID': itemData['category'],
            'temp_f_RWID': None,
            'COMMODITYLIBRARYID': detailData,
            'TITLE': itemData['title'],
            'FORTUNATELY': longHighLight,
            'FORTUNATELY_SHORT': shortHighLight,
            'COVERIMG':  additionData,
            'gradeone': itemData['targetPeople'][0],
            'gradetwo': itemData['targetPeople'][1],
            'MAINPEOPLE': itemData['targetPeople'][1],
            'TEMP_F_DRAFTS': 1}

        response = self._session.post(self.addItemUrl, data=fromData, headers=self.headers)
        # print(response.text)
        return True

    def getBrand(self, startPage=1, endPage=2, fileTypeId=123):
        payload = {
            'fileTypeId': fileTypeId,
            'tableFlag': 'WJ',
            'pageInfo': 'STATUS@@1@@2@_@',
            'isSeacher': 1,
            'offset': 32,
            'limit': 8,
            'order': 'asc',
            'page': 5,
            'rows': 8,
        }
        brandIDs = []
        for i in range(startPage, endPage+1):
            # print(f'正在获取第{i}页的品牌')
            payload['page'] = i
            payload['offset'] = 8 * (i - 1)
            response = self._session.get(self.getBrandListUrl, params=payload)
            returnJson = json.loads(response.text)
            for row in returnJson['rows']:
                brandIDs.append(row['ID'])
            time.sleep(1)

        fromData = {
            'id': None,
            'fileTypeId': 123
        }
        brandData = []
        for index, brandID in enumerate(brandIDs):
            fromData['id'] = brandID
            response = self._session.post(self.getBrandUrl, fromData)
            returnJson = json.loads(response.text)

            print(f'[{index + 1}] {returnJson["data"]["brandsVoList"]}')
            brandData.append(returnJson['data']['brandsVoList'])
            time.sleep(1)

        brands = []
        for data in brandData:
            dataTemp = []
            for brand in data:
                logoData = json.loads(brand['brandsLogo'])
                temp = {
                    'brand': brand['brandsName'],
                    'describe': brand['brandsDescribe'],
                    'logo': logoData[0]['url']
                }
                dataTemp.append(temp)
            brands.append(dataTemp)

        return brands


    # 获取推荐
    def getRecommend(self, itemUrl):
        fromData = {
            'url': itemUrl,
            'title': None
        }
        response = self._session.post(self.getRecommendUrl, data=fromData)
        returnJson = json.loads(response.text)

        recommends = []
        for item in returnJson['data']:
            if len(item['summary']) >= 60:
                recommends.append((item["title"], item['summary']))
        return recommends

    # 从word导入条目
    def importWord(self, wordPath, importType='101'):
        pathFilter = wordPath.split('/')
        wordName = pathFilter[len(pathFilter)-1]

        files = {
            'chanmeId': (None, importType),
            'uploadFile': (wordName, open(wordPath, 'rb'), 'application/msword')
         }
        response = self._session.post(self.importWordUrl, files=files)
        print(response.text)

    # 上传一张图片
    def importImg(self, imgPath):
        pathFilter = imgPath.split('/')
        imgNmae = pathFilter[len(pathFilter) - 1]

        files = {'uploadFile': (imgNmae, open(imgPath, 'rb'), 'Content-Type: image/jpeg')}
        response = self._session.post(self.importImgUrl, files=files)
        returnJson = json.loads(response.text)
        return returnJson['path']

    # 搜索商品
    def searchItem(self, itemUrl):
        fromData = {'url': itemUrl}

        response = self._session.post(self.seachItemUrl, fromData)
        print(response.text)

    # 获取商品信息
    def getItemInfo(self, itemUrl):
        fromData = {
            'url': itemUrl,
            'filetypeidxp': None,
            'filedicid': self.checkItemFiledicid,
            'dataId': None, }

        response = self._session.post(self.checkItemUrl, fromData)

        returnJson = json.loads(response.text)
        if len(returnJson['data']) < 1:
            print('[八斗] 商品不存在或已下架 ' + itemUrl)
            return None

        mainInfo = returnJson['data'][0]
        return {
            'title': mainInfo.get('title'),
            'isAdded': 'alertmsg' in returnJson,
            'industry': mainInfo.get('industry'),
            'url': mainInfo.get('item_url'),
            'id': mainInfo.get('num_iid'),
            'img': mainInfo.get('pict_url'),
            'shopTitle': mainInfo.get('shopTitle'),
            'shopUrl': mainInfo.get('shopUrl')
        }

    def _getDataByXpath(self, pageSource, xpath):
        e = etree.HTML(pageSource)
        return e.xpath(xpath)

    def _getDataByRegular(self, pageSource, RegularString):
        result = re.findall(RegularString, pageSource)
        dedupResult = list(set(result))
        dedupResult.sort(key=result.index)
        return dedupResult
