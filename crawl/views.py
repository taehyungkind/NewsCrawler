from django.shortcuts import render
from django.shortcuts import HttpResponse
from .crawler import Crawler
from .daum_crawler import DaumCrawler
from .nate_crawler import NateCrawler
from .naver_crawler import NaverCrawler
from .zum_crawler import ZumCrawler
import json
# Create your views here.


def daum_crawl(request):
    crawler = DaumCrawler()
    crawler.crawl_popular_news_list()
    news_list = crawler.get_category_news_list("digital")
    return HttpResponse(json.dumps(news_list))