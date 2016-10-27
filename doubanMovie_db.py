#-*- coding: UTF-8 -*-

import sys
import random
import requests
import datetime
import logging
from pymongo import MongoClient
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')

class MovieSpider(object):
    def __init__(self):
        
        self._movie_list = []

        self._client = MongoClient('mongodb://localhost:27017/')
        self._db = self._client.movie
        self._collection = self._db.database
        self._count = 0

        self.headers = [
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17'}
            ]


    def main(self, tags):
        logging.basicConfig(filename='spider.log', format='%(asctime)s %(message)s',  level=logging.INFO)
        # spider_net = ''
        for tag in tags:
            self.movie_spider(tag)
            self._collection.insert_many(self._movie_list)
            self._movie_list = []


    def movie_spider(self, movieTag):
        """ Spider goes over the movie list, and looks up each entry for details.
        """
        logging.info("Start crawling tag: %s" % movieTag)
        root = "https://movie.douban.com/tag/%s" % movieTag
        result = {}
        try:
            html = requests.get(root, headers=random.choice(self.headers)).content
            tree = etree.HTML(html.decode('utf-8'))
            items = tree.xpath("//table/tr[@class='item']")
            print len(items)
            for item in items:
                itemURL = item.xpath("td/a[@class='nbg']/@href")[0].strip()
                itemHTML = requests.get(itemURL, headers=random.choice(self.headers)).content
                itemTree = etree.HTML(itemHTML.decode('utf-8'))
                title = itemTree.xpath("//h1/span[@property='v:itemreviewed']/text()")[0].strip()
                info = itemTree.xpath("//div[@class='subject clearfix']/div[@id='info']")[0]
                director = info.xpath(".//a[@rel='v:directedBy']/text()")
                scriptor = info.xpath("span")[1].xpath("span/a/text()")      # scriptor is not well formatted
                actors = info.xpath(".//a[@rel='v:starring']/text()")
                genre = info.xpath(".//span[@property='v:genre']/text()")
                initDate = info.xpath(".//span[@property='v:initialReleaseDate']/text()")
                rating = itemTree.xpath("//strong[@property='v:average']/text()")[0].strip()
                
                result['title'] = title
                result['director'] = '/'.join(director[:])
                result['scriptor'] = '/'.join(scriptor[:])
                result['actors'] = '/'.join(actors[:])
                result['genre'] = '/'.join(genre[:])
                result['initDate'] = '/'.join(initDate[:])
                result['rating'] = rating

                self._movie_list.append(result)
                result = {}
        except Exception as e:
            logging.exception("Crawling error")
            
            
            
            


if __name__ == "__main__":
    tags = ['宫崎骏']
    # main(tags)
    spider = MovieSpider()
    spider.main(tags)
    
