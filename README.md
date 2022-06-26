## 项目结构简介

- conf - 项目的全局配置, config.yaml 里定义爬取过程中的 url 地址和自己的用户名密码
- cities.py - 爬取每个城市对应子域名
- cas - cas模拟登录模块，链家的二手房成交信息需要登录才能获取。其采用cas单点登录，密码使用 rsa2 加密
- utils - 工具包，目前只有一个从 UA 池中获取随机 User-Agent 的方法
- spider.py - 爬虫主文件，根据城市，地区爬取相应数据, 暂存入csv
- UA.txt - UA 池，反爬

### 目前实现根据城市爬取链家的在售或已交易的二手房信息，并保存为 csv。