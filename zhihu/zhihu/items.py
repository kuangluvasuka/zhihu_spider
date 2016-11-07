# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    follower_num = scrapy.Field()
    ask_num = scrapy.Field()
    answer_num = scrapy.Field()
    commend_num = scrapy.Field()



    
    
