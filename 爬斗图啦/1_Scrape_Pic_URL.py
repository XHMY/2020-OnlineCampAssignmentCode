import requests
from lxml.etree import HTML  # 将网页字符串转换成一个html对象
import queue
import random
from retrying import retry
import json


doutu_url = 'https://www.doutula.com/photo/list/?page={}'
task_url_q = queue.Queue()


@retry(stop_max_attempt_number=2, wait_random_min=300, wait_random_max=1500, stop_max_delay=4000)
def get_html(url):
    '''通过page,下载网页内容'''
    # user-agent代表是何种设备,例如 xx系统xx浏览器xx版本
    USER_AGENT = random.choice(
        ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'])
    headers = {
        'user-agent': USER_AGENT}
    html_str = requests.get(url, headers=headers).text
    return html_str


def get_urls(html_str):
    '''通过网页字符串，提取图片下载地址'''
    selector = HTML(text=html_str)
    img_xpath = '//*[@id="pic-detail"]/div/div[2]/div[2]/ul/li/div/div/a[.]/img/@data-original'
    img_name_xpath = '//*[@id="pic-detail"]/div/div[2]/div[2]/ul/li/div/div/a[.]/img/@alt'
    img_ls = []
    img_ls.append(selector.xpath(img_xpath))
    img_ls.append(selector.xpath(img_name_xpath))
    return img_ls


max_page = 3444
for page in range(1, max_page+1):
    task_url_q.put(doutu_url.format(page))

pic_url_list = []
while not task_url_q.empty():
    ok = True
    cur_url = task_url_q.get()
    print("当前获取页面：" + cur_url)
    try:
        html_str = get_html(cur_url)
    except Exception as e:
        print(e)
        task_url_q.put(cur_url)
        ok = False
    if ok:
        pic_url_list.append(get_urls(html_str))

json_str = json.dumps(pic_url_list, ensure_ascii=False)
filename = 'Pic_URL.json'
with open(filename, 'w') as fd:
    fd.write(json_str)
print("Finish")
