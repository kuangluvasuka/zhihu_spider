#-*- coding: UTF-8 -*-

import sys
import random
import requests
import datetime
import logging
from pymongo import MongoClient
from lxml import etree

class MovieSpider(object):
    def __init__(self):
        
        self.tag_list = []
        self._movie_list = []

        self._client = MongoClient('mongodb://localhost:27017/')
        self._db = self._client.movie
        self._collection = self._db.database

        self.headers = [
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17'}
            ]

        self.MAX_NUM = 20


    def main(self):
        # change the log level if needed
        logging.basicConfig(filename='spider.log', format='%(asctime)s %(message)s',  level=logging.WARNING)
        
        self.genTags()
        for tag in self.tag_list:
            print("Crawling tag: %s" % tag)
            self.movie_spider(tag)
            self._collection.insert_many(self._movie_list)
            self._movie_list = []


    def genTags(self):
        url = "https://movie.douban.com/tag/?view=type"
        try:
            html = requests.get(url, headers=random.choice(self.headers)).content
            tree = etree.HTML(html.decode('utf-8'))
            table = tree.xpath("//table[@class='tagCol']")[0]   # 3 tables, pick the first: 类型
            for entry in table.xpath(".//td/a"):
                tag = entry.xpath("text()")[0].strip()
                self.tag_list.append(tag)

        except Exception as e:
            logging.exception('Error while generating tag lists')


    def movie_spider(self, movieTag):
        """ Spider goes over the movie list, and looks up each entry for details.
        """
        index = 0
        logging.info("Start crawling tag: %s" % movieTag)
        while index < self.MAX_NUM:
            root = "https://movie.douban.com/tag/%s?start=%d&type=T" % (movieTag, index)
            result = {}
            try:
                html = requests.get(root, headers=random.choice(self.headers)).content
                tree = etree.HTML(html.decode('utf-8'))
                items = tree.xpath("//table/tr[@class='item']")
                if len(items) == 0:
                    break
                index += len(items)
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
                    runtime = info.xpath(".//span[@property='v:runtime']/text()")
                    rating = itemTree.xpath("//strong[@property='v:average']/text()")[0].strip()
                    
                    result['title'] = title
                    result['director'] = '/'.join(director[:])
                    result['scriptor'] = '/'.join(scriptor[:])
                    result['actors'] = '/'.join(actors[:])
                    result['genre'] = '/'.join(genre[:])
                    result['initDate'] = '/'.join(initDate[:])
                    result['runtime'] = '/'.join(runtime[:])
                    result['rating'] = rating

                    self._movie_list.append(result)
                    result = {}

            except Exception as e:
                logging.exception("Error while crawling tag: %s" % movieTag)

                
if __name__ == "__main__":
    # tags = ['宫崎骏']
    spider = MovieSpider()
    spider.main()
    
