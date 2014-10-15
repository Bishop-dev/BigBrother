from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from Intelligence.mongoservice import MongoService
# import ipdb;ipdb.set_trace()

class OldestBrother(CrawlSpider):
    name = 'VK'
    allowed_domains = ['vk.com']
    start_urls = ['http://m.vk.com/eagle_falcone']
    xpath = '/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/text()'
    mongo = MongoService()

    def parse_start_url(self, response):
        # self.save_page(response.body)
        hxs = Selector(response)
        status = hxs.xpath(self.xpath).extract()
        self.mongo.track_status(status[0])

    def save_page(self, content):
        with open('page_online.html', 'wb') as f:
            f.write(content)