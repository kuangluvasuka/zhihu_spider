# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from zhihu.items import ZhihuUserItem


class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/people/zhang-zhu-xiang/followers']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Host":"www.zhihu.com",
        "Referer": "https://www.zhihu.com"
    }
    xrsf = ''


    def start_requests(self):
        return [scrapy.Request(url='https://www.zhihu.com',
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.post_login)]
    

    def post_login(self, response):
        self.xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        self.logger.debug("_xsrf is %s" % self.xsrf)
        return scrapy.FormRequest("https://www.zhihu.com/login/email",
                                  meta={'cookiejar': response.meta['cookiejar']},
                                  headers=self.headers,
                                  formdata={'_xsrf': self.xsrf,
                                            'email': '363286855@qq.com',
                                            'password': 'asdfghjkl',
                                            'remember_me': 'true'},
                                  callback=self.after_login)


    def after_login(self, response):    
        if b"errcode" in response.body:
            self.logger.error("Login failue")
            return
        self.logger.info("Login succeed")
        return scrapy.Request(self.start_urls[0],
                              meta={'cookiejar': 1},
                              headers=self.headers,
                              callback=self.parse_follower)
        
    def parse_follower(self, response):
        self.logger.debug("parse follower")
        # followers = scrapy.Selector(response).xpath("//div[@class='zm-list-content-medium']")
        # for follower in followers:
        #     user = ZhihuUserItem()
        #     user_info = follower.xpath(".//a/text()").extract()
        #     user['name'] = user_info[0]
        #     user['follower_num'] = user_info[1]
        #     user['ask_num'] = user_info[2]
        #     user['answer_num'] = user_info[3]
        #     user['commend_num'] = user_info[4]
        #     yield user
        hash_id = json.loads(response.xpath('//div/@data-init').extract()[0])['params']['hash_id']
        self.logger.debug("hash_id is %s" % hash_id)
        follow = 'Followers'    # or 'Followees'
        follow_url = 'https://www.zhihu.com/node/Profile' + follow + 'ListV2'
        follow_num = self.get_follow_num(response)

        for i in range((follow_num[1] - 1) // 20 + 1):
            offset = i * 20
            params = json.dumps({'offset':offset,'order_by':'created','hash_id':hash_id})
            yield scrapy.FormRequest(url=follow_url,
                                      headers=self.headers,
                                      meta={'cookiejar': response.meta['cookiejar']},
                                      formdata={'_xsrf': self.xsrf,
                                                'method': 'next',
                                                'params': params},
                                      callback=self.parse_follow_list)
    def parse_follow_list(self, response):
        data = json.loads(response.body.decode('utf-8'))
        for msg in data['msg']:
            follower = ZhihuUserItem()
            # follower['name'] = scrapy.Selector(msg).xpath('//a[@class="zg-link author-link"]/text()').extract()[0]
            user_info = scrapy.Selector(text=msg).xpath('//div[@class="zm-list-content-medium"]//a/text()').extract()
            follower['name'] = user_info[0]
            follower['follower_num'] = user_info[1]
            follower['ask_num'] = user_info[2]
            follower['answer_num'] = user_info[3]
            follower['commend_num'] = user_info[4]
            yield follower



    def get_follow_num(self, response):
        """
        Returns a list with two intigers: [followee_num, follower_num]
        """

        self.logger.debug("get follower number")
        num = response.xpath('//div[@class="zm-profile-side-following zg-clear"]//strong/text()').extract()
        return list(map(int, num))


"""
 commit 之  前  删  密  码  啊 ！
 """
                      
