import os
from pyecharts.charts import Bar, Bar3D, Line
from pyecharts.charts import Pie
from pyecharts import options as opts


class Draw:
    @staticmethod
    def pic1(data, city):

        y1 = data["dealCount"]
        y2 = data["onSailCount"]
        x = data["regions"]

        bar = Bar()
        # 设置x轴
        bar.add_xaxis(xaxis_data=x)
        # 设置y轴
        bar.add_yaxis(series_name='成交数量', y_axis=y1)
        bar.set_global_opts(title_opts=opts.TitleOpts(title=city + '各区二手房成交/在售数量'))
        bar.add_yaxis(series_name='在售数量', y_axis=y2)
        bar.set_global_opts(title_opts=opts.TitleOpts(title=city + '各区二手房成交/在售数量'))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        bar.render(path=cur_path + '/static/pic1.html')

    @staticmethod
    def pic2(data, city):

        labels = data["types"]
        num = data["dproportions"]
        c = Pie()
        c.add(city + "成交二手房户型占比", [list(z) for z in zip(labels, num)])  # 设置圆环的粗细和大小
        c.set_global_opts(title_opts=opts.TitleOpts(title=city + "成交二手房户型占比"))
        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        c.render(path=cur_path + '/static/pic21.html')

        num = data["oproportions"]
        c = Pie()
        c.add(city + "在售二手房户型占比", [list(z) for z in zip(labels, num)])  # 设置圆环的粗细和大小
        c.set_global_opts(title_opts=opts.TitleOpts(title=city + "在售二手房户型占比"))
        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        c.render(path=cur_path + '/static/pic22.html')

    @staticmethod
    def pic3(data, city):

        y1 = data["dealAvg"]
        y2 = data["onSailAvg"]
        x = data["regions"]

        bar = Bar()
        # 设置x轴
        bar.add_xaxis(xaxis_data=x)
        # 设置y轴
        bar.add_yaxis(series_name='成交', y_axis=y1, itemstyle_opts=opts.ItemStyleOpts(color='green'))
        bar.set_global_opts(title_opts=opts.TitleOpts(title=city + '各区成交二手房平均单价'))
        bar.add_yaxis(series_name='在售', y_axis=y2, itemstyle_opts=opts.ItemStyleOpts(color='blue'))
        bar.set_global_opts(title_opts=opts.TitleOpts(title=city + '各区在售二手房平均单价'))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        bar.render(path=cur_path + '/static/pic3.html')

    @staticmethod
    def pic4(data):

        y1 = data["onSailAvg"]
        y2 = data["dealAvg"]
        x = data["cities"]

        bar = Bar()
        # 设置x轴
        bar.add_xaxis(xaxis_data=x)
        # 设置y轴
        bar.add_yaxis(series_name='成交', y_axis=y2, itemstyle_opts=opts.ItemStyleOpts(color='blue'))
        bar.set_global_opts(title_opts=opts.TitleOpts(title='各城市在售/成交二手房平均单价'))
        bar.add_xaxis(xaxis_data=x)
        # 设置y轴
        bar.add_yaxis(series_name='在售', y_axis=y1, itemstyle_opts=opts.ItemStyleOpts(color='yellow'))
        bar.set_global_opts(title_opts=opts.TitleOpts(title='各城市在售/成交二手房平均单价'))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        bar.render(path=cur_path + '/static/pic4.html')

    @staticmethod
    def pic5(ranges, data, city):

        labels = []
        for r in ranges:
            labels.append(str(r[0]) + "~" + str(r[1]) + "平米")
        labels.append("其他")
        num = data
        c = Pie()
        c.add(city + "在售二手房不同面积占比", [list(z) for z in zip(labels, num)])  # 设置圆环的粗细和大小
        c.set_global_opts(title_opts=opts.TitleOpts(title=city + "在售不同面积占比"))
        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
        # 生成html文件
        cur_path = os.path.dirname(__file__)
        c.render(path=cur_path + '/static/pic5.html')

    @staticmethod
    def pic6(data):
        x_axis = data["face"]
        y_axis = data["floor"]
        bar = []
        for d in data["data"]:
            bar.append([int(d[0]), int(d[1]), d[2]])
        c = (
            Bar3D(init_opts=opts.InitOpts(width="900px", height="600px"))
                .add(
                series_name="",
                data=bar,
                xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x_axis),
                yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y_axis),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            ).set_global_opts(
                title_opts=opts.TitleOpts("城市房价和楼层，朝向关系"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=120000,
                    range_color=[
                        "#313695",
                        "#4575b4",
                        "#74add1",
                        "#abd9e9",
                        "#e0f3f8",
                        "#ffffbf",
                        "#fee090",
                        "#fdae61",
                        "#f46d43",
                        "#d73027",
                        "#a50026",
                    ],
                )
            )
        )
        cur_path = os.path.dirname(__file__)
        c.render(path=cur_path + '/static/pic6.html')

    @staticmethod
    def pic7(data, city):
        x = data["date"]
        y = data["avgPrice"]

        line = (
            Line()
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
                .add_xaxis(xaxis_data=x)
                .add_yaxis(
                series_name=city + "房价走势图",
                y_axis=y,
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        cur_path = os.path.dirname(__file__)
        line.render(path=cur_path + '/static/pic7.html')

    @staticmethod
    def predict(span, w1, w2, w3):
        x = []
        y = []
        for i in range(span):
            x.append(i)
        for i in x:
            y.append(w3 * i ** 2 + w2 * i + w1)

        line = (
            Line()
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
                .add_xaxis(xaxis_data=x)
                .add_yaxis(
                series_name="基本折线图",
                y_axis=y,
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        cur_path = os.path.dirname(__file__)
        line.render(path=cur_path + '/static/predict.html')



