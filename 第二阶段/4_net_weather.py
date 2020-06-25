#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 17:14:30 2020

@author: yokey
"""

import os
filename = "weather_archive.json"
if os.path.exists(filename):
    print("检测到可用的离线天气文件，将自动使用离线模式。")
    with open(filename,'r') as fd:
        data = fd.read();
else:
    print("本次从服务器获取天气信息，下次启动可使用离线模式")
    import urllib.request as r
    city = "guangzhou"
    url =  "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&mode=json&units=metric&lang=zh_cn&APPID=6a67ed641c0fda8b69715c43518b6996"
    data = r.urlopen(url).read().decode('utf-8')
    with open(filename,'x') as fd:
        fd.write(data);


import json
data = json.loads(data)

#print(data['main']['temp'])

print("以下是今天的天气：")
print("温度：" + str(data['main']['temp']) + "摄氏度")
print("体感温度：" + str(data['main']['feels_like']) + "摄氏度")
print("气压：" + str(data['main']['pressure']) + "Pa")
print("最高温度：" + str(data['main']['temp_max']) + "摄氏度")
print("最低温度：" + str(data['main']['temp_min']) + "摄氏度")
print("湿度：" + str(data['main']['humidity']) + "%")
