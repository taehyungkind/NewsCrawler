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
from datetime import datetime
from time import mktime
import time
import operator
# Create your views here.


@transaction.atomic(using="crawl", savepoint=True)
def crawl(request):
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
                # timezone.localtime(timezone.now())).save()
                # print(news)

    return HttpResponse(json.dumps({'status': "ok"}))


def get_category_news(request, host_name, category_name):
    # host = Host.objects.get(name=host_name)
    # category = Category.objects.filter(host=host, name=category_name)
    category = Category.objects.filter(host__name=host_name, name=category_name)

    # articles = ArticleRank.objects.filter(category=category, view=True).select_related('article')
    # TODO 조인방법을 찾아보자 (딕셔너리로 바꾸고 서브쿼리 보내고 정렬하는 거 없이 한큐에!)
    rank_list = ArticleRank.objects.filter(category=category, view=True).values("article", "rank")
    rank_dict = dict([(rank['article'], rank['rank']) for rank in rank_list])
    articles = Article.objects.filter(id__in=rank_dict.keys())

    news_list = []
    for article in articles:
        news_list.append({
            "rank": rank_dict[article.id],
            "title": article.title,
            "url": article.url,
        })
    ordered_news_list = sorted(news_list, key=operator.itemgetter('rank'))
    return HttpResponse(json.dumps(ordered_news_list))


def get_timezone_now():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now = time.strptime(now, "%Y-%m-%d %H:%M:%S")
    now = datetime.fromtimestamp(mktime(now)).replace(tzinfo=timezone.utc)
    return now


def get_host_category_names(request):
    host_list = Host.objects.all()
    for host in host_list:
        category_list = Category.objects.filter(host=host)
    print(host_list)

    last_crawl_time = ArticleRank.objects.all().order_by("-time")[0].time.strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(json.dumps({"result": last_crawl_time}))


def get_now_news(request):
    host_list = ["daum", "nate", "naver", "zum"]
    host_dict = {
        "daum": DaumCrawler,
        "nate": NateCrawler,
        "naver": NaverCrawler,
        "zum": ZumCrawler
    }

    all_news = {}
    all_news["host_list"] = host_list
    for host in host_list:
        crawler = host_dict[host]()
        crawler.crawl_popular_news_list()
        all_news[host] = {
            "news": crawler.category_news_mapper,
            "category_list": crawler.category_list
        }

    return HttpResponse(json.dumps(all_news))


def db_initializer(request):
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
