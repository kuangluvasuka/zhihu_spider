#-*- coding: UTF-8 -*-

import re
import codecs
import urllib2
import urlparse
from bs4 import BeautifulSoup

kStatusCodeOK = 200


class URLManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    
    def has_new_url(self):
        return len(self.new_urls) != 0

    
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

class Outputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open('output.html', 'w', 'utf-8')

        fout.write('<html><head><meta charset="UTF-8"></head>')
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            # data['summary'] = u.data['summary']

            fout.write("<tr>")
            print 'url:', data['url']
            fout.write("<td>%s</td>" % data['url'])
            print 'title:', data['title']
            fout.write("<td>%s</td>" % data['title'])
            print 'summary:', data['summary']
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

def parser(page_url, page_source):
    """ Parse the page to _get_new_urls and _get_new_data
    """
    if page_url is None or page_source is None:
        return
    soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
    new_urls = _get_new_urls(page_url, soup)
    new_data = _get_new_data(page_url, soup)
    return new_urls, new_data

def _get_new_urls(page_url, soup):
    new_urls = set()
    links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
    for link in links:
        new_url = urlparse.urljoin(page_url, link['href'])
        new_urls.add(new_url)
    return new_urls

def _get_new_data(page_url, soup):
    res_data = {}
    title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
    res_data['title'] = title_node.get_text()
    summary_node = soup.find('div', class_="lemma-summary")
    res_data['summary'] = summary_node.get_text()
    res_data['url'] = page_url
    return res_data


def html_downloader(url):
    if url is None:
        return None
    response = urllib2.urlopen(url)
    if response.getcode() is not kStatusCodeOK:
        return None
    return response.read()




