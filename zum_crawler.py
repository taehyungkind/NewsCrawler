
from crawler import Crawler


class ZumCrawler(Crawler):

    def __init__(self, url):
        super(self.__class__, self).__init__(url)

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
        article_list = []
        for li in soup.find_all("li"):
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

    # # 기사의 데이터를 가져온다.
    # def article_parser(self, url):
    #     print(url)
    #     soup = self.get_soup(url)
    #     article = soup.find("div", {"id": "article"})
    #
    #     title = article.find("h2").text.strip()
    #     sponsor = article.find("a", {"class": "spon_media"})
    #     sponsor_name, sponsor_url = sponsor.text.strip(), sponsor.get("href")
    #     origin_url = article.find("a", {"class": "basic_doc"}).get("href")
    #     pub_date, modified_date = self.get_dates(article.find_all("span", {"class": "date"}))
    #     print(title, sponsor_name, sponsor_url, pub_date, modified_date, origin_url)
    #
    #     body = article.find("div", {"id": "article_body"})
    #     images = self.get_images(body)
    #     print(images)
    #
    #     keywords = self.get_keywords(body)
    #     print(keywords)
    #
    #     # text = body.prettify()
    #     # text = text.replace("<br/>", "\n")
    #     content = str(body).replace("<br/>", "\n")
    #     content = BeautifulSoup(content).text
    #     print(content)
    #
    # # 날짜를 가져오는 함수이다. 최초작성시간과 수정날짜를 가져온다.
    # @staticmethod
    # def get_dates(element):
    #     pub_date = element[0].text.strip()
    #     try:
    #         return pub_date, element[1].text.strip()
    #     except IndexError:
    #         return pub_date, None
    #
    # # 이미지 정보를 추출하고 위치를 지정하는 함수
    # # 이미지 위치에는 { image }만 남기고 이미지에 관련된 태그는 모조리 삭제해버린다.
    # @staticmethod
    # def get_images(body):
    #     img_list = []
    #     for tag in body.find_all("table"):
    #         url = tag.find("img").get("src")
    #
    #         try:
    #             desc = tag.find("p", {"class": "img_title"}).text.strip()
    #         except AttributeError:
    #             desc = None
    #         tag.parent.insert(tag.parent.contents.index(tag), "{ image }")
    #         tag.extract()
    #         img_list.append({"url": url, "description": desc})
    #
    #     [tag.extract() for tag in body.find_all("p", {"class": "img_title"})]
    #     return img_list
    #
    # # 키워드를 추출해내는 함수이다. 맨위에만 붙는다고 가정하고 지워버린다.
    # @staticmethod
    # def get_keywords(body):
    #     keywords = [tag.text for tag in body.find_all("p", {"class": "keyword"})]
    #
    #     try:
    #         body.find("div", {"class": "keyword_wrap"}).extract()
    #     except AttributeError:
    #         pass
    #     return keywords


if __name__ == '__main__':
    crawler = ZumCrawler("http://news.zum.com")
    crawler.get_popular_news_list()
    crawler.get_category_news_list("IT")
