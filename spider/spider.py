import pymysql

from cities import Cities
from cas.cas_login import Cas
import requests
from lxml import etree
from utils import Utils
import csv
import time
import random
from conf import cfg


class Spider:

    def __init__(self):
        self.cities = Cities()
        self.cas = Cas()
        self.mysql_conn = None

    def get(self, city, region, typ, pages):
        t = "在售" if typ == Cities.on_sail else "成交"
        print("-----------获取{0}{1}{2}二手房-------------".format(city, region, t))
        self.mysql_conn = pymysql.connect(host='127.0.0.1', port=3306,
                                          user=cfg.cfg["mysql"]["username"],
                                          password=cfg.cfg["mysql"]["password"],
                                          db=cfg.cfg["mysql"]["dbName"])
        if typ == Cities.on_sail:
            self.get_on_sail(self.mysql_conn, city, region, pages)
        else:
            self.get_deal(self.mysql_conn, city, region, pages)
        self.mysql_conn.close()

    def get_deal(self, conn, city, region, pages):

        if not Utils.check_city_exist(conn, city):
            Utils.add_city(conn, city, 0, 0)
        city_id = Utils.get_city_id(conn, city)
        region_id = 0
        if region != "":
            if not Utils.check_region_exist(conn, region):
                Utils.add_region(conn, city_id, region, 0, 0)
            region_id = Utils.get_region_id(conn, region)

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
        try:
            city_house_count = doc.xpath("//div[@class='total fl']/span/text()")[0]
        except:
            city_house_count = 0
            print("无二手房数量数据")

        if region != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(region, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            info_url = info_url + "/" + suffix
        else:
            Utils.update_city(conn, city, deal=city_house_count)

        for i in range(pages):
            print("--------正在爬取成交第{}页--------".format(i + 1))
            if not (region == "" and i == 0):
                data = requests.get(info_url + "/pg" + str(i + 1), headers=headers, cookies=cookie).text
                doc = etree.HTML(data, etree.HTMLParser())
                if i == 0:
                    try:
                        region_house_count = doc.xpath("//div[@class='total fl']/span/text()")[0]
                        Utils.update_region(conn, region, deal=region_house_count)
                    except:
                        print("无二手房数量数据")

            info_list = doc.xpath("//ul[@class='listContent']/li")

            for deal in info_list:
                try:
                    title = deal.xpath(".//div[@class='title']/a/text()")[0]
                    dealDate = deal.xpath(".//div[@class='dealDate']/text()")[0]
                    infos = title.split(" ")
                    totalPrice = deal.xpath(".//div[@class='totalPrice']/span/text()")[0]
                    unitPrice = deal.xpath(".//div[@class='unitPrice']/span/text()")[0]
                    floorR = deal.xpath(".//div[@class='positionInfo']/text()")[0]
                    faceR = deal.xpath(".//div[@class='houseInfo']/text()")[0]
                    face = faceR.split("|")[0].strip().split(" ")[0]
                    floor = Utils.get_floor(floorR)
                    if floor is None:
                        floor = 0

                    infos.extend([totalPrice, unitPrice, dealDate, floor, face])
                    print(infos)
                    # writer.writerow(infos)
                    Utils.add_info(conn, city_id, region_id, 1, infos[0],
                                   infos[1], infos[2][:-2], infos[3], infos[4],
                                   infos[5].replace(".", ""), infos[6], infos[7])

                except:
                    continue
            time.sleep(random.randint(2, 5))

    def get_on_sail(self, conn, city, region, pages):

        if not Utils.check_city_exist(conn, city):
            Utils.add_city(conn, city, 0, 0)
        city_id = Utils.get_city_id(conn, city)
        region_id = 0
        if region != "":
            if not Utils.check_region_exist(conn, region):
                Utils.add_region(conn, city_id, region, 0, 0)
            region_id = Utils.get_region_id(conn, region)

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
        try:
            city_house_count = doc.xpath("//h2[@class='total fl']/span/text()")[0]
        except:
            city_house_count = 0
            print("无二手房数量数据")

        if region != "":
            regions = Spider.get_regions(doc)
            suffix = regions.get(region, "")
            if suffix == "":
                print("未查询到该区数据")
                return
            info_url = info_url + "/" + suffix
        else:
            Utils.update_city(conn, city, onsail=city_house_count)

        for i in range(pages):
            print("--------正在爬取在售第{}页--------".format(i + 1))

            if not (region == "" and i == 0):
                data = requests.get(info_url + "/pg" + str(i + 1), headers=headers).text
                doc = etree.HTML(data, etree.HTMLParser())
                if i == 0:
                    try:
                        region_house_count = doc.xpath("//h2[@class='total fl']/span/text()")[0]
                        Utils.update_region(conn, region, onsail=region_house_count)
                    except:
                        print("无二手房数量数据")

            info_list = doc.xpath("//ul[@class='sellListContent']/li")
            for house in info_list:
                try:
                    name = house.xpath(".//div[@class='info clear']//div[@class='positionInfo']/a[1]/text()")[0]
                    house_info = house.xpath(".//div[@class='info clear']//div[@class='houseInfo']/text()")[0]
                    infos = house_info.split(" |")
                    house_type = infos[0]
                    area = infos[1][:-2]

                    price = house.xpath(
                        ".//div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span/text()")[
                        0]
                    unitPrice = house.xpath(
                        ".//div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()")[
                                    0][:-3]
                    unitPrice = unitPrice.replace(",", "")
                    hi = house.xpath(".//div[@class='info clear']//div[@class='houseInfo']/text()")[0]
                    face = hi.split("|")[2].strip().split(" ")[0]
                    floor = Utils.get_floor(hi)
                    if floor is None:
                        floor = 0

                    # writer.writerow([region, name, house_type, area, price, unitPrice, None])
                    print(region, name, house_type, area, price, unitPrice, floor, face)
                    Utils.add_info(conn, city_id, region_id, 0, name, house_type,
                                   area, price, unitPrice, "00000000", floor, face)

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
    csv_header = ["地区", "名称", "户型", "面积", "总价(万元)", "单价(元)", "成交日期"]
    s = Spider()

    # s.get("济南", "历下", Cities.done, 20)
    # s.get("济南", "莱芜区", Cities.done, 20)
    # s.get("济南", "市中", Cities.done, 20)
    # s.get("济南", "天桥", Cities.done, 20)
    # s.get("济南", "历城", Cities.done, 20)
    # s.get("济南", "槐荫", Cities.done, 20)
    # s.get("济南", "高新", Cities.done, 20)
    #
    # s.get("济南", "历下", Cities.on_sail, 20)
    # s.get("济南", "莱芜区", Cities.on_sail, 20)
    # s.get("济南", "市中", Cities.on_sail, 20)
    # s.get("济南", "天桥", Cities.on_sail, 20)
    # s.get("济南", "历城", Cities.on_sail, 20)
    # s.get("济南", "槐荫", Cities.on_sail, 20)
    # s.get("济南", "高新", Cities.on_sail, 20)


    # s.get("上海", "浦东", Cities.done, 20)
    # s.get("上海", "闵行", Cities.done, 20)
    # s.get("上海", "宝山", Cities.done, 20)
    # s.get("上海", "徐汇", Cities.done, 20)
    # s.get("上海", "普陀", Cities.done, 20)
    # s.get("上海", "杨浦", Cities.done, 20)
    #
    # s.get("上海", "浦东", Cities.on_sail, 20)
    # s.get("上海", "闵行", Cities.on_sail, 20)
    # s.get("上海", "宝山", Cities.on_sail, 20)
    # s.get("上海", "徐汇", Cities.on_sail, 20)
    # s.get("上海", "普陀", Cities.on_sail, 20)
    # s.get("上海", "杨浦", Cities.on_sail, 20)


    # s.get("杭州", "西湖", Cities.on_sail, 10)
    # s.get("杭州", "钱塘区", Cities.on_sail, 10)
    # s.get("杭州", "临平区", Cities.on_sail, 10)
    # s.get("杭州", "下城", Cities.on_sail, 10)
    # s.get("杭州", "拱墅", Cities.on_sail, 10)
    # s.get("杭州", "上城", Cities.on_sail, 10)
    # s.get("杭州", "滨江", Cities.on_sail, 10)
    # s.get("杭州", "余杭", Cities.on_sail, 10)
    # s.get("杭州", "萧山", Cities.on_sail, 10)
    #
    #
    # s.get("保定", "涞水", Cities.done, 10)
    # s.get("保定", "涿州", Cities.done, 10)
    # s.get("保定", "易县", Cities.done, 10)
    # s.get("保定", "高碑店", Cities.done, 10)
    # s.get("保定", "竞秀区", Cities.done, 10)
    #
    # s.get("保定", "涞水", Cities.on_sail, 10)
    # s.get("保定", "涿州", Cities.on_sail, 10)
    # s.get("保定", "易县", Cities.on_sail, 10)
    # s.get("保定", "高碑店", Cities.on_sail, 10)
    # s.get("保定", "竞秀区", Cities.on_sail, 10)
    #
    # s.get("开封", "龙亭区", Cities.on_sail, 3)
    # s.get("开封", "杞县", Cities.on_sail, 3)
    # s.get("开封", "兰考县", Cities.on_sail, 3)
    # s.get("开封", "通许县", Cities.on_sail, 3)

    s.get("上海", "", Cities.done, 50)
    s.get("上海", "", Cities.on_sail, 50)

    #
    # s.get("杭州", "", Cities.on_sail, 50)
    #
    # s.get("济南", "", Cities.on_sail, 50)
    # s.get("济南", "", Cities.done, 50)
    #
    # s.get("保定", "", Cities.on_sail, 50)
    # s.get("保定", "", Cities.done, 50)
    #
    # s.get("开封", "", Cities.on_sail, 50)