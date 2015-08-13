
import requests
from bs4 import BeautifulSoup


class Crawler(object):
    def __init__(self):
        self.mapper = {}

        self.url = "http://news.zum.com"
        response = requests.get(self.url)
        html = response.text
        # print(html)
        self.soup = BeautifulSoup(html)

    def get_popular_news_list(self):
        popular_list = self.soup.find("div", {"class": "list list_1"})
        category_tag_list = popular_list.find_all("h4")
        category_list = [tag.text.strip() for tag in category_tag_list]

        category_news_list = popular_list.find_all("ul", {"class": "rank_news"})
        for idx, ul_tag in enumerate(category_news_list):
            self.mapper.setdefault(category_list[idx], self.ul_tag_parser(ul_tag))

    def ul_tag_parser(self, soup):
        li_list = soup.find_all("li")
        article_list = []
        for li in li_list:
            article_dict = {}
            info = li.find("span")
            article_dict.setdefault(info.get("class")[0], info.text.strip())
            tag = li.find("a")
            href = tag.get("href")
            article_dict["href"] = href[: href.find("?")]
            article_dict["id"] = href[href.find("s/") + 2: href.find("?")]
            article_dict["title"] = tag.get("title")
            article_list.append(article_dict)
        return article_list


if __name__ == '__main__':
    crawler = Crawler()
    crawler.get_popular_news_list()
    print(crawler.mapper)
