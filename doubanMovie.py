#-*- coding: UTF-8 -*-

import codecs
import sys
import random
import requests
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17'}
    ]


def main(tags):
    spider_net = ''
    for tag in tags:
        spider_net += '**' * 40 + '\n' \
                    + '  ' * 17 + tag + '\n' \
                    + '**' * 40 + '\n'
        spider_net += movie_spider(tag)
        print tag + ' finished.'
    
    with open('movie_data.txt', 'w') as f:
        f.write(spider_net)


def movie_spider(movieTag):
    """ Spider goes over the movie list, and looks up each entry for details.
    """
    root = "https://movie.douban.com/tag/%s" % movieTag
    global headers
    result = ''
    html = requests.get(root, headers=random.choice(headers)).content
    tree = etree.HTML(html.decode('utf-8'))
    items = tree.xpath("//table/tr[@class='item']")
    print len(items)
    for item in items:
        itemURL = item.xpath("td/a[@class='nbg']/@href")[0].strip()
        itemHTML = requests.get(itemURL, headers=random.choice(headers)).content
        itemTree = etree.HTML(itemHTML.decode('utf-8'))
        title = itemTree.xpath("//h1/span[@property='v:itemreviewed']/text()")[0].strip()
        info = itemTree.xpath("//div[@class='subject clearfix']/div[@id='info']")[0]
        director = info.xpath(".//a[@rel='v:directedBy']/text()")
        scriptor = info.xpath("span")[1].xpath("span/a/text()")      # scriptor is not well formatted
        actors = info.xpath(".//a[@rel='v:starring']/text()")
        genre = info.xpath(".//span[@property='v:genre']/text()")
        initDate = info.xpath(".//span[@property='v:initialReleaseDate']/text()")
        rating = itemTree.xpath("//strong[@property='v:average']/text()")[0].strip()
        
        result += '电影：' + title + '\n' \
                + '导演：' + '/'.join(director[:]) + '\n' \
                + '编剧：' + '/'.join(scriptor[:]) + '\n' \
                + '演员：' + '/'.join(actors[:]) + '\n' \
                + '类型：' + '/'.join(genre[:]) + '\n' \
                + '上映日期：' + '/'.join(initDate[:]) + '\n' \
                + '评分：' + rating + '\n' \
                + '--' * 40 + '\n'
           
    return result


if __name__ == "__main__":
    tags = ['宫崎骏', '剧情']
    main(tags)
    
