
from NewsCrawler.celery import app

from crawl.models import *
from crawl.daum_crawler import DaumCrawler
from crawl.nate_crawler import NateCrawler
from crawl.naver_crawler import NaverCrawler
from crawl.zum_crawler import ZumCrawler

from datetime import datetime
import time
from time import mktime
from django.utils import timezone
from django.db import transaction


@app.task(bind=True, name="crawling", serializer='json')
@transaction.atomic(using="crawl", savepoint=True)
def crawling(self):
    # self가 없으면 Type error 발생한다 원인은 모르겠음
    ArticleRank.objects.all().update(view=False)

    host_list = ["daum", "nate", "naver", "zum"]
    host_dict = {
        "daum": DaumCrawler,
        "nate": NateCrawler,
        "naver": NaverCrawler,
        "zum": ZumCrawler
    }

    for host_name in host_list:
        crawler = host_dict[host_name]()
        crawler.crawl_popular_news_list()

        host = Host.objects.get(name=host_name)
        for category_name in crawler.category_list:
            news_list = crawler.get_category_news_list(category_name)
            category = Category.objects.get(host=host, name=category_name)
            for news in news_list:
                article = Article(id=news['id'], title=news['title'], url=news['url'], host=host)
                article.save()
                ArticleRank(article=article, category=category, rank=news['rank'], time=get_timezone_now()).save()


def get_timezone_now():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now = time.strptime(now, "%Y-%m-%d %H:%M:%S")
    now = datetime.fromtimestamp(mktime(now)).replace(tzinfo=timezone.utc)
    return now
