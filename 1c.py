/*
 * @Author: Yoeky 
 * @Date: 2020-05-25 16:48:50 
 * @Last Modified by:   Yoeky 
 * @Last Modified time: 2020-05-25 16:48:50 
 */

 
from flask import Flask
import urllib.request as r
app = Flask(__name__)
app.run(port=8888)
cache = {}


@app.route('/<city>')
def hello_world(city):
    if city in cache:
        return cache[city]
    else:
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + \
            "&mode=json&units=metric&lang=zh_cn&APPID=6a67ed641c0fda8b69715c43518b6996"
        try:
            data = r.urlopen(url).read().decode('utf-8')
        except Exception as e:
            data = str(e)
        cache[city] = data
        return data
