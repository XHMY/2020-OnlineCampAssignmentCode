from lxml import etree
import urllib.request as r
import random
import re
import json
from retrying import retry
import time


def d_id(id_s):
    return id_s[-9:]


@retry(stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
def get_text(url):
    USER_AGENT = random.choice([
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    ])
    request = r.Request(url, headers={'User-Agent': USER_AGENT})
    time.sleep(0.5)
    return r.urlopen(request).read().decode('utf-8')


all_text = []
all_id = []
text_path_rex = r"<div class=\"content\">(.*?)</div>"
for i in range(1, 6):
    print("开始爬取第 " + str(i) + " 页")
    id_xpath = "/html/body/div[1]/div/div[2]/div[*]/@id"
    url = "https://www.qiushibaike.com/text/page/"+str(i)+"/"
    request = r.Request(url, headers={
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"})
    data = r.urlopen(request).read().decode('utf-8')
    html = etree.XML(data, etree.HTMLParser())
    the_id = html.xpath(id_xpath)
    the_id = list(map(d_id, the_id))
    all_id += the_id

while len(all_id) != 0:
    ok = True
    print("开始获取ID为 " + str(all_id[0]) + " 的段子")
    url = "https://www.qiushibaike.com/article/" + all_id[0]
    try:
        data = get_text(url)
    except Exception as e:
        print("遇到错误，稍后重试")
        ok = False
    if not ok:
        all_id.append(all_id[0])
    else:
        the_text = re.search(text_path_rex, data).group(1)
        the_text = the_text.replace("<br/>", "\n")
        the_text = re.sub(r"<img.*?>", " ", the_text)
        all_text.append(the_text)
    all_id.pop(0)

json_str = json.dumps(all_text, ensure_ascii=False)
filename = 'duanzi.json'
with open(filename, 'w') as fd:
    fd.write(json_str)
print("已将爬取的段子保存到本地")
