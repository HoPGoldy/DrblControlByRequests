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

    接受一个Drbl支持的word模板，并将其上传到指定的类型领域中
    
    参数：
    
        wordPath(字符串) - 需要上传的word文档路径
        
        importType(整形) - 导入到哪个类型，如101为新有好货（默认）
    

4. **importImg(imgPath)**

    将提供的文件上传至Drbl，若上传成功则返回其url
    
    参数：
        
        imgPath(字符串) - 需要上传的图片路径
    
    返回值：
    
        - 上传成功返回其url
        
        - 上传失败返回None

5. **getItemInfo(itemUrl)**

    获取提供的商品的主要信息
    
    参数：
    
        itemUrl - 想要查询的商品url
    
    返回值：
    
        - 查询成功返回一个包含信息的字典，结构如下
            {
            'title': 商品标题
            'isAdded': 该商品是否被添加，是则为True
            'industry': 商品类别
            'url': 商品的短链接
            'id': 商品id
            'img': 商品封面图url
            'shopTitle': 店铺名
            'shopUrl': 店铺url
            }
            
        - 查询失败则返回None
