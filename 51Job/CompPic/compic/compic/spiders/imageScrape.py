import scrapy


class ImageScrape(scrapy.Spider):
    name = "compicSpider"
    allowed_domains = ['51job.com']
    cnt = 0

    #
    # with open("comp_url_list.json", "r", encoding='utf-8') as f:
    #     start_urls = json.loads(f.read())

    def parse(self, response):
        # if response.css('.research::text').get() == "很抱歉，你选择的职位目前已经暂停招聘":
        #     pass
        self.cnt += 1
        if self.cnt % 10 == 0:
            print("当前处理第{}个页面  进度 {:.2}%".format(self.cnt, self.cnt / len(self.start_urls) * 100))
        pic_url = response.xpath('//*[@id="divCoPoster"]/ul/li[.]/a/@bigimg').getall()
        if not pic_url:
            pass
