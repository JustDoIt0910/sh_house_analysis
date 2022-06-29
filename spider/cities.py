from conf import cfg
from utils.utils import Utils
import requests
from lxml import etree


class Cities:

    on_sail = 0

    done = 1

    def __init__(self):
        self.cities_info_urls = {}
        ua = Utils.get_ua()
        cities_page_url = cfg.cfg["application"]["cities_page_url"]
        headers = {
            "User-Agent": ua
        }
        cities_page = requests.get(cities_page_url, headers)
        doc = etree.HTML(cities_page.text, etree.HTMLParser())
        cities = doc.xpath("//div[@class='city_province']/ul/li/a")
        for c in cities:
            city_name = c.xpath("./text()")[0]
            city_info_url = c.xpath("./@href")[0]
            self.cities_info_urls[city_name] = city_info_url

    def get_url(self, city, typ):
        if typ == Cities.done:
            return self.cities_info_urls[city] + "chengjiao"
        else:
            return self.cities_info_urls[city] + "ershoufang"


if __name__ == '__main__':
    c = Cities()
    print(c.cities_info_urls)