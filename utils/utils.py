from conf import cfg
import random


class Utils:
    ua_pool = []

    @classmethod
    def load(cls):
        print("read UA.txt")
        ua_pool_path = cfg.cfg["application"]["ua_pool"]
        with open(ua_pool_path, "r") as f:
            for line in f:
                cls.ua_pool.append(line[:-1])

    @classmethod
    def get_ua(cls):
        index = random.randint(0, len(cls.ua_pool) - 1)
        return cls.ua_pool[index]


if __name__ == '__main__':
    utils = Utils()
