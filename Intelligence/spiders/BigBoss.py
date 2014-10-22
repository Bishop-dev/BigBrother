from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from Intelligence.mongoservice import MongoService
# import ipdb;ipdb.set_trace()

class OldestBrother(CrawlSpider):
    name = 'VK'
    allowed_domains = ['vk.com']
    start_urls = ['http://m.vk.com/oleksandr.hubachov']
    xpath_time_status = '/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/text()'
    xpath_mobile = '//*[@id="mcont"]/div/div[1]/div[1]/div[1]/b'
    mongo = MongoService()

    def parse_start_url(self, response):
        # self.save_page(response.body)
        self.watch_target(response)

    def watch_target(self, response):
        hxs = Selector(response)
        time_status = hxs.xpath(self.xpath_time_status).extract()
        mobile_status = hxs.xpath(self.xpath_mobile).extract()
        self.mongo.track_status(time_status[0], mobile_status)

    def save_page(self, content):
        with open('page_online.html', 'wb') as f:
            f.write(content)