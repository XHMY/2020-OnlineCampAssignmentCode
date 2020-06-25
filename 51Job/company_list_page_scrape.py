import json

import requests
from lxml.html import etree
from retrying import retry

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

error_list = []
ls = []


def xpath2text(x):
    if (x.text):
        return x.text
    else:
        return ''


@retry(stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
def get_html(url):
    return requests.get(url, headers=headers, timeout=4)


# 从文件中读取本次爬取的目标范围以及ID
with open("task.json", 'r') as fd:
    task = json.loads(fd.read())

# 读取包含URL的列表
with open("company_pageURL_list.json", 'r') as fd:
    url_list = json.loads(fd.read())

cnt = 0
for i in range(task["start"], task["start"] + task["amount"]):  # 公司页数
    try:
        response = get_html(url_list[i])
        data = response.content.decode('gbk')
        data1 = etree.HTML(data)
        print("已获取页面：" + url_list[i])
        name = list(map(xpath2text, data1.xpath('//span[@class="s1"]/a')))
        nature = list(map(xpath2text, data1.xpath('//span[@class="s2"]')))
        scale = list(map(xpath2text, data1.xpath('//span[@class="s3"]')))
        location = list(map(xpath2text, data1.xpath('//span[@class="s4"]')))
        industry = list(map(xpath2text, data1.xpath('//span[@class="s5"]')))
        company_url = data1.xpath('//span[@class="s1"]/a/@href')
        nature.pop(0)
        scale.pop(0)
        location.pop(0)
        industry.pop(0)

        for j in range(len(name)):
            ls.append([])
            ls[cnt].append([name[j], nature[j], scale[j],
                            location[j], industry[j], company_url[j]])
            cnt += 1
    except Exception as e:
        print(e)
        error_list.append([url_list[i], e])

print("已完成，总共遇到" + str(len(error_list)) + "条错误。")
json_str = json.dumps(ls, ensure_ascii=False)  # 转换到json
with open("company_list" + str(task["ID"]) + ".json", 'w', encoding='utf-8') as fd:
    fd.write(json_str)

json_str = json.dumps(error_list, ensure_ascii=False)  # 转换到json
with open("error_list" + str(task["ID"]) + ".json", 'w', encoding='utf-8') as fd:
    fd.write(json_str)
