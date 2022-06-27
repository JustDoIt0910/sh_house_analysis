import pymysql
from utils import Utils
import datetime

if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306,
                           user="root",
                           password="20010910cheng",
                           db="sh_house")

    # Utils.add_city(conn, "上海", 0, 0)
    # print(Utils.get_city_id(conn, "上海"))

    # Utils.update_city(conn, "杭州", onsail=100, deal=200)

    # Utils.add_region(conn, "上海", "浦东", 0, 0)
    # print(Utils.get_region_id(conn, "浦东"))

    # Utils.update_region(conn, "浦东", onsail=1, deal=2)

    # cid = Utils.get_city_id(conn, "上海")
    # rid = Utils.get_region_id(conn, "浦东")
    # Utils.add_info(conn, cid, rid, 1, "房名", "户型", 200, 100000, 100, "20220201")

    # print(Utils.check_city_exist(conn, "济南"))