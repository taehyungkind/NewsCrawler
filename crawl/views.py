# from django.shortcuts import render
from .models import *
from django.shortcuts import HttpResponse
from .daum_crawler import DaumCrawler
from .nate_crawler import NateCrawler
from .naver_crawler import NaverCrawler
from .zum_crawler import ZumCrawler
import json
# Create your views here.


def crawl(request, host):
    host_dict = {
        "daum": DaumCrawler,
        "nate": NateCrawler,
        "naver": NaverCrawler,
        "zum": ZumCrawler
    }
    crawler = host_dict[host]()

    h = Host.objects.get(name=host)
    crawler.crawl_popular_news_list()
    print(crawler.category_list)
    for category in crawler.category_list:
        print(category)
        Category(host=h, name=category).save()
    print(h)
    news_list = crawler.get_category_news_list(crawler.category_list[0])

    return HttpResponse(json.dumps(news_list))
