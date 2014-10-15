from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector

class OldestBrother(CrawlSpider):
    name = 'VK'
    allowed_domains = ['vk.com']
    start_urls = ['http://m.vk.com/eagle_falcone']
    xpath = '/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]'

    def parse_start_url(self, response):
        # self.save_page(response.body)
        hxs = Selector(response)
        x = hxs.xpath(self.xpath).extract()
        print(x)

    def save_page(self, content):
        with open('page.html', 'wb') as f:
            f.write(content)