from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http.request.form import FormRequest
from scrapy.selector import Selector
# import ipdb;ipdb.set_trace()
import time
from Intelligence.google_service import GoogleService
from Intelligence.tracker import Tracker


class OldestBrother(CrawlSpider):
    name = 'VK'
    allowed_domains = ['vk.com']
    start_urls = ['http://m.vk.com/']
    # targets = ['http://m.vk.com/oleksandr.hubachov']
    path = 'http://localhost:63342/BigBrother/'
    targets = ['page_minutes.html', 'page_online.html', 'page_today.html']
    xpath_time_status = '/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/text()'
    xpath_mobile = '//*[@id="mcont"]/div/div[1]/div[1]/div[1]/b'
    tracker = Tracker(GoogleService())

    # def start_requests(self):
    #     yield Request(url=self.start_urls[0], callback=self.login)
    #
    # def login(self, response):
    #     return FormRequest.from_response(response,
    #                                      formdata={'login': 'submit', 'email': '***', 'pass': '***'},
    #                                      callback=self.after_login, dont_filter=True)
    #
    # def after_login(self, response):
    #     while True:
    #         time.sleep(60)
    #         for target in self.targets:
    #             yield Request(url=target, callback=self.watch_target, method='GET', dont_filter=True)

    def start_requests(self):
        for target in self.targets:
            yield Request(callback=self.watch_target, url=self.path + target, method='GET', dont_filter=True)

    def watch_target(self, response):
        # self.save_page(response.body, response.url)
        hxs = Selector(response)
        time_status = hxs.xpath(self.xpath_time_status).extract()
        mobile_status = hxs.xpath(self.xpath_mobile).extract()
        print time_status[0]
        print mobile_status
        # self.tracker.track(time_status[0], mobile_status)

    def save_page(self, content, name):
        with open('page_{0}.html'.format(name.split('/')[-1]), 'wb') as f:
            f.write(content)