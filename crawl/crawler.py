
import requests
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, url):
        self.category_list = []
        self.category_news_mapper = {}
        self.url = url
        self.soup = self.get_soup(self.url)

    # url을 인풋으로 줬을 때, BeautifulSoup 객체를 반환하는 함수
    @staticmethod
    def get_soup(url, param=None):
        return BeautifulSoup(requests.get(url, params=param).text, "html.parser")

    # 카테고리를 찾아서 카테고리 리스트에 넣어두고
    # 카테고리 항목에 맞는 뉴스 리스트를 맵핑시켜준다
    def crawl_popular_news_list(self):
        pass

    # 카테고리를 입력하면 카테고리의 뉴스 리스트를 가져온다.
    def get_category_news_list(self, category):
        news_list = self.category_news_mapper.get(category)
        if news_list is None:
            print("카테고리를 정확히 입력해주세요")
            return []

        # print(category)
        # for news in news_list:
        #     url = urljoin(self.url, news["href"])
        #     print(url)
        #     print(news["title"], news["href"])
        return news_list
