## 项目结构简介

#### 项目完成的时间比较紧，但是本着模块间松耦合的理念，还是基本使用了前后端分离的结构。后端使用springboot，负责数据的查询和处理，前端是相对于后端而言的，使用flask负责数据可视化。爬虫脚本独立于二者，可以由springboot进行定时调用。

- spider - 爬虫脚本，负责爬取链家网二手房数据
	- conf - 项目的全局配置, config.yaml 里定义爬取过程中的 url 地址和自己的用户名密码
	- cities.py - 爬取每个城市对应子域名
	- cas - cas模拟登录模块，链家的二手房成交信息需要登录才能获取。其采用cas单点登录，密码使用 rsa2 和 rsa 加密隔天轮换
	- utils - 工具包，包含从 UA 池中获取随机 User-Agent 的方法，操作数据库的方法。
	- spider.py - 爬虫主文件，根据城市，地区爬取相应数据, 存入mysql
	- UA.txt - UA 池，反反爬
	- sql/table.sql - 建表脚本
- sh_house_backend - 系统后端
- sh_house_frontend - 系统前端(可视化部分)
	- static - 静态图片，资源和使用 pyecharts 动态绘制出的可视化图
	- template - 模板
	- app.py - app
	- draw.py - 各种画图函数
	
[部署地址](http://asilentboy.cn:5000)

![img1](https://github.com/JustDoIt0910/MarkDownPictures/blob/main/sh_house1.jpg)
![img2](https://github.com/JustDoIt0910/MarkDownPictures/blob/main/sh_house2.jpg)
![img3](https://github.com/JustDoIt0910/MarkDownPictures/blob/main/sh_house3.jpg)
![img4](https://github.com/JustDoIt0910/MarkDownPictures/blob/main/sh_house4.jpg)
![img5](https://github.com/JustDoIt0910/MarkDownPictures/blob/main/sh_house5.jpg)

#### TODO
- 使用配置文件配置要爬取的城市
- 给后端加入redis缓存
