
from crawler import Crawler


class DaumCrawler(Crawler):

    def __init__(self, url):
        super(self.__class__, self).__init__(url)

    def get_popular_news_list(self):
        self.category_list = ["society", "politics", "culture", "economic", "foreign", "digital", "sports", "entertain"]

        for category in self.category_list:
            soup = self.get_soup(self.url, {"include": category})
            ul_tag = soup.find("ul", {"class": "list_rank"})
            self.category_news_mapper.setdefault(category, self.ul_tag_parser(ul_tag))
            print()

    @staticmethod
    def ul_tag_parser(soup):
        article_list = []
        for li in soup.find_all("li")[:10]:
            article_dict = {}
            article_dict.setdefault("screen_out", li.find("span", {"class", "screen_out"}).text.strip())
            thumb = li.find("div", {"class": "cont_thumb"})
            a_tag = thumb.find("a", {"class": "link_txt"})
            article_dict.setdefault("title", a_tag.text.strip())
            href = a_tag.get("href")
            article_dict.setdefault("href", href)
            article_dict.setdefault("id", href[3:])
            article_list.append(article_dict)

        return article_list


if __name__ == '__main__':
    crawler = DaumCrawler("http://media.daum.net/netizen/popular/")
    # print(crawler.soup)
    crawler.get_popular_news_list()
