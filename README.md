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
