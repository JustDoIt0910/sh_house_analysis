import yaml
import os


class Cfg:
    def __init__(self):
        cur_path = os.path.dirname(__file__)
        cfg_path = os.path.join(cur_path, "config.yaml")
        cfg_file = open(cfg_path, "r")
        c = yaml.load(cfg_file.read())
        self.cfg = c


cfg = Cfg()
