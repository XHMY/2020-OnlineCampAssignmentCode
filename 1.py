/*
 * @Author: mikey.zhaopeng 
 * @Date: 2020-05-25 16:48:07 
 * @Last Modified by:   mikey.zhaopeng 
 * @Last Modified time: 2020-05-25 16:48:07 
 */
 
import urllib.request as r
import re
import json
from retrying import retry

zipcode = [10001, 21215, 43215, 10013, 10011, 11201, 10003, 20105, 10025, 30303, 10002, 30043,
           11215, 21224, 11101, 10021, 10023, 11211, 33132, 10010, 20001, 11221, 10024, 11354,
           11212, 10022, 20011, 30022, 11214, 53215, 20002, 44304, 11230, 14215, 10314, 30331,
           21234, 32210, 21230, 11213, 11234, 11203, 10004, 10452, 33025, 11233, 11222, 10032,
           10451, 10012, 11235, 33311, 11225, 11434, 11220, 30004, 10453, 33014, 11204, 33125,
           24112, 10014, 11223, 11210, 55455, 14221, 33012, 22314, 33142, 21043, 10031, 11355,
           11205, 33023, 11231, 11432, 10035, 10033, 54302, 30305, 10005, 30024, 32304, 22310,
           10312, 33324, 20003, 10301, 32244]

all_data = []


@retry
def scrape(url):
    return r.urlopen(url).read().decode('utf-8')


for zc in zipcode:
    url = "http://api.openweathermap.org/data/2.5/weather?zip="+str(zc) + \
        ",us&mode=json&units=metric&appid=6a67ed641c0fda8b69715c43518b6996"

    data = r.urlopen(url).read().decode('utf-8')
    print("已获取到城市：" + re.search(r"(?:\"name\":\")(.*?)\"",
                                data).group(1) + " , ZIP Code = "+str(zc))
    data = scrape(url)
    all_data.append(data)

json_str = json.dumps(all_data, ensure_ascii=False)
filename = 'weather_scrape_data.json'
with open(filename, 'w') as fd:
    data = fd.write(json_str)
print("已完成写入文件 'weather_scrape_data.json'")
