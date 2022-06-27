import random
import os


class Utils:
    ua_pool = []

    @classmethod
    def load(cls):
        print("read UA.txt")
        root_path = os.path.join(os.path.dirname(__file__), "..")
        ua_pool_path = os.path.join(root_path, "UA.txt")
        with open(ua_pool_path, "r") as f:
            for line in f:
                cls.ua_pool.append(line)

    @classmethod
    def get_ua(cls):
        index = random.randint(0, len(cls.ua_pool) - 1)
        return cls.ua_pool[index]

    @classmethod
    def check_city_exist(cls, conn, name):
        sql = "SELECT id from t_cities WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                select_result = cursor.fetchall()
                return len(select_result) != 0
        except Exception as e:
            print(e)

    @classmethod
    def check_region_exist(cls, conn, name):
        sql = "SELECT id from t_regions WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                select_result = cursor.fetchall()
                return len(select_result) != 0
        except Exception as e:
            print(e)

    @classmethod
    def add_city(cls, conn, name, deal, on_sail):
        sql = "INSERT INTO t_cities (`name`, onsail, deal) " \
              "VALUES ('{0}','{1}', '{2}')".format(name, on_sail, deal)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()

    @classmethod
    def get_city_id(cls, conn, name):
        sql = "SELECT id FROM t_cities WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                select_result = cursor.fetchall()
                return select_result[0][0]
        except Exception as e:
            print(e)

    @classmethod
    def add_region(cls, conn, city_id, name, deal, on_sail):
        sql = "INSERT INTO t_regions (`name`, cityId, onsail, deal)" \
              " VALUES ('{0}', {1}, {2}, {3})".format(name, city_id, on_sail, deal)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()

    @classmethod
    def get_region_id(cls, conn, name):
        sql = "SELECT id FROM t_regions WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                select_result = cursor.fetchall()
                return select_result[0][0]
        except Exception as e:
            print(e)

    @classmethod
    def update_city(cls, conn, name, **kwargs):
        sql = "UPDATE t_cities SET "
        for field, value in kwargs.items():
            sql += "{0} = {1}, ".format(field, value)
        sql = sql[:-2] + " WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()

    @classmethod
    def update_region(cls, conn, name, **kwargs):
        sql = "UPDATE t_regions SET "
        for field, value in kwargs.items():
            sql += "{0} = {1}, ".format(field, value)
        sql = sql[:-2] + " WHERE `name` = '{0}'".format(name)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()

    @classmethod
    def add_info(cls, conn, city_id, region_id, is_deal,
                 name, h_type, area, total_price, unit_price, deal_time):
        sql = "INSERT INTO t_info " \
              "(`name`, deal, cityId, regionId, `type`, area, totalPrice, unitPrice, dealTime)" \
              " VALUES ('{0}', {1}, {2}, {3}, '{4}', {5}, {6}, {7}, '{8}')".format(
                name, is_deal, city_id, region_id, h_type, area, total_price, unit_price, deal_time
        )
        print(sql)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()

