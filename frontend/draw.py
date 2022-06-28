import base64

import matplotlib.pyplot as plt
import io


class Draw:
    @staticmethod
    def pic1(data):
        img = io.BytesIO()
        y = data["dealCount"]
        x = data["regions"]
        # 解决中文显示问题
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

        plt.title("保定各区二手房成交数量")
        plt.bar(x, y)
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode()

    @staticmethod
    def pic2(data):
        img = io.BytesIO()

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

        labels = data["types"]
        sizes = data["proportions"]
        plt.title("上海成交二手房户型占比")
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode()

    @staticmethod
    def pic3(data):
        img = io.BytesIO()
        y = data["dealAvg"]
        x = data["regions"]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.title("保定各区成交二手房平均单价")
        plt.bar(x, y)
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode()

    @staticmethod
    def pic4(data):
        img = io.BytesIO()
        y = data["dealAvg"]
        x = data["cities"]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.title("上海，济南成交二手房平均单价")
        plt.bar(x, y)
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode()

    @staticmethod
    def pic5(ranges, data):
        img = io.BytesIO()

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        labels = []
        for r in ranges:
            labels.append(str(r[0]) + "~" + str(r[1]) + "平米")
        labels.append("其他")
        sizes = data
        plt.title("济南在售二手房不同面积占比")
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode()
