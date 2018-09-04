# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 10:16
# @Author  : HoPGoldy

from Drbl import DrblControl
import os
import time
from Modules.DataFormater import *
from Brand import getBrandInfo, logoDownload, logoCreate
from setting import *


def clearPicfolder():
    if os.path.exists(PIC_FOLDER_PATH):
        files = os.listdir(PIC_FOLDER_PATH)
        for file in files:
            os.remove(f'{PIC_FOLDER_PATH}/{file}')
    else:
        os.mkdir(PIC_FOLDER_PATH)


def prepare():
    input('[系统] 请复制资源后回车')
    text = getClipBoardData()
    datas = formatDataByReg(text)

    while len(datas) == 0:
        input('[系统] 未发现资源，请重新输入')
        text = getClipBoardData()
        datas = formatDataByReg(text)
    print('[系统] 整理完成')

    if IS_GET_BRAND_INTRODUCE:
        print('\n[系统] 开始搜索品牌')
        for i in range(len(datas)):
            data = datas[i]
            brandIntroduce, logoUrl = getBrandInfo(data['brand'])
            if brandIntroduce is None:
                print(f'[品牌] ✗ 未找到{data["brand"]}')
                brandIntroduce = ' ' * MIN_ADDITION_NUM
            else:
                print(f'[品牌] ✓ 找到{data["brand"]}')

            logoPath = ''
            if IS_GET_BRAND_LOGO:
                if logoUrl is None or logoUrl == '':
                    logoPath = logoCreate(data['brand'], str(i))
                else:
                    logoPath = logoDownload(logoUrl, str(i))
            data['addition'].append({
                'title': '品牌介绍',
                'content': brandIntroduce,
                'brand': data['brand'],
                'logoPath': logoPath
            })

    show(datas)
    return datas


def update(datas):
    drbl = DrblControl()

    if drbl.login(USER_NAME, PASSWORD):
        print('[八斗] 登陆成功')
    else:
        print('[八斗] 登陆失败')
        return None

    for i in range(len(datas)):
        if drbl.addItem(datas[i]):
            print(f'[八斗] ✓ 第{i+1}条上传成功')
        else:
            print(f'[八斗] ✗ 第{i+1}条上传失败')
        time.sleep(1)


if __name__ == '__main__':
    clearPicfolder()

    datas = prepare()

    input('[系统] 按任意键开始上传：')
    update(datas)