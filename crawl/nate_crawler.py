
from .crawler import Crawler
from urllib.parse import urlparse


class NateCrawler(Crawler):

    def __init__(self):
        super(self.__class__, self).__init__("http://news.nate.com/rank/interest")

    def crawl_popular_news_list(self):
        self.category_list = ["sisa", "spo", "ent", "pol", "eco", "soc", "int", "its"]

        for category in self.category_list:
            soup = self.get_soup(self.url, {"sc": category})
            article_list = self.div_parser(soup)
            # 1~5위까지의 리스트만... 나머지는 ul_tag_parser에서 가져온다
            ul_tag = soup.find("ul", {"class": "mduRankSubject"})
            self.category_news_mapper.setdefault(category, article_list + self.ul_tag_parser(ul_tag))

    def div_parser(self, soup):
        article_list = []
        for rank, div in enumerate(soup.find_all("div", {"class": "mduSubjectList"})):
            article_dict = {}
            a_tag = div.find("a")
            article_dict["rank"] = rank + 1
            article_dict["title"] = a_tag.find("strong", {"class": "tit"}).text.strip()
            href = a_tag.get("href")
            article_dict["href"] = href
            article_dict["id"] = self.href_to_id(href)
            article_list.append(article_dict)

        return article_list

    def ul_tag_parser(self, soup):
        article_list = []
        for rank, li in enumerate(soup.find_all("li")):
            article_dict = {}
            a_tag = li.find("a")
            article_dict.setdefault("rank", rank + 6)
            article_dict.setdefault("title", a_tag.text.strip())
            href = a_tag.get("href")
            article_dict.setdefault("href", href)
            article_dict.setdefault("id", self.href_to_id(href))
            article_list.append(article_dict)

        return article_list

    @staticmethod
    def href_to_id(href):
        return urlparse(href).path[6:]


if __name__ == '__main__':
    crawler = NateCrawler()
    crawler.crawl_popular_news_list()
    crawler.get_category_news_list("sisa")
