# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']
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
        return [scrapy.Request(self.start_urls[0],
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.post_login)]
    

    def post_login(self, response):
        xsrf = scrapy.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        self.log("Get <_xsrf> value: %s" % xsrf)
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   headers=self.headers,
                                   formdata={'_xsrf': xsrf,
                                             'email': 'your_email',
                                             'password': 'your_password',
                                             'remember_me': 'true'},
                                   callback=self.after_login)]


    def after_login(self, response):    
        if b"authentication failed" in response.body:
            self.logger.error("login failed")
            return
        print("login succeed~~~~~~~~~~~~~~~~~~~~")
