import json

import scrapy


class JobInfoSpider(scrapy.Spider):
    name = "jobinfo"
    allowed_domains = ['51job.com']
    cnt = 0

    with open("jobs_url_list.json", "r", encoding='utf-8') as f:
        start_urls = json.loads(f.read())

    def parse(self, response):
        # if response.css('.research::text').get() == "很抱歉，你选择的职位目前已经暂停招聘":
        #     pass
        self.cnt += 1
        print("当前处理第{}个页面  进度 {}%".format(self.cnt, self.cnt / len(self.start_urls) * 100))
        yield {
            "job_title": response.css("h1").attrib["title"],
            "job_tag": response.css(".t1 span::text").getall(),
            "job_brief": [a.replace("\xa0", "") for a in response.css(".msg::text").getall()],
            "comp_name": response.css(".catn::text").get(default=''),
            "salary": response.css(".cn strong::text").get(default=''),
            "job_detail": response.xpath('//*[@class="bmsg job_msg inbox"]')[0].xpath('string()').get(default='').split(),
            "contact_info": response.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p').getall(),
            "depart": response.xpath('//div[@class="tBorderTop_box"][3]').get(default='')
        }
