import re
import urllib.request as r
import requests

url = "https://www.bing.com/"
data = r.urlopen(url).read().decode('utf-8')
searchObj = re.search(r'<meta\sproperty=\"og:image\"\scontent="(.*?)&', data)
url = searchObj.group(1)
data_i = requests.get(url)
img_name = "today.jpg"
with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
    file.write(data_i.content)
    file.flush()
print("已完成抓取今日的Bing首页图片并保存到当前运行目录")
