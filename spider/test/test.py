import pymysql
from utils import Utils
import datetime
import re


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306,
                           user="root",
                           password="20010910cheng",
                           db="sh_house")

    sql = "select unitPrice from t_info where regionId = 12 and deal = 1 and `type` = '3室2厅' and floor = 6 order by dealTime"
    with conn.cursor() as c:
        c.execute(sql)
        res = c.fetchall()
    conn.commit()
    y = []
    x = []

    for i, p in enumerate(res):
        y.append(p[0])
        x.append(i)
    import matplotlib.pyplot as plt

    plt.scatter(x, y)
    plt.show()



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

    # try:
    #     pattern = re.compile(r".*?\(.*?([0-9]+).*?\).*?")
    #     print(pattern.match("中楼").group(1))
    # except:
    #     print("不匹配")
    #
    # print("暂无数据".split("|")[0].strip().split(" ")[0])
    #
    # hi = "3室1厅 | 71.39平米 | 西南 | 精装 | 中楼层(共32层) | 2107年建 | 塔楼"
    # face = hi.split("|")[2].strip().split(" ")[0]
    # floor = Utils.get_floor(hi)
    # print(face, floor)

