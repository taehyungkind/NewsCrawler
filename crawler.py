
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
    def get_soup(url):
        return BeautifulSoup(requests.get(url).text)

    # 카테고리를 찾아서 카테고리 리스트에 넣어두고
    # 카테고리 항목에 맞는 뉴스 리스트를 맵핑시켜준다
    def get_popular_news_list(self):
        pass

    # 카테고리를 입력하면 카테고리의 뉴스 리스트를 가져온다.
    def get_category_news_list(self, category):
        pass
