
import requests
from bs4 import BeautifulSoup
from urllib.request import urljoin


class Crawler(object):
    def __init__(self):
        self.category_list = []
        self.category_news_mapper = {}
        self.url = "http://news.zum.com"

        self.soup = self.get_soup(self.url)

    @staticmethod
    def get_soup(url):
        response = requests.get(url)
        return BeautifulSoup(response.text)

    def get_popular_news_list(self):
        popular_list = self.soup.find("div", {"class": "list list_1"})
        category_tag_list = popular_list.find_all("h4")
        self.category_list = [tag.text.strip() for tag in category_tag_list]

        category_news_list = popular_list.find_all("ul", {"class": "rank_news"})
        for idx, ul_tag in enumerate(category_news_list):
            self.category_news_mapper.setdefault(self.category_list[idx], self.ul_tag_parser(ul_tag))

    @staticmethod
    def ul_tag_parser(soup):
        li_list = soup.find_all("li")
        article_list = []
        for li in li_list:
            article_dict = {}
            info = li.find("span")
            article_dict.setdefault(info.get("class")[0], info.text.strip())

            tag = li.find("a")
            article_dict.setdefault("title", tag.get("title"))
            href = tag.get("href")
            article_dict.setdefault("href", href[: href.find("?")])
            article_dict.setdefault("id", href[href.find("s/") + 2: href.find("?")])
            article_list.append(article_dict)
        return article_list

    def get_category_news_list(self, category):
        news_list = self.category_news_mapper[category]
        for news in news_list:
            url = urljoin(self.url, news["href"])
            self.article_parser(url)

    def article_parser(self, url):
        soup = self.get_soup(url)
        article = soup.find("div", {"id": "article"})
        body = article.find("div", {"id": "article_body"})
        print(body)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.get_popular_news_list()
    crawler.get_category_news_list("IT")
