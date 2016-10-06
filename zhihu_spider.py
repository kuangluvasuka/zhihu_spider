#-*- coding: UTF-8 -*-

import sys
import re
import urllib2
from bs4 import BeautifulSoup

def get_page_source(url):
    page_source = urllib2.urlopen(url).read()
    return str(page_source)
    
def parse_text(plain_text):
    soup = BeautifulSoup(plain_text, "html.parser")
    list_soup = soup.find('title')
    # print list_soup
    print list_soup.string.strip()
    
if __name__ == "__main__":
    page = get_page_source("https://book.douban.com/subject/26873486/?icn=index-editionrecommend")
    parse_text(page)