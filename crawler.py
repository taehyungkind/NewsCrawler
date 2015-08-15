
import requests
from bs4 import BeautifulSoup
from urllib.request import urljoin


class Crawler(object):
    def __init__(self):
        self.category_list = []
        self.category_news_mapper = {}
        self.url = "http://news.zum.com"

        self.soup = self.get_soup(self.url)

    # url을 인풋으로 줬을 때, BeautifulSoup 객체를 반환하는 함수
    @staticmethod
    def get_soup(url):
        return BeautifulSoup(requests.get(url).text)

    # 카테고리를 찾아서 카테고리 리스트에 넣어두고
    # 카테고리 항목에 맞는 뉴스 리스트를 맵핑시켜준다
    def get_popular_news_list(self):
        popular_list = self.soup.find("div", {"class": "list list_1"})
        category_tag_list = popular_list.find_all("h4")
        self.category_list = [tag.text.strip() for tag in category_tag_list]

        category_news_list = popular_list.find_all("ul", {"class": "rank_news"})
        for idx, ul_tag in enumerate(category_news_list):
            self.category_news_mapper.setdefault(self.category_list[idx], self.ul_tag_parser(ul_tag))

    # BeautifulSoup 객체 상태인 ul태그를 li로 쪼개고
    # 필요한 정보만 가져오도록 한다. 제목, path, 기사의 고유번호인 id, 랭킹을 가져온다
    # 종합 뉴스의 처리는 일단 나중에 하자.
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

    # 카테고리를 입력하면 카테고리의 뉴스 리스트를 가져온다.
    # 우선은 기사 데이터까지 가져오자!
    def get_category_news_list(self, category):
        news_list = self.category_news_mapper.get(category)
        if news_list is None:
            print("카테고리를 정확히 입력해주세요")
            return

        for news in news_list:
            url = urljoin(self.url, news["href"])
            self.article_parser(url)

    # 기사의 데이터를 가져온다.
    def article_parser(self, url):
        soup = self.get_soup(url)
        article = soup.find("div", {"id": "article"})

        title = article.find("h2").text.strip()
        sponsor = article.find("a", {"class": "spon_media"})
        sponsor_name, sponsor_url = sponsor.text.strip(), sponsor.get("href")
        origin_url = article.find("a", {"class": "basic_doc"}).get("href")
        pub_date, modified_date = self.get_dates(article.find_all("span", {"class": "date"}))
        print(title, sponsor_name, sponsor_url, pub_date, modified_date, origin_url)

        body = article.find("div", {"id": "article_body"})
        images = self.get_images(body)
        print(images)

        # text = body.prettify()
        # text = text.replace("<br/>", "\n")
        temp = str(body).replace("<br/>", "\n")
        temp = BeautifulSoup(temp)
        print(temp)

    # 날짜를 가져오는 함수이다. 최초작성시간과 수정날짜를 가져온다.
    @staticmethod
    def get_dates(element):
        pub_date = element[0].text.strip()
        if len(element) > 1:
            modified_date = element[1].text.strip()
        else:
            modified_date = None
        return pub_date, modified_date

    # 이미지 정보를 추출하고 위치를 지정하는 함수
    @staticmethod
    def get_images(body):
        img_list = []
        for tag in body.find_all("table"):
            url = tag.find("img").get("src")
            _desc = tag.find("p", {"class": "img_title"})
            if _desc is None:
                desc = None
            else:
                desc = _desc.text.strip()
            tag.next_sibling.append("{ image }")
            tag.extract()
            img_list.append({"url": url, "description": desc})

        return img_list


if __name__ == '__main__':
    crawler = Crawler()
    # crawler.get_popular_news_list()
    # crawler.get_category_news_list("IT")

    article_url = 'http://news.zum.com/articles/24291861'
    crawler.article_parser(article_url)
