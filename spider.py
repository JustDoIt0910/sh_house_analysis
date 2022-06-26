from cities import Cities
from cas.cas_login import Cas
import requests
from lxml import etree
from utils import Utils
import csv


class Spider:

    def __init__(self):
        self.cities = Cities()
        self.cas = Cas()

    def get(self, city, area, typ):
        if typ == Cities.on_sail:
            return self.get_on_sail(city, area)
        else:
            return self.get_deal(city, area)

    def get_deal(self, city, area):
        info_url = self.cities.get_url(city, Cities.done)
        cookie = self.cas.login()

        ua = Utils.get_ua()
        headers = {
            "User-Agent": ua
        }

        data = requests.get(info_url, cookies=cookie, headers=headers).text
        doc = etree.HTML(data, etree.HTMLParser())

        if area != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(area, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            region_info_url = info_url + "/" + suffix + "/"
            data = requests.get(region_info_url, headers=headers, cookies=cookie).text
            doc = etree.HTML(data, etree.HTMLParser())

        info_list = doc.xpath("//ul[@class='listContent']/li")

        with open("data.csv", "w+") as f:
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

    def get_on_sail(self, city, area):
        info_url = self.cities.get_url(city, Cities.on_sail)

        ua = Utils.get_ua()
        headers = {
            "User-Agent": ua
        }

        data = requests.get(info_url, headers=headers).text
        doc = etree.HTML(data, etree.HTMLParser())
        if area != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(area, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            region_info_url = info_url + "/" + suffix + "/"
            print(region_info_url)
            data = requests.get(region_info_url, headers=headers).text
            print(data)
            doc = etree.HTML(data, etree.HTMLParser())

        info_list = doc.xpath("//ul[@class='sellListContent']/li")

        with open("data.csv", "w+") as f:
            writer = csv.writer(f)
            for house in info_list:
                try:
                    name = house.xpath(".//div[@class='info clear']//div[@class='positionInfo']/a[1]/text()")[0]
                    house_info = house.xpath(".//div[@class='info clear']//div[@class='houseInfo']/text()")[0]
                    infos = house_info.split(" |")
                    house_type = infos[0]
                    area = infos[1]

                    price = house.xpath(".//div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span/text()")[0]
                    unitPrice = house.xpath(".//div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()")[0]
                    print(name, house_type, area, price, unitPrice)
                except:
                    continue

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


if __name__ == '__main__':
    s = Spider()
    s.get("上海", "浦东", Cities.done)
