# -*- coding: utf-8 -*-，

from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt
import io
import base64
import requests
from draw import Draw

app = Flask(__name__)


@app.route('/')
def build_plot():
    data = requests.get("http://192.168.3.13:9999/data/c1/保定").json()
    pic1 = Draw.pic1(data)

    data = requests.get("http://192.168.3.13:9999/data/c2/上海").json()
    pic2 = Draw.pic2(data)

    data = requests.get("http://192.168.3.13:9999/data/c3/保定").json()
    pic3 = Draw.pic3(data)

    param = {
        "cities": ["上海", "济南"]
    }
    data = requests.get("http://192.168.3.13:9999/data/c4", params=param).json()
    pic4 = Draw.pic4(data)

    ranges = [
            [20, 80],
            [80, 150],
            [150, 200]
        ]
    post_data = {
        "city": "济南",
        "areaRanges": ranges
    }
    data = requests.post("http://192.168.3.13:9999/data/c5", json=post_data).json()
    pic5 = Draw.pic5(ranges, data)

    return render_template('index.html', pic1=pic1, pic2=pic2, pic3=pic3, pic4=pic4, pic5=pic5)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/analyse')
def analyze():
    return render_template('analyse.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/typo')
def typo():
    return render_template('typo.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
