# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from zhihu.items import ZhihuUserItem


class ExampleSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/people/zhang-zhu-xiang/followers']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "https://www.zhihu.com/"
    }
    def start_requests(self):
        return [scrapy.Request(url='https://www.zhihu.com',
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.post_login)]
    

    def post_login(self, response):
        xsrf = scrapy.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        self.logger.debug("Get <_xsrf> value: %s" % xsrf)
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   meta = {'cookiejar': response.meta['cookiejar']},
                                   headers = self.headers,
                                   formdata = {'_xsrf': xsrf,
                                               'email': 'xxx',
                                               'password': 'xxx',
                                             'remember_me': 'true'},
                                   callback = self.after_login)]


    def after_login(self, response):    
        if b"errcode" in response.body:
            self.logger.error("Login failed")
            return
        self.logger.info("Login succeed")
        # self.log(json.loads(response.body.decode('utf-8')))
        return scrapy.Request(self.start_urls[0],
                       meta = {'cookiejar': 1},
                       headers = self.headers,
                       callback = self.parse_follower)
        
    def parse_follower(self, response):
        self.logger.debug("parse follower")
        followers = scrapy.Selector(response).xpath("//div[@class='zm-list-content-medium']")
        for follower in followers:
            user = ZhihuUserItem()
            user_info = follower.xpath(".//a/text()").extract()
            user['name'] = user_info[0]
            user['follower_num'] = user_info[1]
            user['ask_num'] = user_info[2]
            user['answer_num'] = user_info[3]
            user['commend_num'] = user_info[4]
            yield user

    def parse_followee(self, response):
        self.logger.debug("parse followee")
        # scrapy.Selector(response).xpath()


"""
 commit 之  前  删  密  码  啊 ！
 """
                      
