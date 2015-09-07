"""NewsCrawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^crawl/$', "crawl.views.crawl", name="crawl"),
    url(r'^(?P<host_name>daum|nate|naver|zum)/(?P<category_name>\w+)/$', "crawl.views.get_category_news"),
    url(r'^get/host/category/$', "crawl.views.get_host_category_names"),

    url(r'^get/now/news/$', "crawl.views.get_now_news"),
    url(r'^init/$', "crawl.views.db_initializer", name="db_init"),
]
