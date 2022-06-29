# -*- coding: utf-8 -*-，
import datetime
import time

from flask import Flask, url_for, request
from flask import render_template
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import requests
from draw import Draw
from flask import redirect

app = Flask(__name__)

api_url = "http://asilentboy.cn:9999"

cityOptions = []


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def build_plot():
    global cityOptions
    cityOptions = requests.get(api_url + "/data/cityOptions").json()
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/analyse/<int:chart>/<string:city>/<int:is_deal>')
def analyze(chart, city, is_deal):
    data = requests.get(api_url + "/data/c1/" + city).json()
    Draw.pic1(data, city)

    data = requests.get(api_url + "/data/c2/" + city).json()
    Draw.pic2(data, city)

    data = requests.get(api_url + "/data/c3/" + city).json()
    Draw.pic3(data, city)

    param = {
        "cities": ["上海", "杭州", "济南", "保定", "开封"]
    }
    data = requests.get(api_url + "/data/c4", params=param).json()
    Draw.pic4(data)

    ranges = [
        [20, 80],
        [80, 150],
        [150, 200]
    ]
    post_data = {
        "city": city,
        "areaRanges": ranges
    }
    data = requests.post(api_url + "/data/c5", json=post_data).json()
    Draw.pic5(ranges, data, city)

    data = requests.get(api_url + "/data/c6/{}/sail".format(city)).json()
    Draw.pic6(data)

    data = requests.get(api_url + "/data/c7/{}".format(city)).json()
    Draw.pic7(data, city)

    if chart == 2:
        pic_url1 = url_for("static", filename="pic{}1.html".format(chart))
        pic_url2 = url_for("static", filename="pic{}2.html".format(chart))
        return render_template('analyse.html', pic_url=pic_url1, pic_url2=pic_url2, cityOptions=cityOptions[chart - 1],
                               chart=str(chart), city=city, is_deal=str(is_deal))
    else:
        pic_url = url_for("static", filename="pic{}.html".format(chart))
        return render_template('analyse.html', pic_url=pic_url, cityOptions=cityOptions[chart - 1],
                               chart=str(chart), city=city, is_deal=str(is_deal))


@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        params = {
            "type": request.form["type"],
            "region": request.form["region"],
            "floor": request.form["floor"]
        }
    else:
        params = {
            "type": "3室2厅",
            "region": "浦东",
            "floor": 6
        }
    data = requests.get(api_url + "/data/predict", params=params).json()

    w1 = data["coefficients"][0]
    w2 = data["coefficients"][1]
    w3 = data["coefficients"][2]
    from_date = data["from"]
    d = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    from_unix = time.mktime(d.timetuple())
    span = data["span"]

    if request.method == "POST":
        s = request.form["date"]
        if s == '':
            value = 0
        else:
            d = datetime.datetime.strptime(s, "%Y-%m-%d")
            end_unix = time.mktime(d.timetuple())
            diff = end_unix - from_unix
            days = diff / (1000 * 60 * 60 * 24)
            value = format(w3 * days**2 + w2 * days + w1, ".2f")
    else:
        value = 0

    pic_url = url_for("static", filename="predict.html")
    Draw.predict(span, w1, w2, w3)
    return render_template('predict.html', pic_url=pic_url, value=value)


@app.route('/query', methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return render_template("query.html", info=[], title="")
    else:
        form = request.form
        params = {
            "city": form["city"],
            "region": form["region"],
            "type": form["type"],
            "floor": int(form["floor"]),
            "face": form["face"],
            "isDeal": int(form["isDeal"])
        }
        info = requests.get(api_url + "/data/raw", params=params).json()
        # print(info)
        return render_template("query.html", info=info["infos"], title=info["title"])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=False)
