#-*- coding: UTF-8 -*-

import sys
import utils
from utils import URLManager, Outputer

kMaxDepth = 10

def spider(root_url):
    urls = URLManager()
    outputer = Outputer()
    count = 1
    
    urls.add_new_url(root_url)
    while urls.has_new_url():
        try:
            new_url = urls.get_new_url()
            print 'craw %d: %s' % (count, new_url)
            html_source = utils.html_downloader(new_url)
            new_urls, new_data = utils.parser(new_url, html_source)

            urls.add_new_urls(new_urls)
            outputer.collect_data(new_data)
            count += 1
            if count == kMaxDepth:
                break

        except Exception as err:
            print 'craw failed: ', err

        outputer.output_html()

if __name__ == "__main__":
    root_url = "http://baike.baidu.com/view/21087.htm"
    spider(root_url)
    