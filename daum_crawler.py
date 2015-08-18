
from crawler import Crawler


class DaumCrawler(Crawler):

    def __init__(self, url):
        super(self.__class__, self).__init__(url)

    def get_popular_news_list(self):
        self.category_list = ["society", "politics", "culture", "economic", "foreign", "digital", "sports", "entertain"]

        for category in self.category_list:
            soup = self.get_soup(self.url, {"include": category})
            ul_tag = soup.find("ul", {"class": "list_rank"})
            self.ul_tag_parser(ul_tag)
            print()

    @staticmethod
    def ul_tag_parser(soup):
        article_list = []
        for li in soup.find_all("li")[:10]:
            print(li.find("span", {"class": "desc_issue"}).text)

        return article_list


if __name__ == '__main__':
    crawler = DaumCrawler("http://media.daum.net/netizen/popular/")
    # print(crawler.soup)
    crawler.get_popular_news_list()
