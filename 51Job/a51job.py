# -*- coding: utf-8 -*-
import scrapy
import re

from lxml import etree
import html


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://jobs.51job.com/xian/{}.html'.format(122218533)]

    def start_requests(self):
        urls = [
            'https://jobs.51job.com/beijing-xcq/99800217.html?s=01&t=0'
        ]  # urls里面为需要解析的url
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass

    def get_label(self, data):
        label = re.findall('<span class="sp4">(.*?)</span>', data)
        return label  # list

    def parse(self, response):
        data = response.text
        l = self.get_label(data)
        if l == []:
            print(str(l) + '无职业信息')
        else:
            print(l)

    def get(self, data):
        selector = etree.HTML(data)

        # 获取职业消息部分源码
        first = selector.xpath('//div[@class="tBorderTop_box"][1]')[0]
        first_str = etree.tostring(first).decode('gbk')
        first_c = html.unescape(first_str)
        # 获取联系方式部分源码
        second = selector.xpath('//div[@class="tBorderTop_box"][2]')[0]
        second_str = etree.tostring(second).decode('gbk')
        second_c = html.unescape(second_str)
        # 定位公司消息、部门消息源码
        third = selector.xpath('//div[@class="tBorderTop_box"][3]')[0]
        # 判断有无公司消息
        thirdtitle = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/h2/span')
        thirdt = thirdtitle[0].xpath('string(.)')
        if thirdt != '公司消息':
            third_str = etree.tostring(third).decode('gbk')
            third_c = html.unescape(third_str)
            print(first_c)
            print(second_c)
            print(third_c)
        else:
            print(first_c)
            print(second_c)
