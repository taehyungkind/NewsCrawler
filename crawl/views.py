# from django.shortcuts import render
from .models import *
from django.shortcuts import HttpResponse
from django.db import transaction
from .daum_crawler import DaumCrawler
from .nate_crawler import NateCrawler
from .naver_crawler import NaverCrawler
from .zum_crawler import ZumCrawler
from django.utils import timezone
import json
# Create your views here.

@transaction.atomic(using="crawl", savepoint=True)
def crawl(request, host):
    ArticleRank.objects.all().update(view=False)

    host_dict = {
        "daum": DaumCrawler,
        "nate": NateCrawler,
        "naver": NaverCrawler,
        "zum": ZumCrawler
    }
    crawler = host_dict[host]()
    crawler.crawl_popular_news_list()

    h = Host.objects.get(name=host)

    for cate in crawler.category_list:
        news_list = crawler.get_category_news_list(cate)
        category = Category.objects.get(host=h, name=cate)
        for news in news_list:
            article = Article(id=news['id'], title=news['title'], url=news['url'], host=h, category=category)
            article.save()
            ArticleRank(article=article, rank=news['rank'], time=timezone.localtime(timezone.now())).save()
            print(news)

    return HttpResponse(json.dumps({'status': "ok"}))


def test(request):
    host_list = ["daum", "nate", "naver", "zum"]
    host_dict = {
        "daum": DaumCrawler,
        "nate": NateCrawler,
        "naver": NaverCrawler,
        "zum": ZumCrawler
    }

    for host in host_list:
        crawler = host_dict[host]()
        host = Host(name=host, url=crawler.url)
        host.save()
        crawler.crawl_popular_news_list()
        for category in crawler.category_list:
            print(category)
            Category(host=host, name=category).save()

    return HttpResponse(json.dumps({"status": "ok"}))
