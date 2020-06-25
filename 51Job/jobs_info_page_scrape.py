import requests
import re
import threading
from fake_useragent import UserAgent  # 需要pip install fake_useragent
import copy
import json
from lxml import etree
import datetime
import time

error_list = []


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("开始线程：" + self.name)
        run_scrape(self.threadID)
        print("退出线程：" + self.name)


def run_scrape(threadID):
    while len(comp_list) != 0:
        comp_name = comp_list.pop()
        for i in range(len(job_list[comp_name])):
            try:
                data = get_urls(job_list[comp_name][i][-1])
                job_list[comp_name][i].append(get_label(data))
                job_list[comp_name][i].append(get_bigtitle_info(data))
                print("线程{}：完成爬取 {} 的第 {} 个职位".format(threadID, comp_name, i + 1))
            except Exception as e:
                error_list.append([comp_name, job_list[comp_name][i][-1], str(e)])
                print("线程{}：爬取 {} 的第 {} 个职位遇到错误 {}".format(threadID, comp_name, i + 1, str(e)))


def get_urls(url):  # 获取网页源码
    headers = {
        'User-Agent': UserAgent().random
    }
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    response = r.text
    return response


def get_label(data):  # 解析标签
    label = re.findall(r'<span class="sp4">(.*?)</span>', data)
    return label  # list


def get_bigtitle_info(data):
    selector = etree.HTML(data)
    info = {}
    # z=selector.xpath('string(/html/body/div[3]/div[2]/div[3]/div[1]/div)')
    # 获取大标题
    firsttitle = selector.xpath(
        '/html/body/div[3]/div[2]/div[3]/div[1]/h2/span')
    first = firsttitle[0].xpath('string(.)')
    secondtitle = selector.xpath(
        '/html/body/div[3]/div[2]/div[3]/div[2]/h2/span')
    second = secondtitle[0].xpath('string(.)')
    thirdtitle = selector.xpath(
        '/html/body/div[3]/div[2]/div[3]/div[3]/h2/span')
    third = thirdtitle[0].xpath('string(.)')
    num1 = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div')
    z_l = num1[0].xpath('string(.)').replace('\r\n', '')
    # 判断是否包含部门信息
    if third != '公司消息':
        # 获取内容
        x = selector.xpath(
            '/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()')
        y = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()')
        z = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()')
        # /html/body/div[3]/div[2]/div[3]/div[3]/div
        # info['xx']=selector.xpath('/html/body/div[3]/div[2]/div[3]/div[4]/div/text()')
        info = {first: z_l, second: x, third: y}
    if third == '公司信息':
        x = selector.xpath(
            '/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()')
        y = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()')
        info = {first: z_l, second: x}
    return info


# print(get_bigtitle_info(get_urls("https://jobs.51job.com/guangzhou/118915349.html")))
# print(get_label(get_urls("https://jobs.51job.com/guangzhou/118915349.html?s=03&t=0")))

# 从文件中读取本次爬取的目标范围以及ID
with open("task.json", 'r', encoding='utf-8') as fd:
    task = json.loads(fd.read())

# 读取包含URL的列表
with open("jobs_list.json", 'r', encoding='utf-8') as fd:
    job_list = json.loads(fd.read())


comp_list = list(job_list.keys())
thread = []
thread_num = 3

starttime = datetime.datetime.now()
for i in range(thread_num):
    time.sleep(0.3)
    thread.append(myThread(i))
    thread[i].start()

for i in range(thread_num):
    thread[i].join()

print("程序运行完成")
endtime = datetime.datetime.now()
print("运行耗时 {} 秒".format((endtime - starttime).seconds))
# for i in range(task["start"], task["start"] + task["amount"]):
#     data = {}
#     data["标签"] = get_label(get_urls(job_list[i][6]))

# 将结果写入文件
with open("job_info_list" + str(task["ID"]) + ".json", 'w', encoding='utf-8') as fd:
    fd.write(json.dumps(job_list, ensure_ascii=False))

# 将错误列表写入文件
with open("errorlist" + str(task["ID"]) + ".json", 'w', encoding='utf-8') as fd:
    fd.write(json.dumps(error_list, ensure_ascii=False))
