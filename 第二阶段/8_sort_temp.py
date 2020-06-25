import urllib.request as r
from pypinyin import pinyin, Style
import json
import time


def get_sorted_weather(city):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + \
        "&mode=json&lang=zh_cn&&APPID=6a67ed641c0fda8b69715c43518b6996&units=metric"
    data = r.urlopen(url).read().decode('utf-8')
    data = json.loads(data)
    weather_list = data["list"]
    weather_list = sorted(weather_list, key=lambda x: -x["main"]["temp"])
    print("以下是按照气温从高到底排序的未来几天天气情况:")
    for i in range(0, data["cnt"]):
        if(i == 10):
            c = input("是否打印剩余的" + str(data["cnt"]-i) + "项(Yes/no):")
            if(c == "no"):
                break
        print(str(time.strftime("%m-%d %H:%M", time.localtime(weather_list[i]["dt"]))) + "   " +
              str(weather_list[i]["main"]["temp"]) + "℃   " +
              weather_list[i]["weather"][0]["description"])
    print("\n")


while True:
    print("*****使用本程序您可查看未来五天最高气温*****")
    city = input("请输入需要排序温度的的城市名（输入-1结束）：")
    if(city == '-1'):
        break
    if(city[0] > 'z'):
        city_pinyin = pinyin(city, style=Style.NORMAL)
        city = ''
        for cha in city_pinyin:
            city += cha[0]
    get_sorted_weather(city)
