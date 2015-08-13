
import requests
from bs4 import BeautifulSoup


class Crawler(object):
    def __init__(self):
        self.url = "http://news.zum.com"
        response = requests.get(self.url)
        html = response.text
        # print(html)
        self.soup = BeautifulSoup(html)


if __name__ == '__main__':
    crawler = Crawler()
    print(crawler.soup)
