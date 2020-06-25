# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author；鸿
# import requests
# # import urllib.request as r
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
# }
# url = 'https://jobs.51job.com/all/co2758227.html'
# # response = requests.get(url,headers = headers)
# response = requests.get(url,headers = headers)
# print(response.content.decode('gbk'))

# import requests
# from lxml.etree import HTML
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
# }
# url = 'https://jobs.51job.com/all/co5325953.html'
# hidTotal = HTML(requests.get(url,headers=headers).content.decode('gbk')).xpath('//*[@id="hidTotal"]/@value')
# formdata ={'pageno': 1,'hidTotal':hidTotal}#pageno 页数 hidTotal xpath(//*[@id="hidTotal"]/@value)
# html = requests.post(url,headers=headers,data=formdata).content.decode('gbk')
# print(html)

import json
import re

import requests
from fake_useragent import UserAgent
from lxml.etree import HTML
from retrying import retry


# url = 'https://jobs.51job.com/all/co5325953.html'

def get_url():
    """获取文件中的所有url"""
    with open('company_list.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    url_ls = []
    for url in data:
        url_ls.append(url[-1])
    return url_ls


def get_company():
    """获取文件中的所有公司名"""
    with open('company_list.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    company_ls = []
    for company in data:
        company_ls.append(company[0])
    return company_ls


def write_error_list(json_data, id):
    with open('error_list{}.json'.format(id), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
    print('error_list{}.json'.format(id), '写入成功...')


def write_jobs_list_json(json_data, id):
    with open('jobs_list{}.json'.format(id), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
    print('jobs_list{}.json'.format(id), '写入成功...')


def read_task_json():
    with open("task.json", 'r') as fd:
        task = json.loads(fd.read())
    return task


def read_company_list(start, end):
    with open('company_list.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    data1 = []
    for i in range(start, end):
        data1.append(data[i])
    return data1


def supplement_company_list(json_data, id):
    with open('company_info_list{}.json'.format(id), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
    print('company_info_list{}.json'.format(id), '写入成功...')


def write_error_company_list(json_data, id):
    with open('error_company_list{}.json'.format(id), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
    print('error_company_list{}.json'.format(id), '写入成功...')


@retry(stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
def get_request(url, headers):
    return requests.get(url, headers=headers, timeout=4).content.decode('gbk')


@retry(stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
def post_request(url, formdata, headers):
    return requests.post(url, headers=headers, data=formdata, timeout=4).content.decode('gbk')


def get_company_news(company, url_ls, i, error_company_list):
    """获取第i个公司的介绍"""
    headers = {
        'User-Agent': UserAgent().random
    }
    compare_news = []  # 公司介绍
    url = url_ls[i]
    flag = 1
    try:
        response = get_request(url, headers)
        a = re.compile('class="con_txt">(.*?)</div>', re.S).findall(response)
        a[0] = a[0].replace("<br>", " ").replace("&nbsp;", "")  # 公司简介
        a1 = re.compile('<h1 title=(.*?)>', re.S).findall(response)  # 公司名称
        a2 = re.compile('<p class="fp">.*?<span class="label">.*?</span>(.*?)</p>', re.S).findall(response)  # 公司地址
        a3 = re.compile('<p class="fp tmsg"><span class="label">.*?</span><span>(.*?)</span>', re.S).findall(
            response)  # 公司官网网址
        a2_str = "".join(a2)
        a3_str = "".join(a3)
        compare_news.append([a[0]])
        compare_news.append([a2_str.replace(" ", "")])
        if [a3_str.replace(" ", "")] == [""]:
            compare_news.append(['None'])
        else:
            compare_news.append([a3_str.replace(" ", "")])
        print('{}详情获取成功...'.format(company))
    except Exception as e:
        print('{}详情获取失败... 原因为:{}'.format(company, str(e)))
        error_company_list.append([url, "'序号':{}".format(i), str(e)])
        flag = 0
    return compare_news, flag


def get_page_job(company, url, i, error_list):
    """获取当前i页面的所有职位信息"""
    headers = {
        'User-Agent': UserAgent().random
    }
    all_job = []
    try:
        response = get_request(url, headers)
        hidTotal = HTML(response).xpath('//*[@id="hidTotal"]/@value')
        # pageno 页数 hidTotal xpath(//*[@id="hidTotal"]/@value)
        formdata = {'pageno': i, 'hidTotal': hidTotal}
        html = post_request(url, formdata, headers)
        re_job = '<p class="t1"><a target=".*?" href=".*?" class=".*?" title=".*?">(.*?)</a></p>'
        re_aside = '<span class="t2">(.*?)</span>'
        re_place = '<span class="t3">(.*?)</span>'
        re_treatment = '<span class="t4">(.*?)</span>'
        re_url = '<p class="t1"><a target=".*?" href="(.*?)" class=".*?" title=".*?">'
        job_ls = re.findall(re_job, html, re.S)
        aside_ls = re.findall(re_aside, html, re.S)
        place_ls = re.findall(re_place, html, re.S)
        treatment_ls = re.findall(re_treatment, html, re.S)
        url_ls = re.findall(re_url, html, re.S)
        for a in range(len(job_ls)):
            attribute = [job_ls[a]]  # 属性
            list_temp = aside_ls[a].split(' | ')
            [attribute.append(j) for j in list_temp]
            attribute.append(place_ls[a])
            attribute.append(treatment_ls[a])
            attribute.append(url_ls[a])
            all_job.append(attribute)
        if not all_job:
            print(company, ': 数据获取完成'.format(i))
        else:
            print(company, ': 第{}页数据获取成功'.format(i))
    except Exception as e:
        print(e)
        print(company, ': 第{}页数据获取失败!!!'.format(i))
        error_list.append([url, "'pageno':{}".format(i), e])  # url，第i页，错误原因
        # write_error_list([url,"'pageno':{}".format(i), e],id)
    return all_job


def get_all_job(company, url, id):
    """获取当前公司的所有职位信息"""
    all_job = []
    i = 1
    error_list = []
    while True:
        all_job_temp = get_page_job(company, url, i, error_list)
        if not all_job_temp:
            break
        all_job.extend(all_job_temp)
        i += 1
    if error_list:
        write_error_list([url, "'pageno':{}".format(i)], id)
    return all_job


def get_all_job_json(start, end, id):
    company_job = {}
    # for i in range(start,end):
    company_list = get_company()
    url_list = get_url()
    error_company_list = []
    data = read_company_list(start, end)
    i = 0
    for j in range(start, end):
        compare_news, flag = get_company_news(company_list[j], url_list, j, error_company_list)
        if flag == 1:
            data[i].append(compare_news)
        all_job = get_all_job(company_list[j], url_list[j], id)
        company_job[company_list[j]] = all_job
        i += 1
    write_jobs_list_json(company_job, id)
    supplement_company_list(data, id)
    if error_company_list:
        write_error_company_list(error_company_list, id)


def run():
    task = read_task_json()
    get_all_job_json(task["start"], task["start"] + task["amount"], task["ID"])


if __name__ == '__main__':
    run()
    # get_all_job_json(18, 20, 1)
