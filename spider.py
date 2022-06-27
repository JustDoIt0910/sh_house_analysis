from cities import Cities
from cas.cas_login import Cas
import requests
from lxml import etree
from utils import Utils
import csv
import time
import random


class Spider:

    def __init__(self):
        self.cities = Cities()
        self.cas = Cas()

    def get(self, city, area, typ, pages, filename):
        if typ == Cities.on_sail:
            return self.get_on_sail(city, area, pages, filename)
        else:
            return self.get_deal(city, area, pages, filename)

    def get_deal(self, city, area, pages, filename):
        info_url = self.cities.get_url(city, Cities.done)
        cookie = self.cas.login()

        ua = Utils.get_ua()
        headers = {
            "User-Agent": ua
        }
        proxies = {
            "https": "124.226.194.135:808"
        }

        data = requests.get(info_url, cookies=cookie, headers=headers).text
        doc = etree.HTML(data, etree.HTMLParser())

        if area != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(area, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            info_url = info_url + "/" + suffix

        with open(filename, "a+") as f:
            for i in range(pages):
                print("--------正在爬取成交第{}页--------".format(i + 1))
                if not (area == "" and i == 0):
                    data = requests.get(info_url + "/pg" + str(i + 1), headers=headers, cookies=cookie).text
                    doc = etree.HTML(data, etree.HTMLParser())

                info_list = doc.xpath("//ul[@class='listContent']/li")
                writer = csv.writer(f)
                for deal in info_list:
                    try:
                        title = deal.xpath(".//div[@class='title']/a/text()")[0]
                        dealDate = deal.xpath(".//div[@class='dealDate']/text()")[0]
                        infos = title.split(" ")
                        totalPrice = deal.xpath(".//div[@class='totalPrice']/span/text()")[0]
                        unitPrice = deal.xpath(".//div[@class='unitPrice']/span/text()")[0]
                        infos.extend([totalPrice, unitPrice, dealDate])
                        print(infos)
                        writer.writerow(infos)
                    except:
                        continue
                time.sleep(random.randint(2, 5))

    def get_on_sail(self, city, area, pages, filename):
        info_url = self.cities.get_url(city, Cities.on_sail)

        ua = Utils.get_ua()
        headers = {
            "User-Agent": ua
        }
        proxies = {
            "https": "124.226.194.135:808"
        }

        data = requests.get(info_url, headers=headers).text
        doc = etree.HTML(data, etree.HTMLParser())
        if area != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(area, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            info_url = info_url + "/" + suffix
            data = requests.get(info_url, headers=headers).text
            doc = etree.HTML(data, etree.HTMLParser())

        with open(filename, "a+") as f:
            for i in range(pages):
                print("--------正在爬取在售第{}页--------".format(i + 1))
                if not (area == "" and i == 0):
                    data = requests.get(info_url + "/pg" + str(i + 1), headers=headers).text
                    doc = etree.HTML(data, etree.HTMLParser())

                info_list = doc.xpath("//ul[@class='sellListContent']/li")
                writer = csv.writer(f)
                for house in info_list:
                    try:
                        name = house.xpath(".//div[@class='info clear']//div[@class='positionInfo']/a[1]/text()")[0]
                        house_info = house.xpath(".//div[@class='info clear']//div[@class='houseInfo']/text()")[0]
                        infos = house_info.split(" |")
                        house_type = infos[0]
                        area = infos[1]

                        price = house.xpath(
                            ".//div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span/text()")[
                            0]
                        unitPrice = house.xpath(
                            ".//div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()")[0]
                        writer.writerow([name, house_type, area, price, unitPrice, None])
                        print(name, house_type, area, price, unitPrice)
                    except:
                        continue
                time.sleep(random.randint(2, 5))

    @staticmethod
    def get_regions(doc):
        region_list = doc.xpath("//div[@class='position']/dl/dd/div[@data-role='ershoufang']/div[1]/a")
        regions = {}
        for region in region_list:
            name = region.xpath("./text()")[0]
            href = region.xpath("./@href")[0]
            suffix = href.split("/")[2]
            regions[name] = suffix
        return regions

# 上海 杭州
# 济南
# 保定
# 开封


if __name__ == '__main__':
    csv_header = ["名称", "户型", "面积", "总价(万元)", "单价(元)", "成交日期"]
    s = Spider()

    # 爬上海
    filename = "shanghai.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    print("-----------获取上海成交二手房-------------")
    s.get("上海", "", Cities.done, 50, filename)
    print("-----------获取上海在售二手房-------------")
    s.get("上海", "", Cities.on_sail, 50, filename)

    # 爬杭州
    filename = "hangzhou.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    print("-----------获取杭州在售二手房-------------")
    s.get("杭州", "", Cities.on_sail, 100, filename)

    # 爬济南
    filename = "jinan.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    print("-----------获取济南成交二手房-------------")
    s.get("济南", "", Cities.done, 50, filename)
    print("-----------获取济南在售二手房-------------")
    s.get("济南", "", Cities.on_sail, 50, filename)

    # 爬保定
    filename = "baoding.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    print("-----------获取保定成交二手房-------------")
    s.get("保定", "", Cities.done, 50, filename)
    print("-----------获取保定在售二手房-------------")
    s.get("保定", "", Cities.on_sail, 50, filename)

    # 爬开封
    filename = "kaifeng.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
    print("-----------获取开封成交二手房-------------")
    s.get("开封", "", Cities.done, 50, filename)
    print("-----------获取开封在售二手房-------------")
    s.get("开封", "", Cities.on_sail, 50, filename)


