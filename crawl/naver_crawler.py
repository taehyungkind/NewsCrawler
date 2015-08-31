
from .crawler import Crawler
from urllib.parse import urlparse, parse_qs, urljoin


class NaverCrawler(Crawler):

    def __init__(self):
        super(self.__class__, self).__init__("http://news.naver.com/main/home.nhn")

    def crawl_popular_news_list(self):
        for dummy in ["ranking_10" + str(num) for num in range(8)]:
            chunk = self.soup.find("div", {"id": dummy})
            category = chunk.find("h5", {"class": "blind"}).text.strip()
            self.category_list.append(category)
            self.category_news_mapper.setdefault(category, self.ul_tag_parser(chunk.find("ul")))

    def ul_tag_parser(self, soup):
        article_list = []
        for li in soup.find_all("li"):
            article_dict = {}
            article_dict.setdefault("rank", li.find("span", {"class", "rank"}).text.strip())
            a_tag = li.find("a", {"class": "nclicks(rig.ranking)"})
            article_dict.setdefault("title", a_tag.text.strip())
            href = a_tag.get("href")
            article_dict.setdefault("url", urljoin(self.url, href))

            query_param = parse_qs(urlparse(href).query)
            try:
                article_dict.setdefault("id", query_param["aid"][0])
            except KeyError:
                article_dict.setdefault("id", query_param["article_id"][0])
            article_list.append(article_dict)

        return article_list


if __name__ == '__main__':
    crawler = NaverCrawler()
    crawler.crawl_popular_news_list()
    crawler.get_category_news_list(crawler.category_list[2])
