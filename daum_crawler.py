
from crawler import Crawler
import requests
from bs4 import BeautifulSoup
from urllib.request import urljoin

class DaumCrawler(Crawler):

    def __init__(self, url):
        super(self.__class__, self).__init__(url)


if __name__ == '__main__':
    crawler = DaumCrawler("http://media.daum.net/netizen/popular")
    # print(crawler.soup)
