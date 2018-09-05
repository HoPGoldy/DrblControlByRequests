# DrblControlByRequests
基于requests库封装的网站https://drbl.daorc.com的主要操作

# 安装
1. 运行环境

请确保安装python3.6.2以上版本

2. 依赖

cd至根目录下键入如下命令来安装依赖

```pip3 install -r requirements.txt```

# 项目内容
本项目包含了Drbl的主要操作封装和一套完整的资源上传流程（包括一个332type的格式化器，一个用于查询品牌的chinasspp爬虫和生成临时logo的文字转图片脚本），主要结构如下：

Modules文件夹 - 引用的第三方文件

Brand.py - 封装了chinasspp爬虫，为项目提供需要的方法

**Drbl.py** - 主体文件，封装了drbl的主要操作

run.py - 上传流程的启动脚本

setting.py - 一些参数，包括登陆用的用户名和密码

# DrblControl
该类定义与Drbl.py文件夹中，以下为提供的方法功能

1. **login(userName, password)** 

    登陆Drbl，使用该类的其他所有方法之前均需进行登陆

    参数： 

        userName(字符串类型) 登陆用户名

        password(字符串类型) 登陆密码

    返回值：

        True - 登陆成功

        False - 登陆失败


2. **addItem(itemData)**

    接受一个标准的数据结构， 并将其上传到Drbl的新有好货
    
    参数：
    
        itemData(字典) - 需要上传的数据
    
    返回值：
        
        True - 上传成功

        False - 上传失败

3. **importWord(wordPath, importType)**

4. **importImg(imgPath)**

5. **getItemInfo(itemUrl)**
