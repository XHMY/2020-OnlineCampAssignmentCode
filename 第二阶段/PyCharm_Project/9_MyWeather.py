#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:21:35 2020

@author: yokey
"""

import json
import os
import time
import urllib.request as r

import pygal
from pypinyin import pinyin, Style

weather_archive = {}
filename = "weather_archive_2.json"
has_r = False


def console_output_gra(five_day_temp):
    print("以下显示未来五天的平均气温柱状图:")
    fdt = []
    len_w = len(five_day_temp)
    for temp in five_day_temp:
        fdt.append(round(temp))
    need_print = []
    for i in range(len_w):
        need_print.append(False)
    fdt_sort = sorted(fdt, reverse=True)
    for i in range(len_w - 1):
        fdt_gra = fdt_sort[i] - fdt_sort[i + 1]
        for t in range(fdt_gra):
            need_print[fdt.index(fdt_sort[t])] = True
            for tt in range(len_w):
                if need_print[tt]:
                    print("■■■■■■", end='  ')
                else:
                    print("      ", end='  ')
            print()
    for i in range(0, fdt_sort[len_w - 1], 10):
        print("■■■■■■  " * len_w)
    for i in range(0, len_w):
        print("Day " + str(i + 1), end="   ")
    print()


def five_day_weather(city_name):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city_name + \
          "&mode=json&lang=zh_cn&&APPID=6a67ed641c0fda8b69715c43518b6996&units=metric"
    w_data = r.urlopen(url).read().decode('utf-8')
    w_data = json.loads(w_data)
    temp_chart = pygal.Line(
        style=pygal.style.styles['default'](ci_colors=('black', 'blue')), x_label_rotation=90, fill=True)
    temp40 = []
    x_label = []
    i = 1
    five_day_temp = []
    temp_temp = 0
    print("以下是未来五天天气的描述：")
    for day_weather in w_data["list"]:
        temp_temp += day_weather["main"]["temp"]
        if i % 8 == 0:
            five_day_temp.append(temp_temp / 8)
            temp_temp = 0
        # 记录查询过的数据
        if not has_r:
            weather_archive[w_data["city"]["name"].lower()] = {}
        weather_archive[w_data["city"]["name"].lower(
        )][day_weather["dt"]] = day_weather["main"]
        # 处理显示图表所需的数据
        temp40.append(day_weather["main"]["temp"])
        daytime = day_weather["dt_txt"][8:10] + \
            '日' + day_weather["dt_txt"][10:16]
        x_label.append(daytime)
        # 打印未来五天的天气描述
        if int(day_weather["dt_txt"][11:13]) == 0 or i == 0:
            # 每个不同的日期皆需要换行
            print("\n" + day_weather["dt_txt"][8:10] + '日: ', end='')
        print(day_weather["dt_txt"][11:16] + ':' +
              day_weather["weather"][0]["description"], end=' ')
        i += 1
    temp_chart.x_labels = x_label
    temp_chart.add("温度(℃)", temp40)
    temp_chart.title = '未来五天每3小时的温度变化 (℃)'
    print("\n将自动在浏览器中打开未来5天的温度折线图：")
    temp_chart.render_in_browser()  # 在浏览器中显示图表
    console_output_gra(five_day_temp)


def lookup_archive(city_name):
    cnt = 0
    print("以下显示可查询的时间:", end='')
    for key in weather_archive[city_name]:
        if cnt % 5 == 0:
            print('')
        time_value = time.localtime(int(key))
        time_value = time.strftime("%Y-%m-%d %H:%M", time_value)
        print(time_value, end='  ')
        cnt += 1
    while True:
        in_time = input("\n输入上面任何一个时间可查看对应结果(输入-1结束)：")
        if in_time == '-1':
            break
        time_array = time.strptime(in_time, "%Y-%m-%d %H:%M")
        timestamp = time.mktime(time_array)
        print(weather_archive[city_name][timestamp])


if os.path.exists(filename):
    print("检测到可用的历史记录文件")
    with open(filename, 'r') as fd:
        json_str = fd.read()
    weather_archive = json.loads(json_str)
while True:
    city = input("请输入需要查询的城市名（输入-1结束）：")
    if city == '-1':
        break
    if city[0] > 'z':
        city_pinyin = pinyin(city, style=Style.NORMAL)
        city = ''
        for cha in city_pinyin:
            city += cha[0]
    if city in weather_archive:
        has_r = True
    five_day_weather(city)
    if has_r:
        c = input("历史记录文件中有该城市的记录，是否需要查询(y/N):")
        if c == 'y':
            lookup_archive(city)
        has_r = False
    json_str = json.dumps(weather_archive)  # 将字典转换为json
    with open(filename, 'w') as fd:
        data = fd.write(json_str)
