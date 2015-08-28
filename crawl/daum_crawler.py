
from .crawler import Crawler
from urllib.parse import urljoin


class DaumCrawler(Crawler):

    def __init__(self):
        super(self.__class__, self).__init__("http://media.daum.net/netizen/popular/")

    def crawl_popular_news_list(self):
        self.category_list = ["society", "politics", "culture", "economic", "foreign", "digital", "sports", "entertain"]

        for category in self.category_list:
            soup = self.get_soup(self.url, {"include": category})
            ul_tag = soup.find("ul", {"class": "list_rank"})
            self.category_news_mapper.setdefault(category, self.ul_tag_parser(ul_tag))

    def ul_tag_parser(self, soup):
        article_list = []
        for li in soup.find_all("li")[:10]:
            article_dict = {}
            article_dict.setdefault("rank", li.find("span", {"class", "screen_out"}).text.strip())
            a_tag = li.find("div", {"class": "cont_thumb"}).find("a", {"class": "link_txt"})
            article_dict.setdefault("title", a_tag.text.strip())
            href = a_tag.get("href")
            article_dict.setdefault("href", urljoin(self.url, href))
            article_dict.setdefault("id", href[3:])
            article_list.append(article_dict)

        return article_list


if __name__ == '__main__':
    crawler = DaumCrawler()
    crawler.crawl_popular_news_list()
    crawler.get_category_news_list("digital")
