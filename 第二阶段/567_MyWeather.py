#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:21:35 2020

@author: yokey
"""


import pygal
import time
import urllib.request as r
from pypinyin import pinyin, Style
import json
import os
import re

weather_archive = {}
filename = "weather_archive_2.json"
has_r = False


def get_current_temp(city):
    url =  "http://api.openweathermap.org/data/2.5/weather?q=" + city + \
    "&mode=json&units=metric&lang=zh_cn&APPID=6a67ed641c0fda8b69715c43518b6996"
    data = r.urlopen(url).read().decode('utf-8')
    search = re.search(r"(?:\"temp\":)([^,]+)", data)
    print("我们用正则找到的温度是: " + str(search.group(1)) + "摄氏度")
    
    

def get_5DayWeather(city):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + \
        "&mode=json&lang=zh_cn&&APPID=6a67ed641c0fda8b69715c43518b6996&units=metric"
    data = r.urlopen(url).read().decode('utf-8')
    data = json.loads(data)
    temp_chart = pygal.Line(
        style=pygal.style.styles['default'](ci_colors=('black', 'blue')), x_label_rotation=90, fill=True)
    temp40 = []
    x_lable = []
    i = 0
    print("以下是未来五天天气的描述：")
    for dayw in data["list"]:
        # 记录查询过的数据
        if not has_r:
            weather_archive[data["city"]["name"].lower()] = {}
        weather_archive[data["city"]["name"].lower()][dayw["dt"]
                                                      ] = dayw["main"]
        # 处理显示图表所需的数据
        temp40.append(dayw["main"]["temp"])
        daytime = dayw["dt_txt"][8:10] + '日' + dayw["dt_txt"][10:16]
        x_lable.append(daytime)
        # 打印未来五天的天气描述
        if(int(dayw["dt_txt"][11:13]) == 0 or i == 0):
            i = 1  # 每个不同的日期皆需要换行
            print("\n"+dayw["dt_txt"][8:10] + '日: ', end='')
        print(dayw["dt_txt"][11:16] + ':' +
              dayw["weather"][0]["description"], end=' ')
    temp_chart.x_labels = x_lable
    temp_chart.add("温度(℃)", temp40)
    temp_chart.title = '未来五天每3小时的温度变化 (℃)'
    print("\n将自动在浏览器中打开未来5天的温度折线图：")
    temp_chart.render_in_browser()  # 在浏览器中显示图表


def lookup_archive(city):
    cnt = 0
    print("以下显示可查询的时间:", end='')
    for key in weather_archive[city]:
        if(cnt % 5 == 0):
            print('')
        time_value = time.localtime(int(key))
        time_value = time.strftime("%Y-%m-%d %H:%M", time_value)
        print(time_value, end='  ')
        cnt += 1
    while True:
        intime = input("\n输入上面任何一个时间可查看对应结果(输入-1结束)：")
        if(intime == '-1'):
            break
        timeArray = time.strptime(intime, "%Y-%m-%d %H:%M")
        timestamp = time.mktime(timeArray)
        print(weather_archive[city][timestamp])


if os.path.exists(filename):
    print("检测到可用的历史记录文件")
    with open(filename, 'r') as fd:
        json_str = fd.read()
    weather_archive = json.loads(json_str)
while True:
    city = input("请输入需要查询的城市名（输入-1结束）：")
    if(city == '-1'):
        break
    if(city[0] > 'z'):
        city_pinyin = pinyin(city, style=Style.NORMAL)
        city = ''
        for cha in city_pinyin:
            city += cha[0]
    if(city in weather_archive):
        has_r = True
    # get_5DayWeather(city)
    get_current_temp(city)
    if(has_r):
        c = input("历史记录文件中有该城市的记录，是否需要查询(y/N):")
        if(c == 'y'):
            lookup_archive(city)
        has_r = False
    json_str = json.dumps(weather_archive)  # 将字典转换为json
    with open(filename, 'w') as fd:
        data = fd.write(json_str)
