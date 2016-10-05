#-*- coding: UTF-8 -*-

import sys
import re
import urllib
from bs4 import BeautifulSoup

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
    
def getImg(html):
    imgre = re.compile(r'src="(.+?\.jpg)" pic_ext')
    imglist = re.findall(imgre, html)
    x = 0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, '%s.jpg' % x)
        x += 1

if __name__ == "__main__":
    html = getHtml("http://tieba.baidu.com/p/2460150866")
    getImg(html)